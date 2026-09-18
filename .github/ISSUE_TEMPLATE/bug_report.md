---
name: Bug report
about: A crash, a wrong number, or a report that does not match the snapshot
title: ""
labels: bug
assignees: ""
---

**What happened**

**What you expected**

**Reproduce**

Command:

```bash
PYTHONPATH=src python -m lamportlens audit path/to/snapshot.jsonl
```

Smallest snapshot that shows it (two or three JSONL lines are usually enough):

```jsonl

```

**Real output**

Paste the output verbatim, including the `FINDINGS:` line:

```

```

**Environment**

- OS:
- Python version (`python --version`):
- Node version (`node --version`) if the verifier is involved:
- Which implementation: Python / TypeScript / both differ
- Rate in use: default, `--preset`, or explicit `--lamports-per-byte`
