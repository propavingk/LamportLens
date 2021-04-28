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
