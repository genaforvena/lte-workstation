#!/usr/bin/env python3
# Verify signed labor corrections require exact source-bound attribution.
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("labor_reconcile", ROOT / "scripts/mesh_labor_reconcile.py")
labor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(labor)

WINDOW = "2026-09-06T12:19:01Z..2026-09-06T12:29:06Z"
FEED = f"""2026-09-06 * labour feed  ; window:{WINDOW}
    expenses:labour:openai:witness  4 TURN
    assets:budget:openai  -4 TURN
"""
CORRECTION = """2026-09-06 * Codex root-identity migration correction
    ; Reverse title-generation events; retain root completion.
    expenses:labour:openai:witness  -2 TURN
    assets:budget:openai  2 TURN
"""


class Corrections(unittest.TestCase):
    def load(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "2026.journal").write_text(text)
            return labor.load_journal(path)

    def test_signed_correction_requires_explicit_attribution(self):
        with self.assertRaisesRegex(ValueError, "unwindowed labour posting"):
            self.load(FEED + CORRECTION)

    def test_hash_bound_correction_preserves_exact_window(self):
        digest = hashlib.sha256(CORRECTION.strip().encode()).hexdigest()
        annotation = f"; labor-correction-window: {digest} {WINDOW}\n"
        intervals, groups, total, tasks, corrections = self.load(FEED + CORRECTION + annotation)
        self.assertEqual(total, 2)
        self.assertEqual(list(groups.values()), [2])
        self.assertEqual(corrections, -2)
        self.assertEqual(len(intervals), 1)

    def test_stale_annotation_fails_closed(self):
        annotation = f"; labor-correction-window: {'0' * 64} {WINDOW}\n"
        with self.assertRaises(ValueError):
            self.load(FEED + CORRECTION + annotation)

    def test_positive_late_correction_is_counted_in_original_group(self):
        correction = f"""2026-09-19 * labour correction  ; window:{WINDOW}
    ; source-event: late-event-1
    expenses:labour:openai:witness  +1 TURN
    assets:budget:openai  -1 TURN
"""
        intervals, groups, total, tasks, corrections = self.load(FEED + correction)
        self.assertEqual(total, 5)
        self.assertEqual(list(groups.values()), [5])
        self.assertEqual(corrections, 1)

    def test_conflicting_attribution_is_rejected(self):
        digest = hashlib.sha256(CORRECTION.strip().encode()).hexdigest()
        annotation = f"; labor-correction-window: {digest} {WINDOW}\n"
        with self.assertRaises(ValueError):
            self.load(FEED + CORRECTION + annotation + annotation.replace("12:19:01", "12:18:01"))


if __name__ == "__main__":
    unittest.main()
