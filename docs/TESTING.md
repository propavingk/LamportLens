# Testing guide

This document maps the test suite: what each file covers, how the two
implementations are held in agreement, and how to add tests when you change
behavior.

## The shape of the suite

| Suite | Location | Command | Count |
|---|---|---|---|
| Python unit tests | `tests/` | `PYTHONPATH=src python -m unittest discover -s tests -v` | 39 |
| Verifier tests | `verifier/src/verify.test.ts` | `cd verifier && npm test` | 6 |
| Cross-engine parity | `scripts/parity.py` | `python scripts/parity.py` | 3 fixtures |
| Mechanical checks | `scripts/verify.py` | `python scripts/verify.py` | 8 checks |

`make test`, `make parity` and `make verify` wrap the same commands. CI runs
all four.

