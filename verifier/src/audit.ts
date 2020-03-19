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
  parseErrors: ParseError[];
}

const STATUS_ORDER = [
  STATUS_UNDERFUNDED,
  STATUS_AT_MINIMUM,
  STATUS_BARELY_ABOVE,
  STATUS_FUNDED,
  STATUS_EXCLUDED,
];

function bandLabel(dataLen: number): string {
  for (const [label, low, high] of BANDS) {
    if (dataLen >= low && dataLen <= high) return label;
  }
  return BANDS[BANDS.length - 1][0];
}

export function audit(
  records: AccountRecord[],
  parseErrors: ParseError[],
  lamportsPerByte = DEFAULT_LAMPORTS_PER_BYTE,
): AuditResult {
  const statusCounts: Record<string, number> = {};
  const bands = BANDS.map(([label]) => ({ label, accounts: 0, locked: 0 }));
  const bandIndex = new Map(bands.map((band) => [band.label, band]));
  const underfunded: AuditResult["underfunded"] = [];
  const totals = { locked: 0, balance: 0, deficit: 0, reclaimable: 0 };

  for (const record of records) {
    const status = assess(record, lamportsPerByte);
    statusCounts[status] = (statusCounts[status] ?? 0) + 1;
    const minimum = minimumBalance(record.dataLen, lamportsPerByte);
    if (status === STATUS_UNDERFUNDED) {
      const deficit = minimum - record.lamports;
      totals.deficit += deficit;
      underfunded.push({
        address: record.address,
        owner: record.owner,
        lamports: record.lamports,
        minimum,
        deficit,
      });
    }
    if (status !== STATUS_EXCLUDED) {
      totals.locked += minimum;
