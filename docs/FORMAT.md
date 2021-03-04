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
