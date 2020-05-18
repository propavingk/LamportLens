#!/usr/bin/env node
// Command line front end for the verifier.
//
// Usage:
//   node dist/verify.js <snapshot.jsonl> [--lamports-per-byte N] [--preset name]
//
// Prints the audit result as JSON on stdout, so scripts/parity.py can compare
// it with the Python report. Exit codes: 0 clean, 1 findings, 2 usage or
// input error.

import { readFileSync } from "node:fs";
import { auditText } from "./audit.js";
import { DEFAULT_LAMPORTS_PER_BYTE, RATE_PRESETS } from "./rent.js";

function main(argv: string[]): number {
  const args = argv.slice(2);
  let path: string | null = null;
  let lamportsPerByte: number | null = null;
  let preset: string | null = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--lamports-per-byte") {
      lamportsPerByte = Number(args[++i]);
    } else if (arg === "--preset") {
      preset = args[++i] ?? null;
