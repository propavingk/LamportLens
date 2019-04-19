# Sample fixtures

Every file here is a synthetic test vector. None of it was captured from a
live cluster. `build_fixture.py` rebuilds `clean-snapshot.jsonl` and
`snapshot.jsonl` byte for byte, so the construction is inspectable and
reproducible:

```bash
python samples/build_fixture.py
clean-snapshot.jsonl: 12 records
snapshot.jsonl: 44 records
```

Program ids that appear are real, well-known Solana addresses: the system
program, SPL token, token-2022, the associated token program, and the BPF
upgradeable loader. Account addresses are clearly patterned fakes built from
the string `FixTure` plus an index; no real account is represented.

## clean-snapshot.jsonl

12 records. Ten SPL token accounts of 165 bytes holding 2,500,000 lamports
each, one zero-byte system account holding 9,000,000 lamports, and one
executable program account. Everything non-executable is comfortably above
its minimum at the default rate, so the audit reports zero findings and the
exit code is 0. This fixture exists to show what a healthy snapshot looks
like, and to give the CLI an exit-0 case.
