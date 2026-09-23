#!/usr/bin/env python3
"""Privacy and evidence gates for local stuntd pair export."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
sys.path.insert(0, str(CORE / "src"))
from mishe_tauftauf.external_view import safe_publish_delta_view


def entry(sequence, body):
    return f"{sequence:020d} 2026-09-23T00:00:00Z observation/cleaner ::\n    | {body.rstrip()}\n    | \n    .-\n"


class StuntdExportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "core"
        self.home.mkdir()
        self.manifest = self.root / "labels.jsonl"
        self.output = self.root / "training.jsonl"
        self.before = "STATE: GREEN\n"
        self.after = "STATE: RED\n"
        (self.home / "feed").write_text(entry(1, self.before) + entry(2, self.after))
        cases = []
        for name, previous, current, label in (("change", 1, 2, "yes"), ("identity", 1, 1, "no")):
            pair = safe_publish_delta_view(self.before, self.after if current == 2 else self.before)
            cases.append({"case_id": name, "previous_feed_sequence": previous,
                          "current_feed_sequence": current, "expected_label": label,
                          "pair_sha256": hashlib.sha256(pair.encode()).hexdigest(),
                          "question_version": "projected-pair-v1.1", "basis": "fixture direct"})
        self.cases = cases
        self.save()

    def save(self):
        self.manifest.write_text("".join(json.dumps(case) + "\n" for case in self.cases))

    def run_export(self, minimum=2):
        return subprocess.run([sys.executable, str(ROOT / "scripts/mesh-mishe-stuntd-export"),
                               "--manifest", str(self.manifest), "--home", str(self.home),
                               "--output", str(self.output), "--min-examples", str(minimum)],
                              env={**os.environ, "MESH_MISHE_CORE": str(CORE)}, text=True,
                              capture_output=True)

    def test_exports_only_pinned_safe_pairs(self):
        result = self.run_export()
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [json.loads(line) for line in self.output.read_text().splitlines()]
        self.assertEqual([row["answer"] for row in rows], ["true", "false"])
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o600)
        self.assertNotIn("fixture direct", self.output.read_text())

    def test_minimum_blocks_importable_output(self):
        result = self.run_export(300)
        self.assertEqual(result.returncode, 2)
        self.assertIn("insufficient independent labels", result.stderr)
        self.assertFalse(self.output.exists())

    def test_duplicate_or_unpinned_pair_fails_closed(self):
        self.cases.append(dict(self.cases[0], case_id="repeat"))
        self.save()
        result = self.run_export()
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.output.exists())
        self.cases.pop()
        self.cases[0]["pair_sha256"] = "0" * 64
        self.save()
        result = self.run_export()
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.output.exists())

    def test_invalid_guard_must_remain_invalid(self):
        self.cases.append(dict(self.cases[0], case_id="guard", kind="invalid-prior-guard",
                               expected_label="unknown"))
        self.save()
        result = self.run_export()
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid guard accepted", result.stderr)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
