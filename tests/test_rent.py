"""Tests for the rent arithmetic."""
from __future__ import annotations

import unittest

from lamportlens.model import AccountRecord
from lamportlens.rent import (
    DEFAULT_LAMPORTS_PER_BYTE,
    RATE_PRESETS,
    STATUS_AT_MINIMUM,
    STATUS_BARELY_ABOVE,
    STATUS_EXCLUDED,
    STATUS_FUNDED,
    STATUS_UNDERFUNDED,
    assess,
    minimum_balance,
