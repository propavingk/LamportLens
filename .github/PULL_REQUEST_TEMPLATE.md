## What this changes

## Why

## Checklist

- [ ] `PYTHONPATH=src python -m unittest discover -s tests -v` passes
- [ ] `cd verifier && npm run typecheck && npm run build && npm test` passes
- [ ] `python scripts/parity.py` reports every fixture agreeing (required if any rule changed)
- [ ] `python scripts/verify.py` exits 0
