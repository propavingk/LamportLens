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

