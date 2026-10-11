# Work review bundle inbox (fallback route)

ChatGPT Work cannot upload Git LFS objects. Commit its review bundle ZIP here as an ordinary file. The `Import Work review bundle` workflow:
- verifies the bundle;
- commits its images to `assets/art/incoming/` through Git LFS;
- appends its receipts and runs the intake;
- records the bundle's hash in `../IMPORTED.json`;
- removes the ZIP from this folder.

The ZIP stays in Git history only. Nothing is approved here. See `docs/LARGE_FILES.md`.
