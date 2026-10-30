# Borderless US Letter inkjet output

The primary physical output is home inkjet printing in borderless mode on US Letter sheets. This replaces the older generic non-bleed/commercial-printer default. The file can be finished without a named printer; physical reproduction must still be proved on the actual printer/media/driver.

## File contract

- Every interior page is a single portrait 612 × 792 pt page (8.5 × 11 inches), rotation 0. No landscape inserts, spreads, booklet imposition, external bleed allowance, crop marks, registration marks, or printer furniture.
- MediaBox and CropBox must equal the full Letter sheet. Use matching TrimBox/BleedBox when present; never enlarge the exported sheet to 8.75 × 11.25 inches for this mode. A separately commissioned commercial edition may use a separate profile later.
- Paint the selected background to all four page edges with a page background layer. The default is almost-white warm cream `#FCFAF5`; parchment means a restrained flat tone, not a raster scan of aged paper. The paper-white variant uses the same geometry and pagination, with the substrate changed to `#FFFFFF` for cream stock or lower ink use. Both variants are borderless documents.
- Backgrounds and expendable art may meet the sheet edge. Essential text, folios, headers, table keys, figure labels, and important diagram geometry stay at least 0.375 inch (27 pt) inside every edge; the larger configured body margins and binding gutter still apply. Borderless is not zero text margins.
- All essential type is at least 9 pt. Use true black for essential text and monochrome line art; retain the light warm background in the cream edition. Do not convert the entire cream PDF to grayscale and silently remove the requested warmth. Do not use rich multi-ink black for fine text or invent a printer ICC profile.
- Preserve vector/searchable text, embedded fonts, sharp vector diagrams, and effective-resolution evidence for raster artwork. Keep background colour separate from content styling so cream and white exports remain identical in layout.
- A home inkjet PDF does not require PDF/X unless a separately supplied specification says so. Avoid unnecessary conformance conversion that changes appearance, links, or page boxes.

## Borderless expansion and proof

Borderless drivers may enlarge and clip the file. Support varies by model, media, paper source, and driver. Do not assume an overscan amount or that automatic duplex is compatible. Use the actual device's current manual when its model is supplied.

Produce `dist/Heraldry_RC###_inkjet-calibration.pdf`: one diagnostic Letter page with a 1-inch square/ruler, inset distance markers at 0.125/0.25/0.375/0.5 inch, diagnostic 9/9.5-pt type, the active body and table sizes, the configured essential minimum, 0.6/0.75/1-pt rules, light table bands, a cream/white comparison, and representative hatch detail. Type labels derive from the active Typst values: currently 10.5 pt body and 9 pt table text. Include an unchanged paragraph from the current manuscript at body size and a current table-header sample. The calibration source asserts that its manuscript excerpt resolves exactly once. Older `config/design_tokens.json` and `config/production.json` format starting values do not override the active `typst/templates/system.typ` and `typst/heraldry.typ` design. These diagnostic marks never enter the reader edition. Include relevant dense specimen pages for a small first print batch. This calibration file is excluded from book-wide essential-edge checks because its diagnostic edge marks intentionally violate those margins.

In `dist/PRINT_INSTRUCTIONS.md`, instruct the user to select Letter portrait, one PDF page per sheet, borderless on, and actual size/100% at the application level (no Fit/Shrink or additional scale). Let the supported driver control expansion; start at its lowest amount that yields acceptable edge coverage and adjust from the physical proof. A driver may enlarge even when the application says 100%. Select a supported media/source and the quality appropriate to the stock; never claim one driver setting fits every model. Test duplex/flip direction on a small batch if double-sided printing is wanted, using manual duplex if necessary.

As an internal stress test, centre-scale representative pages by 1.03 and clip to 612 × 792 pt. Review text and significant figure geometry after cropping. This is a deliberately conservative design scenario, not measured printer behaviour. Deliver the untouched 612 × 792 pt master, not the enlarged test render; avoid scaling twice.

Report `inkjet_file_preflight` independently from `physical_inkjet_proof`. The former can PASS from file evidence; the latter is NOT TESTED until an actual printed proof has been inspected. Physical proof is not a blocker to completing the file. Report a commercial cover wrap/PDF-X check as NOT APPLICABLE unless that additional output is requested. Complete Letter-size front/back cover sheets; no guessed spine or mandatory wrap-template hunt.

## Runnable file check

After installing and locking PyMuPDF, run:

```sh
python3 tools/verify_inkjet_pdf.py dist/Heraldry_RC###_inkjet-borderless.pdf --report build/checks/inkjet-preflight.json
```

The checker covers portrait geometry/boxes, referenced font embedding, minimum type size, text edge safety, and simulated text overscan. Its PASS does not certify source fidelity, background paint, vector-only figures, raster resolution, artwork, all-page visual quality, print marks, or the physical printer. Those require the production evidence and visual gates. The standalone command writes an ignored local report; the requested release pipeline writes its bound report to `production/qa/inkjet-preflight.json`.

Official references checked 2026-10-06:

- https://support2.epson.net/manuals/english/lfp/styluspro38803885/ug/html/print_4.htm — example manufacturer documentation explaining enlargement/cropping and borderless modes; not identification of the user's printer or a universal setting.
- https://code.claude.com/docs/en/cloud-environments — runtime, network and checkpoint considerations for producing the files.

Output names use the active RC number from source/versions.json; replace RC### in command examples with that number.
