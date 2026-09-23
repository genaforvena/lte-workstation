#!/usr/bin/env python3
"""Cleaner shadow parity checks use only event epochs and statuses."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class CleanerParityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.log = self.base / "chat.log"
        self.baseline = self.home / "cleaner-parity-baseline.json"
        self.baseline.write_text(json.dumps({"epoch": 0, "time": "2026-09-23T04:00:00Z"}), encoding="utf-8")
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home),
                    "MESH_MISHE_CHAT_LOG": str(self.log), "MESH_MISHE_CORE": str(CORE),
                    "PYTHONPATH": str(CORE / "src")}

    def ledger(self, statuses):
        lines = []
        for index, status in enumerate(statuses, 1):
            second = index
            minute, second = divmod(second, 60)
            timestamp = f"2026-09-23T04:{minute:02d}:{second:02d}Z"
            lines.append(f"{timestamp} cleaner@mesh-home :: [task-ledger] v1 r={index} | "
                         f"/chain=s:private-task-{index} | /current=i:0 | /status=s:{status} | "
                         f"/steps/0/owner=s:cleaner | /steps/0/status=s:{status} | "
                         f"/description=s:private-path-{index}\n")
        self.log.write_text("".join(lines), encoding="utf-8")

    def observation(self, second, count, events, sequence=1):
        minute, second = divmod(second, 60)
        timestamp = f"2026-09-23T04:{minute:02d}:{second:02d}.000000Z"
        body = ("STATE: GREEN\nCLEANER: candidates=0 held=0 actionable=0 delete=0 unknowns=0 "
                f"head=abcdef123456 task=none task-epoch={events[-1][0] if events else 0} "
                f"task-event-count={count} task-events=" +
                (",".join(f"{epoch}:{status}" for epoch, status in events) if events else "NONE") + "\n")
        with (self.home / "feed").open("a", encoding="utf-8") as stream:
            stream.write(f"{sequence:020d} {timestamp} observation/cleaner ::\n")
            for line in body.splitlines():
                stream.write(f"    | {line}\n")
            stream.write("    .\n")

    def check(self):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-parity")], env=self.env,
                              text=True, capture_output=True)

    def test_transient_open_active_complete_is_covered_by_one_later_sample(self):
        self.ledger(["open", "active", "complete"])
        self.observation(70, 3, [(1, "open"), (2, "active"), (3, "complete")])
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS covered=3 missing=0 pending=0", result.stdout)
        self.assertIn("latency-max=69s", result.stdout)
        self.assertNotIn("private-", result.stdout + result.stderr)

    def test_bounded_event_overflow_is_missing(self):
        statuses = ["open"] * 20
        self.ledger(statuses)
        self.observation(1, 1, [(1, "open")])
        self.observation(70, 20, [(i, "open") for i in range(5, 21)], sequence=2)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL covered=17 missing=3 pending=0", result.stdout)

    def test_pre_first_frame_history_is_unknown(self):
        self.ledger(["open"] * 20)
        self.observation(70, 20, [(i, "open") for i in range(5, 21)])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN reason=prehistory", result.stdout)

    def test_new_transition_after_latest_observation_is_pending(self):
        self.ledger(["open", "active"])
        self.observation(1, 1, [(1, "open")])
        result = self.check()
        self.assertEqual(result.returncode, 0)
        self.assertIn("PENDING covered=1 missing=0 pending=1", result.stdout)

    def test_recovered_unknown_observation_does_not_poison_parity(self):
        self.ledger(["open", "active"])
        self.observation(1, 1, [(1, "open")], sequence=1)
        with (self.home / "feed").open("a", encoding="utf-8") as stream:
            stream.write("00000000000000000002 2026-09-23T04:00:03.000000Z observation/cleaner ::\n"
                         "    | STATE: UNKNOWN\n    .\n")
        self.observation(5, 2, [(1, "open"), (2, "active")], sequence=3)
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS covered=2 missing=0 pending=0", result.stdout)

    def test_no_transition_is_unknown(self):
        self.ledger([])
        self.observation(5, 0, [])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)

    def test_malformed_and_corrupt_evidence_is_unknown(self):
        self.ledger(["open"])
        self.observation(5, 1, [(1, "active")])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)
        with (self.home / "feed").open("a", encoding="utf-8") as stream:
            stream.write("corrupt feed\n")
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)

    def test_count_gap_is_unknown(self):
        self.ledger(["open", "active"])
        self.observation(5, 1, [(1, "open"), (2, "active")])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)

    def test_invalid_ledger_timestamp_is_unknown_without_traceback(self):
        self.ledger(["open"])
        self.log.write_text(self.log.read_text(encoding="utf-8").replace("04:00:01Z", "04:99:99Z"),
                            encoding="utf-8")
        self.observation(5, 1, [(1, "open")])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN reason=ledger", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
