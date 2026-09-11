## What this changes

## Why

## Checklist

- [ ] `PYTHONPATH=src python -m unittest discover -s tests -v` passes
- [ ] `cd verifier && npm run typecheck && npm run build && npm test` passes
- [ ] `python scripts/parity.py` reports every fixture agreeing (required if any rule changed)
- [ ] `python scripts/verify.py` exits 0
- [ ] Report shape changes: real `audit` output pasted above
- [ ] `docs/FORMAT.md` updated if a field, rule or exit code changed
- [ ] Rate table in `docs/RATE_SCHEDULE.md` updated if a new SIMD step was added
