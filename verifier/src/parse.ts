// JSONL parsing for the verifier, mirroring the validation rules that the
// Python model applies. Errors are collected, not thrown, so a partially
// readable snapshot still produces a full result.

import { AccountRecord, MAX_ACCOUNT_DATA_LEN } from "./rent.js";

export interface ParseError {
  line: number;
  message: string;
}

function requireNonEmptyString(obj: Record<string, unknown>, key: string, line: number): string {
  if (!(key in obj)) throw new FormatError(`line ${line}: missing required field '${key}'`);
  const value = obj[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new FormatError(`line ${line}: field '${key}' must be a non-empty string`);
  }
  return value;
}

function requireInteger(
  obj: Record<string, unknown>,
  key: string,
  line: number,
  minimum: number,
  maximum?: number,
): number {
  if (!(key in obj)) throw new FormatError(`line ${line}: missing required field '${key}'`);
  const value = obj[key];
  if (typeof value !== "number" || !Number.isInteger(value)) {
    throw new FormatError(`line ${line}: field '${key}' must be an integer`);
  }
  if (value < minimum) throw new FormatError(`line ${line}: field '${key}' must be >= ${minimum}`);
  if (maximum !== undefined && value > maximum) {
    throw new FormatError(`line ${line}: field '${key}' must be <= ${maximum}`);
  }
  return value;
}

export class FormatError extends Error {}

export function parseRecord(value: unknown, line: number): AccountRecord {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new FormatError(`line ${line}: record must be a JSON object`);
  }
  const obj = value as Record<string, unknown>;
  const address = requireNonEmptyString(obj, "address", line);
  const lamports = requireInteger(obj, "lamports", line, 0);
  const dataLen = requireInteger(obj, "data_len", line, 0, MAX_ACCOUNT_DATA_LEN);
  const owner = requireNonEmptyString(obj, "owner", line);
  let executable = false;
  if ("executable" in obj && obj["executable"] !== null) {
    if (typeof obj["executable"] !== "boolean") {
      throw new FormatError(`line ${line}: field 'executable' must be a boolean`);
    }
    executable = obj["executable"];
  }
  return { address, lamports, dataLen, owner, executable, line };
}

export function parseText(text: string): { records: AccountRecord[]; errors: ParseError[] } {
  const records: AccountRecord[] = [];
  const errors: ParseError[] = [];
  const lines = text.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    const raw = lines[index];
    if (raw.trim() === "") continue;
    const number = index + 1;
