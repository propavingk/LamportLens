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

