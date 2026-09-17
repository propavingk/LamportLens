# The rent-exempt rate schedule

This document is the reference for the one number that changes LamportLens
results over time: `lamports_per_byte`. It records the SIMD-0437 reduction
steps, the dates the Solana Foundation upgrade notes give for them, and the
minimum balances each step produces for common account sizes.

Everything in the tables below is exact integer arithmetic on the documented
formula. Nothing here is a benchmark or an estimate.

## The formula

```
minimum_balance = (ACCOUNT_STORAGE_OVERHEAD + data_len) * lamports_per_byte
```

`ACCOUNT_STORAGE_OVERHEAD` is 128 bytes, the space an empty account occupies.
The historical version of the same formula used two constants,
`lamports_per_byte_year` (3480) and `exemption_threshold` (2.0). Folding the
threshold into the rate, as SIMD-0194 does, gives 6960, which is why the
schedule starts there.

## The steps

| Step | lamports_per_byte | Status | Notes |
|---|---|---|---|
| historical (SIMD-0194 form) | 6,960 | superseded | the rate that produced the familiar 890,880 and 2,039,280 lamports |
| SIMD-0437-1 | 6,333 | live on mainnet | active since mainnet epoch 1028, 2026-09-03 |
| SIMD-0437-2 | 5,080 | live on testnet | testnet activation 2026-09-03, mainnet expected mid-September 2026 |
| SIMD-0437-3 | 2,575 | queued | expected with Agave 4.4, November 2026 window |
| SIMD-0437-4 | 1,322 | queued | expected with Agave 4.4, November 2026 window |
| SIMD-0437-5 | 696 | queued | expected with Agave 4.4, late 2026 |

The default in `src/lamportlens/rent.py` is 6,333, the step listed as live on
mainnet at the time of writing. When the next step activates, changing the
default is a release with a changelog entry, because snapshots audited before
and after will report different deficits for the same accounts.

## Minimum balances by size and step

All values are lamports. Sizes are the real ones used on Solana: a token mint
is 82 bytes, an SPL token account is 165 bytes, and a multisig account is 355
bytes. The 0 byte row is the empty-account case that the fixtures use.

| data_len | 6,960 | 6,333 | 5,080 | 2,575 | 1,322 | 696 |
|---|---|---|---|---|---|---|
| 0 | 890,880 | 810,624 | 650,240 | 329,600 | 169,216 | 89,088 |
| 82 | 1,461,600 | 1,329,930 | 1,066,800 | 540,750 | 277,620 | 146,160 |
| 165 | 2,039,280 | 1,855,569 | 1,488,440 | 754,475 | 387,346 | 203,868 |
| 355 | 3,361,680 | 3,058,839 | 2,453,640 | 1,243,725 | 638,526 | 336,168 |
| 1 MiB | 7,298,979,840 | 6,641,442,432 | 5,327,416,320 | 2,700,412,800 | 1,386,386,688 | 729,897,984 |
| 10 MiB | 72,981,780,480 | 66,407,128,704 | 53,268,311,040 | 27,001,161,600 | 13,862,343,936 | 7,298,178,048 |

10 MiB is Solana's maximum account data size (`MAX_ACCOUNT_DATA_LEN`), so the
last row is the largest exemption any account can require.

## Why the step history matters to an audit

A snapshot is a point-in-time reading, and the minimum it is compared against
depends on the rate that was live when the accounts were funded. Two examples
from the fixtures:

- An SPL token account holding 2,039,280 lamports is at exactly the minimum
  under the historical rate and comfortably funded under the current one. An
  audit that used the wrong step would report either a false deficit or a
  false sense of safety.
- A zero-byte account holding 810,624 lamports is at exactly the current
  minimum and underfunded by 80,256 lamports against the historical rate.

That is why the rate is a required input to the arithmetic and why the report
prints the rate it used on the header line. It is also why the class of
accounts sitting just below 2,039,280 lamports is worth watching: they were
funded to the old bond, and the current rate made part of that bond
unnecessary, which makes them candidates for closure and recovery rather than
maintenance.

## Selecting a step

```bash
# the default, the step live on mainnet at the time of writing
lamportlens audit snapshot.jsonl

# any named step
lamportlens audit snapshot.jsonl --preset simd-0437-2

# an explicit rate, for a private cluster or a test
lamportlens audit snapshot.jsonl --lamports-per-byte 6960
```

Resolution order is explicit: `--lamports-per-byte` wins over `--preset`,
which wins over the default. The same options exist on the TypeScript
verifier, and the parity script in CI compares both implementations at the
default rate on every fixture.

## Sources

- Solana documentation, Accounts: the rent-exempt minimum formula and the
  128 byte storage overhead.
- Solana upgrade notes, Reduced Rent: the SIMD-0437 step list, the
  6,960 to 6,333 reduction live on mainnet since epoch 1028 on 2026-09-03,
  and the remaining steps queued behind Agave 4.4.
- solana-improvement-documents, SIMD-0194: renaming to a single
  `lamports_per_byte` and deprecating the floating point threshold.

This document restates those sources; it does not replace them. When the
network moves to the next step, re-read the upgrade notes before changing
anything here.
