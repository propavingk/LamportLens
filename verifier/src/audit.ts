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
