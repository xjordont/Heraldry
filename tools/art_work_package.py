#!/usr/bin/env python3
"""Self-contained ChatGPT Work input package for the current illustration queue, and its review-bundle check.

  python3 tools/art_work_package.py build [--out ZIP] [--allow-dirty]
        Write the deterministic input ZIP (default build/art/Heraldry_Work_Input_<phase>.zip; a build output, never
        committed) and a copy of its WORK_PACKAGE.json beside it. The ZIP holds the exact queue, its prompt files, every queue-listed reference
        as real image bytes, the complete v7 skill (source folder and installable ZIP), current receipts, selection
        state and the style config the skill validator reads. Nothing else: no other art, no private reference PDFs.
  python3 tools/art_work_package.py verify ZIP [--no-run]
        Extract into an empty temporary folder and check the manifest, prompt hashes and reference decoding, then run
        the packaged work_preflight.py --offline-package and helper doctor/status with Git credentials unavailable.
  python3 tools/art_work_package.py verify-bundle BUNDLE.zip
        Claude Code's first step on a Work review bundle: hashes, receipts, QA reports and references against this repo.
        It approves nothing.
  python3 tools/art_work_package.py import-bundle BUNDLE.zip
        verify-bundle, then copy the native images into assets/art/incoming and append receipts_append.jsonl to
        RECEIPTS.jsonl (lines already present are skipped). Used by the 'Import Work review bundle' workflow on bundles
        committed to production/art/work/inbox/, so no Git LFS upload is needed from the delivering machine. It approves
        nothing: intake and orchestrator review follow.

Work cannot authenticate shell git, and the GitHub connector cannot fetch large binary references, so the package is
the delivery route for Work's inputs. It is built only from committed files: the manifest names the source commit.
"""
import argparse, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
QUEUE = "production/art/gpt/QUEUE.json"
SKILL_DIR = "production/art/skill/heraldry-classic-ink-art"
SKILL_ZIP = "production/art/skill/Heraldry_Classic_Ink_Art_Skill_v7_0.zip"
FIXED = {  # path: role
    QUEUE: "queue",
    "production/art/gpt/QUEUE.md": "queue",
    "production/art/gpt/INSTRUCTIONS.md": "instructions",
    "production/art/gpt/RECEIPTS.jsonl": "receipts",
    "production/art/SELECTIONS.json": "selections",
    "config/art_style.json": "config",
}
OUT_DIR = ROOT / "build/art"
STAMP = (2026, 10, 11, 0, 0, 0)
KIND = "heraldry-work-input-package"
LFS = b"version https://git-lfs"
SCRIPTS = f"{SKILL_DIR}/scripts"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def decode(data, name):
    if data[:len(LFS)] == LFS:
        raise SystemExit(f"{name} is a Git LFS pointer, not image bytes: fetch it (git lfs pull --include={name}) before packaging")
    with Image.open(io.BytesIO(data)) as im:
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        return im.format, [im.width, im.height]


def prompt_sha(text):
    return sha((text[:-1] if text.endswith("\n") else text).encode())


def contents(root=ROOT):
    """{path: (bytes, role)} for everything the package holds, read from root, plus the queue."""
    q = json.loads((root / QUEUE).read_text(encoding="utf-8"))
    if q.get("schema") != 2:
        raise SystemExit("QUEUE.json must be schema 2")
    paths = dict(FIXED)
    for it in q["items"]:
        paths[it["prompt"]] = "prompt"
        for r in it["references"]:
            paths[r] = "reference"
    for f in sorted((root / SKILL_DIR).rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
            paths[f.relative_to(root).as_posix()] = "skill"
    out = {}
    for rel, role in sorted(paths.items()):
        f = root / rel
        if not f.is_file():
            raise SystemExit(f"missing package input: {rel}")
        if rel.lower().endswith(".pdf") or rel.startswith("references/"):
            raise SystemExit(f"refusing to package private reference material: {rel}")
        out[rel] = (f.read_bytes(), role)
    return q, out


def start_here(q, src):
    ids = "\n".join(f"{n}. `{it['id']}` ({it['register']}, {it['size']}, at most {it['max_attempts']} attempts) "
                    f"- attach exactly: {', '.join('`' + r + '`' for r in it['references'])}" for n, it in enumerate(q["items"], 1))
    h = f"python {SCRIPTS}/heraldry_art.py"
    s = "/mnt/data/heraldry_work_scratch"
    return f"""# Heraldry ChatGPT Work input package: START HERE

Source: `{src['repository']}` `{src['branch']}` commit `{src['commit']}`. Queue phase `{q['phase']}`, {q['count']} items.
This package replaces the authenticated Git checkout for **inputs only**. It holds the exact queue, prompts,
references (real image bytes), the complete v7 skill, receipts and selection state, with SHA-256 for every file
in `WORK_PACKAGE.json`. It cannot push anything to GitHub, and it approves nothing.

## 1. Unpack and verify (no Git, no credentials)

Unzip into the new empty folder `/mnt/data/heraldry_work` (any empty folder works; these paths assume this one) and
run every command from inside it. Do not run `git init`, `git clone` or `git pull` here. The helper keeps attempt
counts, print-size previews and QA copies in the sibling folder `{s}`; put your own scratch files
(native images, QA JSON, smoke record) there too, never inside the package folder.

```
cd /mnt/data/heraldry_work
python {SCRIPTS}/work_preflight.py --repo . --offline-package --require-installed
{h} doctor
{h} status
```

Expected: `status` READY, `source.kind` offline_package, `delivery` bundle, `remote_access` NOT_ATTEMPTED,
`image_and_reference_tool` UNVERIFIED. Any BLOCKED result: stop and report it word for word. Never edit a
packaged file; the preflight rejects any change (receipts may only grow).

## 2. Smoke test inside Work (required; no script can do it)

Confirm that the image tool accepts every reference of an item as an attached image and that the generated
native file is on disk where Python can read it. Only if all three are true, write `{s}/smoke.json`:
`{{"image_generated": true, "all_queue_references_attached": true, "native_file_accessible": true, "note": "..."}}`
and rerun the preflight with `--smoke-file {s}/smoke.json`. If the tool cannot take every listed
reference, STOP and report a capability blocker. Never generate without them.

## 3. Generate the queued items ({q['phase']} phase, {q['count']} items)

{ids}

Image model: GPT Image 2.5 Sunburst if the image tool offers it (owner request), otherwise the default; record the
exact model name shown with `save --model`. Size: the listed size is the minimum and fixes the aspect, so request
the largest size the tool offers at that aspect. Art direction (owner, 2026-10-11): gritty old-school black-and-white
ink, with bold rough brush contours, heavy solid blacks, scratchy hatching and dry-brush texture, high contrast and
visible human marks. Pure black ink only: no grey wash, stipple fields or uniform machine texture; the attached owner
samples set the target.

For each item follow `{SKILL_DIR}/SKILL.md` and `references/WORK_OPERATIONS.md` exactly: `show ID`; the
verbatim prompt; only the listed references; save the native file as `{s}/<ID>_aN.png`; `check ID FILE`;
inspect the native image and print-size preview beside the references; `fidelity_gate.py create ... --out
{s}/<ID>.qa.json`; complete all ten criteria with real evidence; `save ID FILE --qa-file {s}/<ID>.qa.json
--must ... --avoid-clear`. Retries follow `references/REPAIR.md` within the attempt budget. Keep every native file
byte-identical.

## 4. Deliver a review ZIP and stop

```
{h} sheet --refs --out {s}/sheet.jpg
python {SCRIPTS}/style_audit.py --repo . --limit 10 --out {s}/style.json
{h} bundle --out /mnt/data/Heraldry_Work_Review_{q['phase']}.zip --evidence {s}/sheet.jpg --evidence {s}/style.json --evidence {s}/smoke.json
{h} status
```

`delivery_guard.py` does not apply here (it needs a Git checkout). The bundle carries the native images,
`receipts_append.jsonl`, every QA report, your evidence and a hash manifest. Give it to the owner as a
downloadable file and state plainly: nothing was pushed to GitHub; nothing is approved. Bundle at least every
{q.get('push_every', 5)} saved images (the review bundle should stay under GitHub's 25 MB browser upload). Continue
until `status` says NOTHING LEFT (anchors phase: stop after the anchors). Claude Code reviews independently.
"""


def build_blobs(allow_dirty=False):
    q, files = contents()
    if not shutil.which("git") or not (ROOT / ".git").exists():
        raise SystemExit("build from the repository checkout: the manifest needs the source commit")
    dirty = git("status", "--porcelain", "--untracked-files=all", "--", *files)
    if dirty and not allow_dirty:
        raise SystemExit("package inputs differ from the last commit; commit them first so the source commit is exact:\n" + dirty)
    src = {"repository": "xjordont/Heraldry", "branch": "main", "commit": git("rev-parse", "HEAD"),
           "commit_date": git("show", "-s", "--format=%cI", "HEAD"), "dirty": bool(dirty)}
    refs = {}
    for it in q["items"]:
        text = files[it["prompt"]][0].decode("utf-8")
        if prompt_sha(text) != it["prompt_sha256"]:
            raise SystemExit(f"{it['prompt']} does not match its queue prompt_sha256")
        for r in it["references"]:
            if r not in refs:
                fmt, px = decode(files[r][0], r)
                refs[r] = {"path": r, "sha256": sha(files[r][0]), "format": fmt, "px": px, "used_by": []}
            refs[r]["used_by"].append(it["id"])
    import art_skill_build                                # the installable skill zip, built from the same commit
    blobs = {rel: b for rel, (b, _) in files.items()}
    blobs[SKILL_ZIP] = art_skill_build.zip_bytes()
    blobs["START_HERE.md"] = start_here(q, src).encode()
    roles = {rel: role for rel, (_, role) in files.items()}
    roles.update({SKILL_ZIP: "skill_zip", "START_HERE.md": "instructions"})
    manifest = {
        "schema": 1, "kind": KIND, "skill_version": "7.0.0", "created_from": src,
        "source": {k: src[k] for k in ("repository", "branch", "commit", "commit_date")},
        "queue": {"path": QUEUE, "sha256": sha(blobs[QUEUE]), "phase": q["phase"], "count": q["count"], "ids": [i["id"] for i in q["items"]],
                  "generated_at": q["generated_at"]},
        "prompts": [{"id": i["id"], "path": i["prompt"], "prompt_sha256": i["prompt_sha256"], "verified_against_queue": True,
                     "max_attempts": i["max_attempts"], "references": i["references"]} for i in q["items"]],
        "references": list(refs.values()),
        "files": [{"path": rel, "sha256": sha(b), "bytes": len(b), "role": roles[rel],
                   **({"mutable": "append_only"} if rel.endswith("RECEIPTS.jsonl") else {})} for rel, b in sorted(blobs.items())],
        "excluded": ["references/private/** (owner reference PDFs and every other book)", "all art not listed by the queue",
                     "manuscript, layout, figures and build outputs"],
        "delivery": {"route": "bundle", "git_remote_access": "not provided: the package carries no credentials and cannot push",
                     "authenticated_git_lfs": "separate capability: only a real authenticated checkout can use delivery_guard.py ship"},
        "not_certified": ["image tool accepts every listed reference as an attached image (Work smoke test)",
                          "native output file accessible to Python inside Work (Work smoke test)", "artistic quality: independent review"],
    }
    blobs["WORK_PACKAGE.json"] = (json.dumps(manifest, indent=1, ensure_ascii=False) + "\n").encode()
    return q, blobs


def write_zip(path, blobs):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(blobs):
            zi = zipfile.ZipInfo(rel, STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o755 if rel.startswith(SCRIPTS + "/") else 0o644) << 16
            z.writestr(zi, blobs[rel])


def cmd_build(a):
    q, blobs = build_blobs(a.allow_dirty)
    out = Path(a.out) if a.out else OUT_DIR / f"Heraldry_Work_Input_{q['phase']}.zip"
    write_zip(out, blobs)
    side = out.with_name("WORK_PACKAGE.json")
    side.write_bytes(blobs["WORK_PACKAGE.json"])
    man = json.loads(blobs["WORK_PACKAGE.json"])
    print(json.dumps({"zip": str(out), "sha256": sha(out.read_bytes()), "bytes": out.stat().st_size, "files": len(blobs),
                      "source_commit": man["source"]["commit"], "phase": q["phase"], "items": man["queue"]["ids"],
                      "references": [{"path": r["path"], "format": r["format"], "px": r["px"]} for r in man["references"]]}, indent=1))
    return 0


def safe_extract(zpath, dest):
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            p = Path(n)
            if p.is_absolute() or ".." in p.parts:
                raise SystemExit(f"unsafe path in zip: {n}")
        z.extractall(dest)
        return z.namelist()


def offline_env(home):
    """An environment in which git has no credentials, config or prompts: what Work's shell looks like."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "GH_", "GITHUB_")) and k not in ("SSH_AUTH_SOCK",)}
    env.update({"HOME": str(home), "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
                "GIT_ASKPASS": "/bin/false", "HERALDRY_SCRATCH": str(home / "scratch"), "PYTHONDONTWRITEBYTECODE": "1"})
    return env


def verify(zpath, run_tools=True):
    report = {"zip": str(zpath), "sha256": sha(Path(zpath).read_bytes()), "checks": [], "errors": []}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pkg = tmp / "package"
        names = safe_extract(zpath, pkg)
        man = json.loads((pkg / "WORK_PACKAGE.json").read_text(encoding="utf-8"))
        listed = {f["path"]: f for f in man["files"]}
        extra = sorted(set(names) - set(listed) - {"WORK_PACKAGE.json"})
        missing = sorted(set(listed) - set(names))
        if extra or missing:
            report["errors"].append(f"zip members differ from manifest: extra {extra}, missing {missing}")
        for rel, f in listed.items():
            b = (pkg / rel).read_bytes() if (pkg / rel).is_file() else b""
            if sha(b) != f["sha256"] or len(b) != f["bytes"]:
                report["errors"].append(f"hash mismatch: {rel}")
        report["checks"].append(f"{len(listed)} files match their SHA-256 and size")
        if any(n.lower().endswith(".pdf") or n.startswith("references/") for n in names):
            report["errors"].append("private reference material present")
        report["checks"].append("no PDFs and no references/ material")
        q = json.loads((pkg / QUEUE).read_text(encoding="utf-8"))
        if sha((pkg / QUEUE).read_bytes()) != man["queue"]["sha256"]:
            report["errors"].append("queue hash differs from manifest")
        for it in q["items"]:
            if prompt_sha((pkg / it["prompt"]).read_text(encoding="utf-8")) != it["prompt_sha256"]:
                report["errors"].append(f"prompt hash mismatch: {it['id']}")
        report["checks"].append(f"{len(q['items'])} prompt files match QUEUE.json prompt_sha256")
        refs = sorted({r for it in q["items"] for r in it["references"]})
        for r in refs:
            try:
                fmt, px = decode((pkg / r).read_bytes(), r)
                report["checks"].append(f"reference decodes: {r} {fmt} {px[0]}x{px[1]}")
            except BaseException as e:      # noqa: BLE001 - decode raises SystemExit for pointers
                report["errors"].append(f"reference does not decode: {r} ({e})")
        report["source_commit"] = man["source"]["commit"]
        report["phase"], report["items"] = man["queue"]["phase"], man["queue"]["ids"]
        if run_tools:
            home = tmp / "home"
            (home / "scratch").mkdir(parents=True)
            env = offline_env(home)
            for label, args in (("work_preflight --offline-package --require-installed", [f"{SCRIPTS}/work_preflight.py", "--repo", ".", "--offline-package", "--require-installed"]),
                                ("heraldry_art doctor", [f"{SCRIPTS}/heraldry_art.py", "doctor"]),
                                ("heraldry_art status", [f"{SCRIPTS}/heraldry_art.py", "status"]),
                                ("delivery_guard audit (must refuse: no Git)", [f"{SCRIPTS}/delivery_guard.py", "audit", "--repo", "."])):
                r = subprocess.run([sys.executable, *args], cwd=pkg, env=env, capture_output=True, text=True, timeout=300)
                report.setdefault("tools", {})[label] = {"exit": r.returncode, "stdout": r.stdout.strip()[-1500:], "stderr": r.stderr.strip()[-800:]}
            pre = json.loads(report["tools"]["work_preflight --offline-package --require-installed"]["stdout"])
            if pre["status"] != "READY" or pre["delivery"] != "bundle" or pre["git"] or pre["origin_main_access"]:
                report["errors"].append("offline preflight did not report READY / bundle / no git / no remote access")
            if report["tools"]["heraldry_art doctor"]["exit"] != 0:
                report["errors"].append("helper doctor is not ready in the offline package")
            if report["tools"]["delivery_guard audit (must refuse: no Git)"]["exit"] == 0:
                report["errors"].append("delivery_guard claimed it could deliver from an offline package")
            if any(p.suffix == ".pyc" or p.name == "__pycache__" for p in pkg.rglob("*")):
                pass  # bytecode writing is disabled in the environment; nothing to report
    report["status"] = "PASS" if not report["errors"] else "FAIL"
    return report


def cmd_verify(a):
    r = verify(a.zip, not a.no_run)
    print(json.dumps(r, indent=1))
    return 0 if r["status"] == "PASS" else 1


def verify_bundle(bpath, root=ROOT):
    """Check a Work review bundle against this repository. Approves nothing."""
    sys.path.insert(0, str(root / SCRIPTS))
    import fidelity_gate as fg
    errors, notes = [], []
    q = json.loads((root / QUEUE).read_text(encoding="utf-8"))
    byid = {it["id"]: it for it in q["items"]}
    with zipfile.ZipFile(bpath) as z:
        names = set(z.namelist())
        for n in names:
            if Path(n).is_absolute() or ".." in Path(n).parts:
                return {"status": "FAIL", "errors": [f"unsafe path {n}"]}
        man = json.loads(z.read("BUNDLE_MANIFEST.json"))
        if man.get("kind") != "heraldry-work-review-bundle":
            errors.append("not a Heraldry Work review bundle")
        if man.get("pushed_to_github") is not False:
            errors.append("bundle manifest does not state that nothing was pushed")
        for rel, f in man.get("files", {}).items():
            if rel not in names or sha(z.read(rel)) != f["sha256"]:
                errors.append(f"bundle file missing or changed: {rel}")
        extra = names - set(man.get("files", {})) - {"BUNDLE_MANIFEST.json"}
        if extra:
            errors.append(f"unlisted files in bundle: {sorted(extra)}")
        if man.get("queue", {}).get("sha256") != sha((root / QUEUE).read_bytes()):
            notes.append("the bundle was made against a different QUEUE.json than this checkout's")
        receipts = {}
        for line in z.read("receipts_append.jsonl").decode().splitlines():
            if line.strip():
                r = json.loads(line)
                receipts[r["id"]] = r
        with tempfile.TemporaryDirectory() as tmp:
            for it in man.get("items", []):
                iid = it["id"]
                if iid not in byid:
                    errors.append(f"{iid} is not in the current queue")
                    continue
                img = Path(tmp) / Path(it["file"]).name
                img.write_bytes(z.read(it["file"]))
                rec = receipts.get(iid) or {}
                if rec.get("native_sha256") != sha(img.read_bytes()):
                    errors.append(f"{iid}: receipt native_sha256 differs from the image")
                if rec.get("prompt_sha256") != byid[iid]["prompt_sha256"]:
                    errors.append(f"{iid}: receipt prompt hash differs from the queue")
                want = [sha((root / r).read_bytes()) for r in byid[iid]["references"]]
                if rec.get("reference_shas") != want:
                    errors.append(f"{iid}: reference hashes differ from this repository's references")
                qa_bytes = z.read(it["qa_report"])
                if sha(qa_bytes) != rec.get("qa_report_sha256"):
                    errors.append(f"{iid}: QA report differs from the one bound in the receipt")
                qa = json.loads(qa_bytes)
                # Work may record absolute paths inside its package folder; the reviewer checks this repo's copies.
                for ref, want_path in zip(qa.get("references_used") or [], byid[iid]["references"]):
                    got = str(ref.get("path", "")).replace("\\", "/") if isinstance(ref, dict) else ""
                    if got.endswith("/" + want_path):
                        ref["path"] = want_path
                cwd = os.getcwd()
                try:
                    os.chdir(root)              # QA reference paths are repository-relative
                    errs = fg.verify_record(qa, img, byid[iid], require_pass=not rec.get("accepted_flags"))
                finally:
                    os.chdir(cwd)
                errors += [f"{iid}: QA {e}" for e in errs]
                notes.append(f"{iid}: {it['px'][0]}x{it['px'][1]} (queue {byid[iid]['size']}), {it.get('variants_tried')} attempt(s), "
                             f"failed criteria {it.get('qa_failed_criteria') or 'none'}{', ACCEPTED WITH FLAGS' if rec.get('accepted_flags') else ''}")
    return {"status": "PASS" if not errors else "FAIL", "source": man.get("source"), "items": [i["id"] for i in man.get("items", [])],
            "refusals": man.get("refusals", []), "errors": errors, "notes": notes,
            "next": "Visually review every image before tools/art_intake.py; this check approves nothing."}


def import_bundle(bpath, root=ROOT):
    r = verify_bundle(bpath, root)
    if r["status"] != "PASS":
        return r
    receipts = root / "production/art/gpt/RECEIPTS.jsonl"
    have = set(receipts.read_text(encoding="utf-8").splitlines()) if receipts.is_file() else set()
    with zipfile.ZipFile(bpath) as z:
        man = json.loads(z.read("BUNDLE_MANIFEST.json"))
        images = []
        for it in man["items"]:
            data = z.read(it["file"])
            if sha(data) != it["sha256"] or not it["file"].startswith("assets/art/incoming/"):
                return {"status": "FAIL", "errors": [f"refusing {it['file']}"]}
            dest = root / it["file"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            for old in dest.parent.glob(it["id"] + ".*"):      # one file per ID
                if old != dest:
                    old.unlink()
            dest.write_bytes(data)
            images.append(it["file"])
        new = [l for l in z.read("receipts_append.jsonl").decode("utf-8").splitlines() if l.strip() and l not in have]
    if new:
        text = receipts.read_text(encoding="utf-8") if receipts.is_file() else ""
        receipts.write_text(text + ("" if not text or text.endswith("\n") else "\n") + "\n".join(new) + "\n", encoding="utf-8")
    r.update(imported=images, receipts_added=len(new), bundle_sha256=sha(Path(bpath).read_bytes()))
    return r


def cmd_import_bundle(a):
    r = import_bundle(a.bundle)
    print(json.dumps(r, indent=1))
    return 0 if r["status"] == "PASS" else 1


def cmd_verify_bundle(a):
    r = verify_bundle(a.bundle)
    print(json.dumps(r, indent=1))
    return 0 if r["status"] == "PASS" else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--out")
    p.add_argument("--allow-dirty", action="store_true", help="tests only: build from uncommitted inputs (recorded in the manifest)")
    p = sub.add_parser("verify")
    p.add_argument("zip")
    p.add_argument("--no-run", action="store_true")
    p = sub.add_parser("verify-bundle")
    p.add_argument("bundle")
    p = sub.add_parser("import-bundle")
    p.add_argument("bundle")
    a = ap.parse_args(argv)
    return {"build": cmd_build, "verify": cmd_verify, "verify-bundle": cmd_verify_bundle,
            "import-bundle": cmd_import_bundle}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
