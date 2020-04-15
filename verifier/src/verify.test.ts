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
