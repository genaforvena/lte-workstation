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
        self.assertIn("no-new-intent", self.bridge("check").stdout)
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
        for receipt in self.feed()[:1]:
            self.assertIn(f"entry {receipt.sequence} for top-pain cleaner: wake", raw)
            self.assertIn(f"wake requested top-pain cleaner for entry {receipt.sequence}", raw)
        for receipt in self.feed()[1:]:
            self.assertNotIn(f"entry {receipt.sequence} for top-pain cleaner: wake", raw)
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
        self.assertEqual(self.bridge("once").returncode, 2)
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

    def test_non_object_state_fails_closed(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        state = self.home / "cleaner-task-bridge.json"
        state.write_text("null\n")
        result = self.bridge("once")
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN reason=state", result.stdout)
        self.assertEqual(result.stderr, "")

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
            self.assertEqual(sum(e.body == disposition and e.source == "mishe-tauftauf" for e in all_entries), int(event == first))
            self.assertEqual(sum(e.body == request and e.source == "mishe-tauftauf" for e in all_entries), int(event == first))
            self.assertEqual(DISPOSITION_RE.findall(disposition), [(str(event.sequence), "cleaner", "wake")])
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(len(feed.entries()), len(all_entries))

    def test_one_intent_per_chain_and_two_distinct_openings(self):
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            for chain, status in (("private-A", "open"), ("private-A", "open"),
                                  ("private-A", "active"), ("private-B", "open"),
                                  ("private-A", "complete"), ("private-B", "blocked"),
                                  ("private-A", "open")):
                stream.write(row(status, chain))
        self.assertEqual(self.bridge("once").returncode, 0)
        all_events = self.feed()
        self.assertEqual(len(all_events), 7)
        raw = (self.home / "feed").read_text()
        intents = [event.sequence for event in all_events if
                   f"entry {event.sequence} for top-pain cleaner: wake" in raw]
        self.assertEqual(intents, [all_events[0].sequence, all_events[3].sequence,
                                   all_events[6].sequence])
        self.assertEqual(self.bridge("check").returncode, 0)
        state = (self.home / "cleaner-task-bridge.json").read_text()
        self.assertNotIn("private-A", raw + state)
        self.assertNotIn("private-B", raw + state)
        from mishe_tauftauf.feed import Feed
        Feed(self.home).append_runtime_once("mishe-tauftauf",
                                            f"entry {all_events[1].sequence} for top-pain cleaner: wake")
        self.assertIn("route-receipt", self.bridge("check").stdout)

    def test_v1_migration_reconstructs_seen_chains_without_new_intents(self):
        from mishe_tauftauf.feed import Feed
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open", "old-secret"))
            stream.write(row("open", "old-secret"))
        feed = Feed(self.home)
        for epoch, status in ((2, "open"), (3, "open")):
            receipt = feed.append_runtime_once("observation/cleaner-task", f"cleaner task-ledger epoch={epoch} status={status}")
            feed.append_runtime_once("mishe-tauftauf", f"entry {receipt.sequence} for top-pain cleaner: wake")
            feed.append_runtime_once("mishe-tauftauf", f"wake requested top-pain cleaner for entry {receipt.sequence}")
        # v1 cursor reflects both events; v1 emitted wake receipts for each.
        state_path = self.home / "cleaner-task-bridge.json"
        state = json.loads(state_path.read_text())
        lines = self.log.read_bytes().splitlines(keepends=True)
        state.update(epoch=3, offset=sum(map(len, lines)),
                     last_len=len(lines[-1]), last_hash=__import__("hashlib").sha256(lines[-1]).hexdigest(),
                     event_count=2)
        state = {key: value for key, value in state.items()
                 if key not in {"salt", "chain_status", "intent_epochs", "legacy_through_epoch", "baseline_offset"}}
        state["version"] = 1
        state_path.write_text(json.dumps(state))
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open", "old-secret"))
            stream.write(row("open", "new-secret"))
        self.assertEqual(self.bridge("once").returncode, 0)
        all_events = self.feed()
        self.assertEqual(len(all_events), 4)
        raw = (self.home / "feed").read_text()
        self.assertNotIn(f"entry {all_events[2].sequence} for top-pain cleaner: wake", raw)
        self.assertIn(f"entry {all_events[3].sequence} for top-pain cleaner: wake", raw)
        self.assertNotIn("old-secret", raw + state_path.read_text())
        self.assertNotIn("new-secret", raw + state_path.read_text())
        self.assertEqual(self.bridge("check").returncode, 0)

    def test_v1_migration_rejects_ambiguous_feed(self):
        from mishe_tauftauf.feed import Feed
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open", "private-A"))
        feed = Feed(self.home)
        feed.append_runtime_once("observation/cleaner-task", "cleaner task-ledger epoch=2 status=active")
        result = self.bridge("once")
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN", result.stdout)
        self.assertNotIn("private-A", result.stdout)

    def test_migration_waits_for_new_cycle_and_gate_audits_intents(self):
        from mishe_tauftauf.feed import Feed
        self.assertEqual(self.bridge("baseline").returncode, 0)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open", "private-A"))
        feed = Feed(self.home)
        old = feed.append_runtime_once("observation/cleaner-task", "cleaner task-ledger epoch=2 status=open")
        feed.append_runtime_once("mishe-tauftauf", f"entry {old.sequence} for top-pain cleaner: wake")
        feed.append_runtime_once("mishe-tauftauf", f"wake requested top-pain cleaner for entry {old.sequence}")
        state_path = self.home / "cleaner-task-bridge.json"
        state = json.loads(state_path.read_text())
        last = row("open", "private-A").encode()
        state.update(version=1, epoch=2, offset=self.log.stat().st_size,
                     event_count=1, last_len=len(last),
                     last_hash=__import__("hashlib").sha256(last).hexdigest())
        for key in ("salt", "chain_status", "intent_epochs", "legacy_through_epoch", "baseline_offset"):
            del state[key]
        state_path.write_text(json.dumps(state))
        self.assertIn("migration-required", self.bridge("check").stdout)
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertIn("no-new-intent", self.bridge("check").stdout)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("open", "private-A"))
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertIn("no-new-intent", self.bridge("check").stdout)
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(row("blocked", "private-A"))
            stream.write(row("open", "private-A"))
        self.assertEqual(self.bridge("once").returncode, 0)
        self.assertEqual(self.bridge("check").returncode, 0)
        state = json.loads(state_path.read_text())
        state["intent_epochs"] = [3]
        state_path.write_text(json.dumps(state))
        self.assertIn("ledger-intents", self.bridge("check").stdout)


if __name__ == "__main__":
    unittest.main()
