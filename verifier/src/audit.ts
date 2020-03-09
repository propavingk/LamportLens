// Auditing for the verifier, mirroring the Python audit rules and emitting
// the same subset of keys that the Python JSON report exposes, so the parity
// script can compare the two implementations field by field.

import { ParseError, parseText } from "./parse.js";
import {
  AccountRecord,
  DEFAULT_LAMPORTS_PER_BYTE,
  STATUS_AT_MINIMUM,
  STATUS_BARELY_ABOVE,
  STATUS_EXCLUDED,
  STATUS_FUNDED,
  STATUS_UNDERFUNDED,
  assess,
  minimumBalance,
} from "./rent.js";

export const BANDS: Array<[string, number, number]> = [
  ["0 bytes", 0, 0],
  ["1-99", 1, 99],
  ["100-999", 100, 999],
  ["1k-9.9k", 1_000, 9_999],
