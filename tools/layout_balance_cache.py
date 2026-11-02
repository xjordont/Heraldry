"""Persist converged balance hints, never measurements or publication approval.

Call after validated measurement evidence is available. A hint only seeds the
normal Book signature checks and balancing loop: recomputation and every PDF
warning, source-keep, and publication gate remain mandatory.
"""
import hashlib
import json
import logging
import re
import tempfile
from pathlib import Path

SCHEMA = 1
CACHE_DIRECTORY = ".cache/layout-measurements"
LOG = logging.getLogger(__name__)
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SEGMENT = re.compile(r"(?:0|[1-9][0-9]*)\Z")
# V2 binds rendered pieces and the complete layout profile. Legacy ID/count
# signatures cannot establish that edited text has the same segment geometry.
SIGNATURE = re.compile(r"v2:[0-9a-f]{64}\Z")


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value):
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def _identity(value):
    return (isinstance(value, dict) and type(value.get("schema")) is int and value["schema"] == 1
            and all(_sha(value.get(k)) for k in ("content_sha256", "input_sha256"))
            and value.get("variant") == "cream" and value.get("edition") == "interior"
            and isinstance(value.get("compiler"), str) and bool(value["compiler"])
            and type(value.get("timestamp")) is int and value["timestamp"] >= 0)


def _balance(value):
    if not isinstance(value, dict):
        raise ValueError("Balance hint is not a dictionary")
    normalized = {}
    for key, entry in value.items():
        if not isinstance(key, str) or SEGMENT.fullmatch(key) is None:
            raise ValueError("Balance hint has a nonnumeric segment key")
        if (not isinstance(entry, (list, tuple)) or len(entry) != 2
                or not isinstance(entry[0], str) or SIGNATURE.fullmatch(entry[0]) is None
                or type(entry[1]) is not int or entry[1] < 0):
            raise ValueError("Balance hint has an invalid signature/piece index")
        normalized[key] = [entry[0], entry[1]]
    return normalized


def _context(root, binding):
    """Match the supplied exact-PDF evidence against its measurement entry.

    The measurement caller owns current-input validation. This module neither
    imports a compiler nor independently compiles or rebinds measured heights.
    """
    if (not isinstance(binding, dict) or binding.get("origin") != "measurement-pdf-attachment"
            or binding.get("warnings") != [] or not _identity(binding.get("identity"))):
        raise ValueError("Missing complete warning-free measurement identity")
    cache = binding.get("cache")
    if not isinstance(cache, dict) or cache.get("status") not in ("hit", "miss") or not _sha(cache.get("key")):
        raise ValueError("Measurement caching disabled or cache key invalid")
    if not all(_sha(binding.get(k)) for k in ("measurement_pdf_sha256", "measurements_sha256")):
        raise ValueError("Missing exact measurement PDF/attachment digests")
    entry = Path(root) / CACHE_DIRECTORY / cache["key"]
    envelope = json.loads((entry / "evidence.json").read_bytes())
    if (not isinstance(envelope, dict) or type(envelope.get("schema")) is not int
            or envelope["schema"] != SCHEMA or envelope.get("key") != cache["key"]):
        raise ValueError("Measurement cache envelope/key mismatch")
    evidence = envelope.get("evidence")
    if not isinstance(evidence, dict) or any(evidence.get(k) != binding.get(k) for k in (
            "origin", "identity", "warnings", "measurement_pdf_sha256", "measurements_sha256", "units")):
        raise ValueError("Measurement entry does not match complete supplied evidence")
    if hashlib.sha256((entry / "measurement.pdf").read_bytes()).hexdigest() != binding["measurement_pdf_sha256"]:
        raise ValueError("Measurement PDF no longer matches its bound SHA")
    return entry, cache["key"]


def _diagnostic(status, reason, *, diagnostics=None, **extra):
    result = {"status": status, "reason": reason, **extra}
    if diagnostics is not None:
        diagnostics.append(result)
    LOG.info("Layout balance cache %s: %s", status, reason)
    return result


def load_hint(root, measurement_binding, *, diagnostics=None):
    """Return a validated starting plan or {}; optional diagnostics is a list."""
    try:
        entry, key = _context(root, measurement_binding)
        payload = json.loads((entry / "balance.json").read_bytes())
        if (not isinstance(payload, dict) or type(payload.get("schema")) is not int
                or payload["schema"] != SCHEMA or payload.get("key") != key
                or payload.get("converged") is not True):
            raise ValueError("Invalid balance envelope/key or unconverged plan")
        if any(payload.get(k) != measurement_binding.get(k) for k in (
                "identity", "measurement_pdf_sha256", "measurements_sha256")):
            raise ValueError("Balance hint does not match complete measurement identity")
        digest = payload.get("hint_sha256")
        unsigned = {k: v for k, v in payload.items() if k != "hint_sha256"}
        if not _sha(digest) or hashlib.sha256(_canonical(unsigned)).hexdigest() != digest:
            raise ValueError("Balance hint digest mismatch")
        balance = _balance(payload.get("balance"))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        _diagnostic("miss", str(error), diagnostics=diagnostics)
        return {}
    _diagnostic("hit", "validated starting hint; recomputation required", diagnostics=diagnostics,
                key=key, path=(entry / "balance.json").as_posix(), segments=len(balance))
    return balance


def save_hint(root, measurement_binding, balance, *, converged=True, warnings=()):
    """Save only an actual converged plan; return a nonfatal diagnostic status.

    Call only after the normal compile/recompute loop succeeds. The optional
    guards also let callers explicitly pass failed convergence or diagnostics;
    neither failed nor warning-bearing plans may replace an existing hint.
    """
    if converged is not True or warnings:
        return _diagnostic("skipped", "balance did not converge without warnings")
    try:
        entry, key = _context(root, measurement_binding)
        normalized = _balance(balance)
        payload = {"schema": SCHEMA, "key": key, "converged": True,
                   "identity": measurement_binding["identity"],
                   "measurement_pdf_sha256": measurement_binding["measurement_pdf_sha256"],
                   "measurements_sha256": measurement_binding["measurements_sha256"],
                   "balance": normalized}
        payload["hint_sha256"] = hashlib.sha256(_canonical(payload)).hexdigest()
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        return _diagnostic("skipped", str(error))
    target = entry / "balance.json"
    try:
        with tempfile.TemporaryDirectory(prefix=".balance-", dir=entry) as temporary:
            scratch = Path(temporary) / "balance.json"
            scratch.write_bytes(_canonical(payload) + b"\n")
            scratch.replace(target)
    except OSError as error:
        return _diagnostic("error", str(error), key=key, path=target.as_posix())
    return _diagnostic("stored", "converged starting hint saved; recomputation remains required",
                       key=key, path=target.as_posix(), segments=len(normalized))
