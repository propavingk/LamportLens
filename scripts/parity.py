"""Cross-engine parity check for LamportLens.

Runs the Python core and the TypeScript verifier on the same fixtures and
compares the numbers they report. This is a build-time check, not part of the
offline tool: neither implementation spawns the other at runtime.

Usage (from the repository root, after `cd verifier && npm run build`):

    python scripts/parity.py

