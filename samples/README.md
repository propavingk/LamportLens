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
