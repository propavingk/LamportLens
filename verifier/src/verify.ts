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
    } else if (path === null) {
      path = arg;
    } else {
      process.stderr.write("verify: unexpected argument " + arg + "\n");
      return 2;
    }
  }

  if (path === null) {
    process.stderr.write("usage: verify <snapshot.jsonl> [--lamports-per-byte N] [--preset name]\n");
    return 2;
  }

  let rate = DEFAULT_LAMPORTS_PER_BYTE;
  if (lamportsPerByte !== null) {
    if (!Number.isInteger(lamportsPerByte) || lamportsPerByte <= 0) {
      process.stderr.write("verify: lamports-per-byte must be a positive integer\n");
      return 2;
    }
    rate = lamportsPerByte;
  } else if (preset !== null) {
    const value = RATE_PRESETS[preset];
    if (value === undefined) {
      process.stderr.write("verify: unknown preset " + preset + "\n");
      return 2;
    }
    rate = value;
  }

  let text: string;
  try {
    text = readFileSync(path, "utf8");
  } catch (error) {
    process.stderr.write("verify: cannot read " + path + "\n");
    return 2;
  }

  const result = auditText(text, rate);
  const payload = {
    input: path,
    records: result.records,
    lamports_per_byte: rate,
    findings: result.findings,
    status_counts: result.statusCounts,
    totals: result.totals,
    bands: result.bands,
    underfunded: result.underfunded,
    parse_errors: result.parseErrors,
  };
  process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
  return result.findings > 0 ? 1 : 0;
}

process.exit(main(process.argv));

// draft note 1416
