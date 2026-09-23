#!/usr/bin/env python3
"""Label attribution gates for the legacy-verdict stuntd manifest."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
SCRIPT = ROOT / "scripts" / "mesh-mishe-stuntd-manifest"


def feed_entry(sequence, stamp, body):
    framed = "".join(f"    | {line}\n" for line in body.rstrip().split("\n"))
    return f"{sequence:020d} {stamp} observation/cleaner ::\n{framed}    .\n"



class ManifestTest(unittest.TestCase):
    """A temp pane-consume.log supplies the verdicts; no real mesh state is read."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Legacy log lives under $HOME/.mesh, so redirect the whole home.
        self.home = self.root / "mesh-home"
        (self.home / ".mesh").mkdir(parents=True)
        self.log = self.home / ".mesh" / "pane-consume.log"
        self.feed_home = self.home / "mishe-tauftauf"
        self.feed_home.mkdir()

        self.stamps = ["2026-09-23T10:00:00Z", "2026-09-23T11:00:00Z"]
        self.write_log(self.stamps)
        self.write_feed()

        self.manifest = self.root / "manifest.jsonl"

    def write_log(self, stamps):
        self.log.write_text(
            "".join(f"{stamp} cleaner: SURPRISE (task change) [smart-default] — waking\n"
                    for stamp in stamps)
        )

    def write_feed(self):
        bodies = [
            "STATE: GREEN\nCLEANER: candidates=1 held=0 actionable=0 delete=0 unknowns=0 head=aaaaaaaaaaaa task=none task-epoch=0 task-event-count=0 task-events=NONE\n",
            "STATE: GREEN\nCLEANER: candidates=1 held=0 actionable=0 delete=0 unknowns=0 head=aaaaaaaaaaaa task=none task-epoch=0 task-event-count=0 task-events=NONE\n",
            "STATE: RED\nCLEANER: candidates=2 held=1 actionable=0 delete=0 unknowns=0 head=bbbbbbbbbbbb task=none task-epoch=0 task-event-count=0 task-events=NONE\n",
            "STATE: INTERMEDIATE\nCLEANER: candidates=3 held=0 actionable=0 delete=0 unknowns=0 head=cccccccccccc task=none task-epoch=0 task-event-count=0 task-events=NONE\n",
        ]
        stamps = ["2026-09-23T09:00:00Z", "2026-09-23T09:30:00Z", "2026-09-23T10:30:00Z", "2026-09-23T11:30:00Z"]
        self.feed_home.joinpath("feed").write_text(
            "".join(
                feed_entry(i + 1, stamp, body)
                for i, (stamp, body) in enumerate(zip(stamps, bodies))
            )
        )

    def run_manifest(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--manifest", str(self.manifest),
             "--feed-home", str(self.feed_home)],
            env={**os.environ, "HOME": str(self.home), "MESH_MISHE_CORE": str(CORE)},
            text=True, capture_output=True,
        )

    def rows(self):
        return [json.loads(line) for line in self.manifest.read_text().splitlines()]

    def test_positive_needs_a_verdict_inside_the_window(self):
        result = self.run_manifest()
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows()
        self.assertEqual(len(rows), 3)
        # 09:00 -> 09:30 holds no verdict; 09:30 -> 10:30 contains the 10:00
        # verdict; 10:30 -> 11:30 contains the 11:00 one.
        self.assertEqual([row["expected_label"] for row in rows], ["no", "yes", "yes"])
        for row in rows:
            self.assertEqual(row["question_version"], "projected-pair-v1.1")
            self.assertTrue(row["basis"].startswith("legacy mesh-pane-consume SURPRISE"))

    def test_verdict_outside_window_is_a_negative(self):
        # An early verdict before the first pane pair starts must not leak in;
        # the in-window verdicts keep both classes so the corpus stays landable.
        self.write_log(["2026-09-23T08:00:00Z", "2026-09-23T10:00:00Z", "2026-09-23T11:00:00Z"])
        result = self.run_manifest()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row["expected_label"] for row in self.rows()], ["no", "yes", "yes"])

    def test_verdict_on_the_previous_boundary_is_negative(self):
        # 09:00 exactly equals the previous pane timestamp, so the open-closed
        # window (prev, cur] must not claim it; in-window verdicts keep both classes.
        self.write_log(["2026-09-23T09:00:00Z", "2026-09-23T10:00:00Z", "2026-09-23T11:00:00Z"])
        result = self.run_manifest()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row["expected_label"] for row in self.rows()], ["no", "yes", "yes"])

    def test_missing_log_is_unknown_and_writes_nothing(self):
        self.log.unlink()
        result = self.run_manifest()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stderr)
        self.assertFalse(self.manifest.exists())

    def test_single_class_corpus_fails_closed(self):
        # Identical panes collapse to one unsafe pair, so no row survives.
        self.feed_home.joinpath("feed").write_text(
            feed_entry(1, "2026-09-23T09:30:00Z", "STATE: GREEN\n")
            + feed_entry(2, "2026-09-23T10:30:00Z", "STATE: GREEN\n")
        )
        result = self.run_manifest()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stderr)
        self.assertFalse(self.manifest.exists())

    def test_manifest_rows_re_export_cleanly(self):
        result = self.run_manifest()
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "training.jsonl"
        export = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "mesh-mishe-stuntd-export"),
             "--manifest", str(self.manifest), "--home", str(self.feed_home),
             "--output", str(output), "--min-examples", "2"],
            env={**os.environ, "HOME": str(self.home), "MESH_MISHE_CORE": str(CORE),
                 "MESH_MISHE_EXPORT_ROOT": str(self.root)},
            text=True, capture_output=True,
        )
        self.assertEqual(export.returncode, 0, export.stderr)
        rows = [json.loads(line) for line in output.read_text().splitlines()]
        self.assertEqual(len(rows), 3)
        self.assertEqual(sorted(row["answer"] for row in rows), ["false", "true", "true"])


if __name__ == "__main__":
    unittest.main()
