.PHONY: help test verify run parity clean

PYTHON ?= python
export PYTHONPATH := src

help:
	@echo "lamportlens targets:"
	@echo "  make test     run the Python tests and the TypeScript verifier tests"
