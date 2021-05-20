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

## Python unit tests

| File | Covers |
|---|---|
| `tests/test_model.py` | every validation rule, error collection with line numbers, blank line handling, unknown key tolerance |
| `tests/test_rent.py` | formula anchors at both rates, preset values, status classification including the executable exclusion |
| `tests/test_audit.py` | designed status counts on both fixtures, deficit sum, band totals, owner summaries, reclaimable definition |
| `tests/test_cli.py` | exit codes 0, 1 and 2, JSON shape, rate override changing findings, `bands` and `owners` subcommands |

The three underfunded accounts in the snapshot fixture are deliberate and
their deficits are asserted exactly:

```
1,855,569 - 1,600,000 = 255,569
1,855,569 - 1,200,000 = 655,569
  810,624 -   700,000 = 110,624
```

