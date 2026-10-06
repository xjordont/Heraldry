# One-command clean build: make clean all verify package
PY ?= python3
VERSION = $(shell $(PY) tools/manuscript.py --version)
DIST := dist
B := build

.NOTPARALLEL:
.PHONY: all deps fonts parse figures book release-files print print-white digital covers calibration specimen verify package clean test
all: release-files

deps:
	$(PY) -m pip install -r requirements.lock
fonts:
	$(PY) tools/make_fonts.py
parse:
	$(PY) tools/preflight.py --report production/preflight.json
	$(PY) tools/parse_source.py
	$(PY) tools/make_index.py
	$(PY) tools/build_extras.py
figures: parse
	$(PY) figures/src/make_figures.py
book: figures
	$(PY) tools/build_book.py --passes 8
	$(PY) tools/build_book.py --variants-only
release-files: book
	mkdir -p $(DIST)
	cp $(B)/book-cream.pdf $(DIST)/Heraldry_$(VERSION)_inkjet-borderless.pdf
	cp $(B)/book-white.pdf $(DIST)/Heraldry_$(VERSION)_inkjet-borderless-white.pdf
	cp $(B)/book-digital.pdf $(DIST)/Heraldry_$(VERSION)_digital.pdf
	cp $(B)/covers-cream.pdf $(DIST)/Heraldry_$(VERSION)_covers-front-back.pdf
	cp $(B)/covers-white.pdf $(DIST)/Heraldry_$(VERSION)_covers-front-back-white.pdf
	cp $(B)/calibration.pdf $(DIST)/Heraldry_$(VERSION)_inkjet-calibration.pdf
	$(PY) tools/provenance.py
print print-white digital covers calibration: release-files
verify:
	$(PY) tools/verify.py
# Table specimen targets use the freshly verified table page map.
specimen: verify
	$(PY) tools/specimen.py
package: specimen
	$(PY) tools/package.py
test:
	$(PY) -m unittest discover -s tests -v
clean:
	rm -rf $(B) typst/content.typ
