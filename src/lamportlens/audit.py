"""Snapshot audit: statuses, storage bands, owner concentration.

Every decision this module makes is a pure function of the records and the
active lamports-per-byte rate. Nothing depends on wall-clock time, locale or
hash ordering that is not sorted.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .model import MAX_ACCOUNT_DATA_LEN, AccountRecord
from .rent import (
