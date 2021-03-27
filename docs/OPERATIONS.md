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
   program accounts.
3. Snapshot at a single slot. Mixing accounts read at different slots makes
   the totals approximate, and the header does not know which slot it is
   looking at.
4. Keep the file. Snapshots diff cleanly between runs, and the interesting
   question is usually not the absolute number but the change since last
   week.

For a token program owned by a single mint, an export of the mint account and
