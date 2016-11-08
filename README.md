<p align="center">
  <img src="docs/assets/banner.svg" alt="lamportlens banner: six bars for the SIMD-0437 rate steps from 6,960 down to 696, showing the rent-exempt minimum for a zero-byte account at each step, with the live 6,333 step in copper and a marker stepping down the ladder" width="640">
</p>

# LamportLens

Rent-exempt and balance hygiene for captured Solana account snapshots.

Point it at a JSONL export of accounts and it tells you which ones hold less
than the rent-exempt minimum, how much lamport bond the snapshot represents,
where that bond concentrates across data sizes, and which owners hold it. It
is offline, deterministic, and runs with nothing but the standard library.

<details>
<summary>Contents</summary>

- [Why storage bonds are the interesting number](#why-storage-bonds-are-the-interesting-number)
- [What it does](#what-it-does)
- [Quick start](#quick-start)
- [A real run: healthy snapshot](#a-real-run-healthy-snapshot)
- [A real run: snapshot with findings](#a-real-run-snapshot-with-findings)
- [Commands](#commands)
- [The input format](#the-input-format)
- [A worked walkthrough](#a-worked-walkthrough)
- [Statuses and what each one should trigger](#statuses-and-what-each-one-should-trigger)
- [Exit codes and CI integration](#exit-codes-and-ci-integration)
- [The rate is the variable](#the-rate-is-the-variable)
- [The second implementation](#the-second-implementation)
- [Design decisions](#design-decisions)
- [Repository layout](#repository-layout)
- [Tests and verification](#tests-and-verification)
- [Limitations](#limitations)
- [Glossary](#glossary)
- [The mark](#the-mark)
- [License](#license)

</details>

---

## Why storage bonds are the interesting number

Every Solana account must hold a minimum lamport balance sized to its data.
The name for that balance is rent, but the mechanism is a bond: the lamports
stay with the account and return in full when it is closed. Two operational
consequences follow, and they are what this tool exists for.

First, the bond is the floor of your program's storage economics. A token
program with fifty thousand token accounts is not paying fifty thousand fees;
it is holding fifty thousand bonds, and the size of that holding is the number
to watch.

Second, the bond is not constant. The SIMD-0437 schedule reduces
lamports per byte in steps from 6,960 toward 696, and the first step is
already live on mainnet. Accounts funded to the old bond now sit above the
new minimum, which turns part of that bond into recoverable capital. Accounts
funded below the new minimum sit in the opposite state and are the findings
this tool reports.

A snapshot is the only way to see any of this. The accounts API answers one
question at a time, and a dashboard shows today; a JSONL export answers the
whole question offline, and it diffs.

---

## What it does

- Validates every line of a snapshot and reports bad ones with line numbers
  instead of aborting.
- Computes each account's rent-exempt minimum at a chosen lamports-per-byte
  rate and classifies it: underfunded, at-minimum, barely-above, funded, or
  executable-excluded for program accounts.
- Totals the bond (`locked`), the deficit, the balances observed, and the
  lamports a closure sweep would return (`reclaimable`).
- Groups accounts into seven fixed data-length bands and ranks owners by the
  bond they hold.
- Emits a line-oriented text report or a JSON report with fixed field names.
- Cross-checks every rule with a second implementation in TypeScript. The two
  engines are compared on every fixture by `scripts/parity.py`.

<p align="center">
  <img src="docs/assets/bands.svg" alt="Seven rows, one per data length band, with bars for account counts and two numeric columns: the 1M and above band holds 22,167,121,248 lamports across 2 accounts, the 1k-9.9k band holds 125,545,392 across 8, and the 100-999 band holds 58,630,914 across 26" width="640">
</p>

The graphic is built from the actual numbers in this repository's fixture: 44
records, 3 underfunded accounts, a total bond of 22,357,719,216 lamports, and
2 executable accounts excluded from every band.

---

## Quick start

Nothing to install for the Python core:

```bash
export PYTHONPATH=src
python -m lamportlens audit samples/snapshot.jsonl
```

Or install the console script with `pip install .` and run
`lamportlens audit samples/snapshot.jsonl`.

The TypeScript verifier builds with a single dev dependency: `cd verifier &&
npm install && npm run build`, then `node dist/verify.js ../samples/snapshot.jsonl`.

---

## A real run: healthy snapshot

The clean fixture has 12 accounts, all exempt, one program account excluded.
This is the actual output, captured from the command shown:

```bash
PYTHONPATH=src python -m lamportlens audit samples/clean-snapshot.jsonl
```

```text
LAMPORTLENS REPORT
input: samples\clean-snapshot.jsonl
records: 12 | lamports per byte: 6333 | parse errors: 0

STATUS COUNTS
  underfunded: 0
  at-minimum: 0
  barely-above: 0
  funded: 11
  executable-excluded: 1

TOTALS
  locked in exemptions: 19366314
  balances observed: 34000000
  underfunded deficit: 0
  reclaimable on close: 0

UNDERFUNDED (first 10, smallest surplus first)
  none

BANDS (first 10)
  0 bytes: accounts 1, locked 810624
  1-99: accounts 0, locked 0
  100-999: accounts 10, locked 18555690
  1k-9.9k: accounts 0, locked 0
  10k-99k: accounts 0, locked 0
  100k-999k: accounts 0, locked 0
  1M and above: accounts 0, locked 0

OWNERS (top 5 by locked lamports)
  TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA  accounts 10 underfunded 0 locked 18555690
  11111111111111111111111111111111  accounts 1 underfunded 0 locked 810624
  BPFLoaderUpgradeab1e11111111111111111111111  accounts 1 underfunded 0 locked 0

PARSE ERRORS (first 10)
  none

FINDINGS: 0
```

The exit code is 0. The executable program account is visible in the status
counts and absent from every band and from the locked total, which is the
exclusion rule working.

---

## A real run: snapshot with findings

The snapshot fixture has 44 records and exercises every status. Command, then
the full capture collapsed so this page stays scannable:

```bash
PYTHONPATH=src python -m lamportlens audit samples/snapshot.jsonl
```

<details>
<summary>Full report for the snapshot fixture (3 findings)</summary>

```text
LAMPORTLENS REPORT
input: samples\snapshot.jsonl
records: 44 | lamports per byte: 6333 | parse errors: 0

STATUS COUNTS
  underfunded: 3
  at-minimum: 7
  barely-above: 1
  funded: 31
  executable-excluded: 2

TOTALS
  locked in exemptions: 22357719216
  balances observed: 22625334712
  underfunded deficit: 1021762
  reclaimable on close: 13274968

UNDERFUNDED (first 10, smallest surplus first)
  FixTure017AbCdEfGhJkMnPqRsTuVwXyZ123456789Ab owner TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb lamports 1200000 deficit 655569
  FixTure016AbCdEfGhJkMnPqRsTuVwXyZ123456789Ab owner TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA lamports 1600000 deficit 255569
  FixTure020AbCdEfGhJkMnPqRsTuVwXyZ123456789Ab owner ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL lamports 700000 deficit 110624

BANDS (first 10)
  0 bytes: accounts 3, locked 2431872
  1-99: accounts 3, locked 3989790
  100-999: accounts 26, locked 58630914
  1k-9.9k: accounts 8, locked 125545392
  10k-99k: accounts 0, locked 0
  100k-999k: accounts 0, locked 0
  1M and above: accounts 2, locked 22167121248

OWNERS (top 5 by locked lamports)
  BPFLoaderUpgradeab1e11111111111111111111111  accounts 3 underfunded 0 locked 15833310624
  TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA  accounts 26 underfunded 1 locked 6390585969
  TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb  accounts 9 underfunded 1 locked 127400961
  ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL  accounts 4 underfunded 1 locked 4800414
  11111111111111111111111111111111  accounts 2 underfunded 0 locked 1621248

PARSE ERRORS (first 10)
  none

FINDINGS: 3
```

</details>

The exit code is 1. Read the totals bottom-up: three accounts are short by
1,021,762 lamports in total, the largest single deficit belongs to the
token-2022 account at 1,200,000 lamports, and two of the three sit under
owners whose bond is otherwise small, which is worth knowing before deciding
where to spend attention.

---

## Commands

| Command | What it prints | Exit codes |
|---|---|---|
| `lamportlens version` (also `--version`) | `lamportlens <version>` | 0 |
| `lamportlens audit PATH [--format text\|json] [--limit N] [--output FILE] [--preset NAME] [--lamports-per-byte N]` | the full report | 0 clean, 1 findings, 2 usage |
| `lamportlens bands PATH [--preset NAME]` | band account counts and locked lamports | 0, or 1 when parse errors exist |
| `lamportlens owners PATH [--preset NAME]` | the per-owner table, unpaginated | 0, or 1 when parse errors exist |

`--limit N` sets how many entries each list section prints before the explicit
`... N more` line. The default is 10, and a list is never silently truncated.

---

## The input format

One JSON object per line. The fields, their types and their rules:

| Field | Type | Required | Rules |
|---|---|---|---|
| `address` | string | yes | non-empty |
| `lamports` | integer | yes | 0 or greater |
| `data_len` | integer | yes | 0 to 10,485,760 (Solana's 10 MiB account limit) |
| `owner` | string | yes | non-empty; the owning program id |
| `executable` | boolean or null | no | defaults to false; true marks a program account |

Unknown keys are ignored, so exports with extra fields stay readable. Bad
lines are collected with their line numbers and reported under `PARSE ERRORS`;
parsing continues and the good records still produce a full report. The
complete contract, including the JSON report fields, is in
[docs/FORMAT.md](docs/FORMAT.md).

The fixtures in `samples/` are synthetic test vectors, and
[samples/README.md](samples/README.md) says so explicitly and documents how
each one is constructed. `samples/build_fixture.py` rebuilds them byte for
byte. Program ids in the fixtures are real, well-known addresses; account
addresses are clearly patterned fakes.

---

## A worked walkthrough

Follow one record from the snapshot fixture, the first token account funded to
the historical bond. It carries `lamports: 2039280` and `data_len: 165`.

**Step 1, validation.** The address and owner are non-empty strings, both
numbers are integers in range, `executable` is absent so it defaults to false.
The record is accepted.

**Step 2, the minimum.** At the default rate of 6,333 lamports per byte:
`(128 + 165) * 6333 = 1,855,569`. The account holds 2,039,280 lamports, which
is 183,711 above the minimum. The same account under `--preset historical`
computes a minimum of 2,039,280 and lands exactly at-minimum. One record, two
rates, two different statuses: this is why the header line prints the rate.

**Step 3, the status.** 2,039,280 is above `floor(1,855,569 * 1.01) =
1,874,124`, so the status is funded, not barely-above. The ratio exists for
accounts that sit inside that sliver.

**Step 4, the aggregates.** The account adds 1,855,569 to `locked`, 2,039,280
to `balance`, 1,855,569 to the `100-999` band, and 1,855,569 to the token
program's owner total. It contributes nothing to `reclaimable`, because
funded accounts are not closure candidates.

**Step 5, the report.** The account never appears as a line; it is visible
only through the aggregates it moved. The report lists problems and
concentration, not records.---

## Statuses and what each one should trigger

| Status | Meaning | Action |
|---|---|---|
| `underfunded` | holds less than the bond and is at risk under rent collection | top up to `minimum`, or close if unused |
| `at-minimum` | funded exactly to the bond, nothing spendable | keep if used, close if not; the balance returns in full on close |
| `barely-above` | within one percent of the bond, effectively unspendable | decide between topping up for real use or closing |
| `funded` | holds meaningfully more than the bond | normal |
| `executable-excluded` | a program account, outside the rent rule | no action from this tool |

The full remediation playbook, including the fee caveat about closing
accounts, is in [docs/OPERATIONS.md](docs/OPERATIONS.md).

---

## Exit codes and CI integration

| Code | Meaning |
|---|---|
| 0 | no findings: no underfunded accounts, no parse errors |
| 1 | findings present |
| 2 | usage error: missing or unreadable input |

A CI job that snapshots a program's accounts can use the exit code directly:

```bash
PYTHONPATH=src python -m lamportlens audit snapshot.jsonl --format json --output report.json
```

The JSON output is stable, so `report.json` can be committed as a build
artifact or diffed between runs. Adding keys is a minor change; renaming or
removing one needs a changelog entry, because consumers depend on them.

---

## The rate is the variable

The rent-exempt minimum depends on `lamports_per_byte`, which SIMD-0437
reduces in steps from 6,960 toward 696. The default is 6,333, the step listed
as live on mainnet since epoch 1028 on 2026-09-03, and the full step table
with dates is in [docs/RATE_SCHEDULE.md](docs/RATE_SCHEDULE.md).

```bash
PYTHONPATH=src python -m lamportlens bands samples/snapshot.jsonl
```

```text
0 bytes: accounts 3, locked 2431872
1-99: accounts 3, locked 3989790
100-999: accounts 26, locked 58630914
1k-9.9k: accounts 8, locked 125545392
10k-99k: accounts 0, locked 0
