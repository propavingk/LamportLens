#!/usr/bin/env node
// Command line front end for the verifier.
//
// Usage:
//   node dist/verify.js <snapshot.jsonl> [--lamports-per-byte N] [--preset name]
//
// Prints the audit result as JSON on stdout, so scripts/parity.py can compare
// it with the Python report. Exit codes: 0 clean, 1 findings, 2 usage or
