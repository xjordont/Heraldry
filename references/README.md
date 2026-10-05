# Optional visual references

The mandatory design instructions live in `docs/DESIGN_SPEC.md`; the rationale and sampled observations live in `docs/REFERENCE_ANALYSIS.md`. `reference_manifest.json` identifies exact supplied file hashes and selected PDF viewer pages. Reference availability is optional and never blocks the Heraldry build.

## Default

Upload the kit's contents to the project repository. Read the design specification and execute MASTER_PROMPT.md. The distilled guidance is sufficient to begin the actual-content specimen.

## Optional visual calibration

Keep chosen source PDFs in a separate authorised reference directory. The recommended first set is BlackDeathCity, Deth Wizards, Mythras, Hametsu, Five Leagues, and Hellcrawl: 14 selected viewer pages across six unique books. Do not read entire books or copies with identical hashes.

Preview the selection without loading sources:

    python3 tools/render_reference_pages.py --plan

Render only the primary selection:

    python3 -m pip install PyMuPDF
    python3 tools/render_reference_pages.py --source-root /path/to/authorised/reference-pdfs

The output goes to `references/private/`, which is excluded from Git by default. Inspect render-status.json for availability, successful rendering, and any PDF warnings. The exact-file hash verifies that the selected page numbers refer to the inspected edition. Different editions need a new visual check and a revised manifest.

For one particular design problem, request only relevant IDs, for example:

    python3 tools/render_reference_pages.py --source-root /path/to/reference-pdfs --ids REF-CALLTOARMS REF-TNA

`--all` includes all nine manifested books and 19 selected pages. It is optional, not the default reading assignment. These reference pages are evidence, not original Heraldry assets. Keep them out of the publication PDFs and release archive. If copying excerpts into a shared or cloud project, do so only with the necessary permission; private hosting is not a substitute for that permission.

For cloud execution without reference file access, proceed with the distilled specification. If approved reference evidence is supplied through an available private channel, point Claude to its exact location and manifest ID. Give individual workers only the decisions or selected images needed for their task.

Claude Code currently documents visual image reads and PDF page-range reads using Poppler. See https://code.claude.com/docs/en/tools-reference. Verify the installed tools rather than assuming the future session has identical behaviour.
