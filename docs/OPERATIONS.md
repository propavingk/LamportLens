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
its token accounts is usually all you need: those are the accounts whose bonds
dominate the totals in most programs.

## Running an audit

```bash
# mainnet rate at the time of writing
lamportlens audit snapshot.jsonl

# against the historical rate, to see what the old bond would have been
lamportlens audit snapshot.jsonl --preset historical

# machine-readable, for a dashboard or a gate
lamportlens audit snapshot.jsonl --format json --output report.json
```

Exit codes make the tool usable as a CI gate without parsing anything: 0 when
every account is exempt, 1 when underfunded accounts or parse errors exist, 2
for usage problems. A job that fails on exit 1 is a job that fails when the
data is wrong.

## Reading the report

The report answers four questions in order.

**How bad is it right now?** The `STATUS COUNTS` section. `underfunded` is
the number that matters; `executable-excluded` is bookkeeping.

**How much is actually missing?** The `TOTALS` section. `deficit` is the
amount that must be added to bring every underfunded account to its minimum.
`locked` is the total bond the snapshot represents, which is the number to
compare between snapshots.

**Where is it?** The `UNDERFUNDED` list, largest deficit first. A single
mis-sized large account usually dominates the total, and it is worth fixing
before fifty small ones.

**Who holds the storage?** The `BANDS` and `OWNERS` sections. In most
programs one band and one owner dominate, and that is where a closure sweep
pays off.

## Remediation playbook

| Status | What it means | Action |
