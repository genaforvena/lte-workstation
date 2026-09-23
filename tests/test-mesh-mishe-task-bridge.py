#!/usr/bin/env python3
"""Task-ledger bridge replay and privacy checks, without touching the live feed."""
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


def row(status, secret="secret-task-id-and-path"):
    return (f"2026-09-23T06:32:00Z [task-ledger] /chain=s:{secret} | /current=i:0 | "
            f"/status=s:{status} | /steps/0/owner=s:cleaner | /steps/0/status=s:{status}\n")


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.log = self.base / "chat.log"
        self.log.write_text("unrelated baseline\n", encoding="utf-8")
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home),
                    "MESH_MISHE_CHAT_LOG": str(self.log), "MESH_MISHE_CORE": str(CORE)}

    def bridge(self, mode):
        return subprocess.run(["python3", str(ROOT / "scripts/mesh-mishe-task-bridge"), mode],
                              env=self.env, text=True, capture_output=True)

    def feed(self):
        from mishe_tauftauf.feed import Feed
        return [e for e in Feed(self.home).entries() if e.source == "observation/cleaner-task"]

    def test_transient_burst_replay_and_privacy(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        self.assertIn("no-transition", self.bridge("check").stdout)
        with self.log.open("a", encoding="utf-8") as stream:
            for status in ("open", "active", "complete"):
                stream.write(row(status))
        pending = self.bridge("check")
        self.assertEqual(pending.returncode, 2)
        self.assertIn("reason=pending", pending.stdout)
        result = self.bridge("once")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([e.body for e in self.feed()], [
            f"cleaner task-ledger epoch={i} status={status}"
            for i, status in enumerate(("open", "active", "complete"), 2)])
        raw = (self.home / "feed").read_text()
        for receipt in self.feed():
            self.assertIn(f"entry {receipt.sequence} for top-pain cleaner: wake", raw)
            self.assertIn(f"wake requested top-pain cleaner for entry {receipt.sequence}", raw)
        self.assertEqual(self.bridge("check").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            for i in range(20):
                stream.write(row("open" if i % 2 == 0 else "complete"))
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(len(self.feed()), 23)
        self.assertNotIn("secret-task-id-and-path", (self.home / "feed").read_text())
        state = self.home / "cleaner-task-bridge.json"
        saved = json.loads(state.read_text())
        saved["epoch"] = 1
        saved["offset"] = len("unrelated baseline\n")
        saved["last_hash"] = __import__("hashlib").sha256(b"unrelated baseline\n").hexdigest()
        saved["last_len"] = len("unrelated baseline\n")
        saved["event_count"] = 0
        state.write_text(json.dumps(saved))
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(len(self.feed()), 23)
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(len(self.feed()), 23)

    def test_gate_rejects_missing_event_count(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open"))
        self.assertEqual(self.bridge("once").returncode, 0)
        state = self.home / "cleaner-task-bridge.json"
        saved = json.loads(state.read_text())
        saved["event_count"] += 1
        state.write_text(json.dumps(saved))
        self.assertIn("feed-count", self.bridge("check").stdout)

    def test_malformed_and_rewind_fail_closed(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open"))
            stream.write(row("bogus"))
        result = self.bridge("once")
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)
        self.assertEqual(len(self.feed()), 0)
        self.log.write_text("short\n", encoding="utf-8")
        self.assertEqual(self.bridge("once").returncode, 2)

    def test_duplicate_epoch_does_not_reveal_secret(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write("2026-09-23T06:32:00Z [task-ledger] /chain=s:secret | "
                         "/steps/0/owner=s:cleaner | /status=s:open\n")
        result = self.bridge("once")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("secret", result.stdout)

    def test_interrupted_receipts_are_replayed_without_duplicates(self):
        from mishe_tauftauf.feed import Feed
        from mishe_tauftauf.runtime import DISPOSITION_RE, is_bookkeeping

        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open"))
            stream.write(row("active"))
        feed = Feed(self.home)
        first = feed.append_runtime_once("observation/cleaner-task", "cleaner task-ledger epoch=2 status=open")
        second = feed.append_runtime_once("observation/cleaner-task", "cleaner task-ledger epoch=3 status=active")
        feed.append_runtime_once("mishe-tauftauf", f"entry {first.sequence} for top-pain cleaner: wake")
        self.assertEqual(self.bridge("check").returncode, 2)
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(self.bridge("check").returncode, 0)
        all_entries = feed.entries()
        for event in (first, second):
            self.assertFalse(is_bookkeeping(event))
            self.assertEqual(sum(e.body == event.body and e.source == event.source for e in all_entries), 1)
            disposition = f"entry {event.sequence} for top-pain cleaner: wake"
            request = f"wake requested top-pain cleaner for entry {event.sequence}"
            self.assertEqual(sum(e.body == disposition and e.source == "mishe-tauftauf" for e in all_entries), 1)
            self.assertEqual(sum(e.body == request and e.source == "mishe-tauftauf" for e in all_entries), 1)
            self.assertEqual(DISPOSITION_RE.findall(disposition), [(str(event.sequence), "cleaner", "wake")])
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(len(feed.entries()), len(all_entries))


if __name__ == "__main__":
    unittest.main()
