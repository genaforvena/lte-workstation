#!/usr/bin/env python3
"""Fixture checks for aggregate-only cleaner wake-volume reports."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/mesh-mishe-shadow-volume"
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
START = "2026-09-23T11:00:00Z"
END = "2026-09-23T12:00:00Z"


def entry(sequence: int, stamp: str, source: str, body: str) -> str:
    return f"{sequence:020d} {stamp} {source} ::\n    | {body}\n    .-\n"


class VolumeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.feed = Path(self.tmp.name) / "feed"
        self.log = Path(self.tmp.name) / "legacy.log"
        self.feed.write_text("".join([
            entry(1, "2026-09-23T10:59:59Z", "observation/cleaner", "STATE: prior"),
            entry(2, "2026-09-23T11:00:00Z", "mishe-tauftauf", "wake requested top-pain cleaner for entry 1"),
            entry(3, "2026-09-23T11:10:00Z", "observation/cleaner-task", "cleaner task-ledger epoch=5 status=open"),
            entry(4, "2026-09-23T11:10:01Z", "mishe-tauftauf", "wake requested top-pain cleaner for entry 3"),
            entry(5, "2026-09-23T12:00:00Z", "mishe-tauftauf", "wake requested top-pain cleaner for entry 1"),
        ]), encoding="utf-8")
        self.log.write_text("\n".join([
            "2026-09-23T10:59:59Z cleaner: WOKE mind (cleaner) to consume its stream",
            "2026-09-23T11:00:00Z cleaner: change detected [smart-default] — waking",
            "2026-09-23T11:00:01Z cleaner: refractory — last wake of cleaner <1800s ago, holding (retry next pass)",
            "2026-09-23T11:00:02Z cleaner: mind busy (cleaner) — skip wake (will re-invite next pass)",
            "2026-09-23T11:00:03Z cleaner: mesh-tell REFUSED — PRIVATE-TEXT",
            "2026-09-23T11:00:04Z cleaner: WOKE mind (cleaner) to consume its stream",
            "2026-09-23T11:00:05Z cleaner: pane unchanged — no wake (droplet held)",
            "2026-09-23T12:00:00Z cleaner: WOKE mind (cleaner) to consume its stream",
            "2026-09-23T11:00:00Z other: change detected [smart-default] — waking",
        ]) + "\n", encoding="utf-8")

    def run_report(self):
        env = dict(os.environ, MESH_MISHE_CORE=str(CORE))
        result = subprocess.run([str(SCRIPT), "--start", START, "--end", END,
                                 "--feed", str(self.feed), "--legacy-log", str(self.log)],
                                capture_output=True, text=True, env=env, check=False)
        self.assertEqual(result.stderr, "")
        self.assertNotIn("PRIVATE-TEXT", result.stdout)
        self.assertNotIn("cleaner task-ledger", result.stdout)
        self.assertNotIn(str(self.tmp.name), result.stdout)
        return result, json.loads(result.stdout)

    def test_counts_and_half_open_boundaries(self):
        result, report = self.run_report()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["authority"], "legacy")
        self.assertEqual(report["comparison"], "contemporaneous-counts-only")
        counts = report["counts"]
        for name in ("shadow_observation_requests", "shadow_task_open_requests", "legacy_change",
                     "legacy_refractory", "legacy_busy", "legacy_refused", "legacy_delivered",
                     "legacy_unchanged"):
            self.assertEqual(counts[name], 1, name)
        self.assertTrue(all(value == 0 for name, value in counts.items() if name not in (
            "shadow_observation_requests", "shadow_task_open_requests", "legacy_change",
            "legacy_refractory", "legacy_busy", "legacy_refused", "legacy_delivered", "legacy_unchanged")))

    def test_unknown_unrecognized_legacy_line(self):
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write("2026-09-23T11:30:00Z cleaner: PRIVATE-TEXT\n")
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["status"], report["reason"]), (2, "UNKNOWN", "legacy-event"))

    def test_unknown_malformed_request(self):
        with self.feed.open("a", encoding="utf-8") as stream:
            stream.write(entry(6, "2026-09-23T11:30:00Z", "mishe-tauftauf", "wake requested top-pain cleaner PRIVATE-TEXT"))
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["reason"]), (2, "feed-request"))

    def test_unknown_missing_reference(self):
        with self.feed.open("a", encoding="utf-8") as stream:
            stream.write(entry(6, "2026-09-23T11:30:00Z", "mishe-tauftauf", "wake requested top-pain cleaner for entry 999"))
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["reason"]), (2, "feed-reference"))

    def test_unknown_malformed_feed(self):
        with self.feed.open("a", encoding="utf-8") as stream:
            stream.write("PRIVATE-TEXT")
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["reason"]), (2, "input"))

    def test_unknown_unreadable_log(self):
        self.log.unlink()
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["reason"]), (2, "input"))

    def test_unknown_malformed_legacy_stamp(self):
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write("2026-09-XXT11:30:00Z cleaner: PRIVATE-TEXT\n")
        result, report = self.run_report()
        self.assertEqual((result.returncode, report["reason"]), (2, "legacy-format"))

    def test_unknown_future_interval(self):
        result = subprocess.run([str(SCRIPT), "--start", "2099-01-01T00:00:00Z",
                                 "--end", "2099-01-01T01:00:00Z", "--feed", str(self.feed),
                                 "--legacy-log", str(self.log)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["reason"], "interval")

    def test_default_interpreter_finds_editable_core(self):
        env = dict(os.environ)
        env.pop("MESH_MISHE_CORE", None)
        result = subprocess.run([str(SCRIPT), "--start", START, "--end", END,
                                 "--feed", str(self.feed), "--legacy-log", str(self.log)],
                                capture_output=True, text=True, env=env, check=False)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["counts"]["shadow_observation_requests"], 1)


if __name__ == "__main__":
    unittest.main()
