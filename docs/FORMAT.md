# Format contract

This document specifies the input format, every validation rule, the text
report sections, the JSON report fields, the exit codes, and the deterministic
rules the audit follows. It is the contract between the two implementations in
this repository (Python in `src/lamportlens/`, TypeScript in `verifier/src/`)
and between the tool and anyone writing a snapshot for it.

## Input: one JSON object per line

The input file is JSONL. Blank lines are ignored. Every other line must decode
as a JSON object. The fields:

| Field | Type | Required | Rules |
|---|---|---|---|
| `address` | string | yes | non-empty |
| `lamports` | integer | yes | `>= 0` |
| `data_len` | integer | yes | `>= 0` and `<= 10485760` (10 MiB) |
| `owner` | string | yes | non-empty; the owning program id |
| `executable` | boolean or null | no | defaults to false |

Unknown keys are ignored. A `null` value is treated as absent for
`executable`. Types are enforced: `"lamports": "2000"` is invalid, and so is
`"executable": "yes"`. `data_len` is bounded by `MAX_ACCOUNT_DATA_LEN`
because an account larger than 10 MiB cannot exist on Solana, and a snapshot
claiming otherwise has an exporter bug.

### Validation errors

Every invalid line is collected with its line number and reported under
`PARSE ERRORS`. Parsing continues. The observed error messages are:

| Condition | Message |
|---|---|
| not a JSON object | `line N: record must be a JSON object` |
| JSON syntax error | `line N: invalid JSON (...)` |
| missing `address` | `line N: missing required field 'address'` |
| empty `address` | `line N: field 'address' must be a non-empty string` |
| missing `lamports` | `line N: missing required field 'lamports'` |
| non-integer or negative `lamports` | `line N: field 'lamports' must be an integer` / `must be >= 0` |
| `data_len` over 10 MiB | `line N: field 'data_len' must be <= 10485760` |
| missing `owner` | `line N: missing required field 'owner'` |
| non-boolean `executable` | `line N: field 'executable' must be a boolean` |

## Deterministic rules

These rules are implemented twice, once per language, and the parity script
asserts that both implementations agree on every fixture.

### The arithmetic

```
minimum = (128 + data_len) * lamports_per_byte
```

Integer only. `lamports_per_byte` is resolved by the CLI: explicit flag, then
preset, then the documented default. See `docs/RATE_SCHEDULE.md` for the
steps and their dates.

### Status classification

| Status | Condition |
|---|---|
| `executable-excluded` | the record is an executable program account; excluded from the rent comparison |
| `underfunded` | `lamports < minimum` |
| `at-minimum` | `lamports == minimum` |
| `barely-above` | `minimum < lamports <= floor(minimum * 1.01)` |
| `funded` | `lamports > floor(minimum * 1.01)` |

Executable accounts are excluded because the loader holds programs and the
account rent rule does not apply to them the same way. Counting them would
manufacture findings at scale. The ratio 1.01 exists so that an account
holding a token 1,000 lamports above its bond is not reported as fully funded
when it cannot meaningfully spend that margin.

### Aggregates

| Aggregate | Definition |
|---|---|
| `locked` | the sum of `minimum` over every non-excluded account, the total bond the snapshot represents |
| `balance` | the sum of `lamports` over every non-excluded account |
| `deficit` | for each underfunded account, `minimum - lamports`, summed |
| `reclaimable` | the sum of `lamports` over accounts whose status is `at-minimum` or `barely-above`; closing these returns the full balance, before fees |

### Bands

Data length bands, fixed edges:

| Band | `data_len` range |
|---|---|
| `0 bytes` | 0 |
| `1-99` | 1 to 99 |
| `100-999` | 100 to 999 |
| `1k-9.9k` | 1,000 to 9,999 |
| `10k-99k` | 10,000 to 99,999 |
| `100k-999k` | 100,000 to 999,999 |
| `1M and above` | 1,000,000 to 10,485,760 |

Excluded accounts are not counted in any band, so band counts sum to
`records - excluded`.

### Owner summaries

Per `owner`: account count, underfunded count, `locked` (sum of minima over
non-excluded accounts) and `balance` (sum of lamports over non-excluded
accounts). The report ranks owners by `locked` descending, then by account
count, then by owner string.

## Text report

The `audit` command prints, in order:

| Section | Content |
|---|---|
| header | tool name, input path, records, rate used, parse error count |
| `STATUS COUNTS` | one line per status in fixed order |
| `TOTALS` | locked, balances observed, underfunded deficit, reclaimable |
| `UNDERFUNDED` | the first N, largest deficit first, with owner and deficit |
| `BANDS` | every band with account count and locked lamports |
| `OWNERS` | top five by locked lamports |
| `PARSE ERRORS` | the first N error messages verbatim |
| `FINDINGS` | the total count used for the exit code |

N defaults to 10 and is set by `--limit`. Lists are never silently truncated:
a cut list always prints how many entries were omitted.

## JSON report

`audit --format json` prints one object. Field by field:

| Field | Type | Meaning |
|---|---|---|
| `input` | string | the path as given on the command line |
| `records` | int | accepted records |
| `lamports_per_byte` | int | the resolved rate |
| `findings` | int | underfunded accounts plus parse errors |
| `status_counts` | object | one key per status, in fixed order |
| `totals.locked` | int | total bond |
| `totals.balance` | int | total balance observed |
| `totals.deficit` | int | total deficit |
| `totals.reclaimable` | int | balance in at-minimum and barely-above accounts |
| `underfunded` | array | objects with `address`, `owner`, `lamports`, `minimum`, `deficit`; largest deficit first |
| `bands` | array | objects with `label`, `accounts`, `locked` |
| `owners` | object | owner id to `accounts`, `underfunded`, `locked`, `balance` |
| `parse_errors` | array | objects with `line` and `message` |

Adding keys is a minor change. Renaming or removing a key needs a changelog
entry, because consumers diff this output in CI.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | no findings: no underfunded accounts, no parse errors |
| 1 | findings present: at least one underfunded account or parse error |
| 2 | usage error: missing or unreadable input file |

Accounts at exactly the minimum are not findings. They are exempt, which is
the state the cluster requires; they are reported under `reclaimable` because
closing them recovers the bond, not because they are wrong.

## Determinism guarantees

- Two runs over the same input produce byte-identical output.
- JSON output uses stable key order and sorted collections.
- Nothing in the output depends on wall-clock time, locale, or randomness.
- The TypeScript verifier emits the same subset of keys so
  `scripts/parity.py` can compare implementations without shared code.
