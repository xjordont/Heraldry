# HERALDRY SKIRMISH RC484 — reproducible publication build.
# One-command clean build:  make clean all verify package
PY ?= python3
DIST := dist
B := build

.PHONY: all deps fonts parse figures book print print-white digital covers calibration specimen verify package clean

all: print print-white digital covers calibration specimen

deps:
	$(PY) -m pip install --break-system-packages -r requirements.lock

fonts:
	$(PY) tools/make_fonts.py

parse:
	$(PY) tools/preflight.py --report production/preflight.json
	$(PY) tools/parse_source.py
	$(PY) tools/make_index.py
	$(PY) tools/build_extras.py

figures:
	$(PY) figures/src/make_figures.py

# balancing/convergence loop over the cream interior, then white + digital from the same layout
book: parse figures
	$(PY) tools/build_book.py --passes 8
	$(PY) tools/build_book.py --variants-only

print: book
	mkdir -p $(DIST)
	cp $(B)/book-cream.pdf $(DIST)/Heraldry_RC484_inkjet-borderless.pdf

print-white: book
	mkdir -p $(DIST)
	cp $(B)/book-white.pdf $(DIST)/Heraldry_RC484_inkjet-borderless-white.pdf

digital: book
	mkdir -p $(DIST)
	cp $(B)/book-digital.pdf $(DIST)/Heraldry_RC484_digital.pdf

covers calibration: parse
	mkdir -p $(DIST)
	cp $(B)/covers-cream.pdf $(DIST)/Heraldry_RC484_covers-front-back.pdf
	cp $(B)/covers-white.pdf $(DIST)/Heraldry_RC484_covers-front-back-white.pdf
	cp $(B)/calibration.pdf $(DIST)/Heraldry_RC484_inkjet-calibration.pdf

specimen: print
	$(PY) tools/specimen.py

verify:
	$(PY) tools/verify.py

package: verify
	$(PY) tools/package.py

clean:
	rm -rf $(B) typst/content.typ
