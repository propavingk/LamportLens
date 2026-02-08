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

## snapshot.jsonl

44 records built to exercise every status at the default rate of 6,333
lamports per byte:

| Group | Count | What it exercises |
|---|---|---|
| token accounts at 2,039,280 lamports | 10 | funded under the current rate, exactly at the historical minimum |
| token accounts at exactly the current minimum (1,855,569) | 5 | at-minimum |
| token account 1,000 lamports above the minimum | 1 | barely-above |
| token account at 1,600,000 and 1,200,000 | 2 | underfunded |
| zero-byte accounts at 890,880, at 810,624, and at 700,000 | 3 | funded, at-minimum, underfunded respectively |
| a 1 MB mint account and a 2.5 MB program data account | 2 | the large end of the bands |
| mid-size accounts in the 100-999 and 1k-9.9k bands | 16 | band coverage, balances computed to stay funded |
| executable programs | 2 | the excluded bucket |
| assorted small accounts | 3 | owner spread |

Expected result: 3 underfunded accounts with deficits 255,569, 655,569 and
110,624 lamports, a total deficit of 1,021,762, 7 at-minimum accounts, and
findings equal to 3. Exit code 1.

## broken-lines.jsonl

Nine lines, seven of them deliberately invalid, covering every validation
rule: invalid JSON, missing address, negative lamports, a data length above
10 MiB, missing owner, a string lamports value, and a non-boolean executable
flag. Two valid records surround the bad lines to prove that parsing
continues. Expected result: 2 records and 7 parse errors, exit code 1.

## Why synthetic

Producing an honest fixture with exactly these status counts requires either
a real snapshot that happens to contain the boundary cases (possible, but not
reproducible or shareable) or a constructed vector. Constructed vectors are
labelled as such here rather than presented as captured data. If you have a
real capture, the tool reads it; the format is documented in
`docs/FORMAT.md`.
