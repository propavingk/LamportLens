// Tests for the verifier: formula anchors, status classification, and the
// same designed counts the Python tests assert over the shared fixtures.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { test } from "node:test";
import assert from "node:assert/strict";

import { auditText } from "./audit.js";
import { AccountRecord, assess, minimumBalance } from "./rent.js";

const here = dirname(fileURLToPath(import.meta.url));
const samples = join(here, "..", "..", "samples");

function sample(name: string): string {
  return readFileSync(join(samples, name), "utf8");
}

function record(lamports: number, dataLen: number, executable = false): AccountRecord {
  return { address: "A".repeat(44), lamports, dataLen, owner: "O".repeat(44), executable, line: 1 };
}

test("formula anchors", () => {
  assert.equal(minimumBalance(0), 810_624);
  assert.equal(minimumBalance(165), 1_855_569);
  assert.equal(minimumBalance(0, 6960), 890_880);
  assert.equal(minimumBalance(165, 6960), 2_039_280);
});

test("status classification", () => {
  assert.equal(assess(record(800_000, 0)), "underfunded");
  assert.equal(assess(record(810_624, 0)), "at-minimum");
  assert.equal(assess(record(815_000, 0)), "barely-above");
  assert.equal(assess(record(2_500_000, 0)), "funded");
  assert.equal(assess(record(1, 400_000, true)), "executable-excluded");
});

test("clean snapshot has no findings", () => {
  const result = auditText(sample("clean-snapshot.jsonl"));
  assert.equal(result.records, 12);
  assert.equal(result.findings, 0);
  assert.equal(result.statusCounts["funded"], 11);
  assert.equal(result.statusCounts["executable-excluded"], 1);
});

test("snapshot counts match the designed fixture", () => {
  const result = auditText(sample("snapshot.jsonl"));
  assert.equal(result.records, 44);
  assert.equal(result.findings, 3);
