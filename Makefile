.PHONY: help test verify run parity clean

PYTHON ?= python
export PYTHONPATH := src

help:
	@echo "lamportlens targets:"
	@echo "  make test     run the Python tests and the TypeScript verifier tests"
	@echo "  make verify   run the repository quality gate (scripts/verify.py)"
	@echo "  make run      audit the snapshot sample and print the report"
	@echo "  make parity   compare Python and TypeScript on the samples"
	@echo "  make clean    remove caches and build output"

test:
	$(PYTHON) -m unittest discover -s tests -v
	cd verifier && npm test

verify:
	$(PYTHON) scripts/verify.py

run:
	$(PYTHON) -m lamportlens audit samples/snapshot.jsonl

parity:
	$(PYTHON) scripts/parity.py

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	-rm -rf verifier/dist verifier/node_modules
