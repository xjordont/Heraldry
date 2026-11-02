# One-command clean build: make clean all verify package
PY ?= python3
VERSION = $(shell $(PY) tools/manuscript.py --version)
DIST := dist
B := build

.NOTPARALLEL:
.PHONY: all deps doctor check status fonts parse figures book release-files digital specimen verify package clean test art-packages
all: release-files

deps:
	$(PY) -m pip install -r requirements.lock
doctor check status:
	$(PY) tools/dev.py $@ --python $(PY)
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
	cp $(B)/book-digital.pdf $(DIST)/Heraldry_$(VERSION)_digital.pdf
	$(PY) tools/digital_compact.py $(DIST)/Heraldry_$(VERSION)_digital.pdf $(DIST)/Heraldry_$(VERSION)_digital-compact.pdf --report production/qa/digital-compact.json
	$(PY) tools/provenance.py
digital: release-files
verify:
	$(PY) tools/verify.py
# Table specimen targets use the freshly verified table page map.
specimen: verify
	$(PY) tools/specimen.py
package: specimen
	$(PY) tools/package.py
# Both suites (tests/ and the art skill's), one module per process in parallel: same tests, same result.
test:
	$(PY) tools/run_tests.py
# Installable skill zip and offline Work input package, built on request into build/art/ (never committed).
art-packages:
	$(PY) tools/art_skill_build.py
	$(PY) tools/art_work_package.py build
	$(PY) tools/art_work_package.py verify $(B)/art/Heraldry_Work_Input_$$($(PY) -c "import json;print(json.load(open('production/art/gpt/QUEUE.json'))['phase'])").zip
clean:
	rm -rf $(B) typst/content.typ
