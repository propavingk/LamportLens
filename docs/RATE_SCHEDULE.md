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
