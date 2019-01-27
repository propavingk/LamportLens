"""Tests for the snapshot audit over the fixtures."""
from __future__ import annotations

import unittest
from pathlib import Path

from lamportlens.audit import audit
from lamportlens.model import parse_file
from lamportlens.rent import STATUS_AT_MINIMUM, STATUS_EXCLUDED, STATUS_FUNDED, STATUS_UNDERFUNDED

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


class CleanSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
