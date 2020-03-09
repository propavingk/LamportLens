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
  ["10k-99k", 10_000, 99_999],
  ["100k-999k", 100_000, 999_999],
  ["1M and above", 1_000_000, 10_485_760],
];

export interface AuditResult {
  records: number;
  findings: number;
  statusCounts: Record<string, number>;
  totals: { locked: number; balance: number; deficit: number; reclaimable: number };
  bands: Array<{ label: string; accounts: number; locked: number }>;
  underfunded: Array<{ address: string; owner: string; lamports: number; minimum: number; deficit: number }>;
