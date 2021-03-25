# Operations guide

This document is for the person running LamportLens on real snapshots: how to
capture one, how to read the report, and what action each status should
trigger.

## Capturing a snapshot

LamportLens does not talk to a cluster. Capture is deliberately out of scope:
every RPC provider, archival tool, and explorer exports accounts in a slightly
different shape, and a fetcher would freeze one of them into this tool.

The input is one JSON object per line with the fields in `docs/FORMAT.md`.
Whatever you use to produce it, the rules are:

1. Record `lamports` and `data_len` exactly as the cluster reports them. Do
   not pre-round, and do not convert between SOL and lamports in the capture
   step. The tool works in lamports only.
2. Record the owning program id in `owner`, and set `executable` only for
