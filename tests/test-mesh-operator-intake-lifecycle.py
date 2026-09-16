#!/usr/bin/env python3
"""Drive the real intake -> mesh-task -> canonical replay boundary in isolation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/mesh-operator-intake"
sys.path.insert(0, str(REPO / "scripts"))
from mesh_task_log import replay


class IntakeLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.mesh = Path(self.tmp.name)
        self.voice = self.mesh / "voice-in.log"
        self.chat = self.mesh / "chat.log"
        self.chat.write_text("")
        self.stamp = (datetime.now(timezone.utc) - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.voice.write_text(f"{self.stamp}  TEXT  do work\n")
        self.env = dict(os.environ, MESH_DIR=str(self.mesh), MESH_TASK_DIR=str(self.mesh / "task-chains"),
                        MESH_CHAT_LOG=str(self.chat), MESH_TASK_CHAT_CMD="/bin/true",
                        MESH_TASK_HANDOFF_CMD="/bin/true")
        for key in list(self.env):
            if key.startswith("MESH_OPERATOR_INTAKE_"):
                del self.env[key]

    def run_tool(self, *args, **extra):
        return subprocess.run([sys.executable, str(SCRIPT), *args], env=dict(self.env, **extra),
                              text=True, capture_output=True, timeout=15)

    def test_canonical_idempotence_and_filter_key(self):
        first = self.run_tool()
        self.assertEqual(first.returncode, 0, first.stderr)
        records = replay(self.chat)
        self.assertEqual(len(records), 1)
        ask = next(iter(records.values()))["data"]["ask"]
        digest = hashlib.sha256(self.voice.read_bytes().rstrip(b"\n")).hexdigest()[:24]
        self.assertEqual(ask, "tg-" + digest)
        before = self.chat.read_bytes()
        second = self.run_tool()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.chat.read_bytes(), before)
        state = json.loads((self.mesh / "operator-intake/status.json").read_text())
        self.assertEqual(state["created"], 0)
        self.assertEqual(state["missing"], 0)
        self.assertIsNone(state["oldest_gap"])
        description = next(iter(records.values()))["data"]["steps"][0]["description"]
        self.assertIn("subagents", description)
        self.assertIn("Do not resend", description)
        step = next(iter(records.values()))["data"]["steps"][0]
        self.assertEqual(step["tags"], "audit-followthrough")
        self.assertIn(".findings.json", description)

    def test_event_mode_is_quiet_when_source_unchanged(self):
        self.assertEqual(self.run_tool('--event').returncode, 0)
        path = self.mesh / 'operator-intake/status.json'
        state = json.loads(path.read_text())
        state['run'] = '2020-01-01T00:00:00Z'
        path.write_text(json.dumps(state))
        self.assertEqual(json.loads(self.run_tool('--status').stdout)['health'], 'OK')
        with self.voice.open('a') as handle:
            handle.write(f'{self.stamp}  TEXT  another\n')
        self.assertEqual(json.loads(self.run_tool('--status').stdout)['health'], 'PENDING')
        os.utime(self.voice, (1, 1))
        self.assertEqual(json.loads(self.run_tool('--status').stdout)['health'], 'STALE')

    def test_event_mode_retries_backlog_and_has_no_grace_loss(self):
        stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.voice.write_text(''.join(f'{stamp}  TEXT  item {i}\n' for i in range(2)))
        first = self.run_tool('--event', MESH_OPERATOR_INTAKE_BATCH='1')
        self.assertNotEqual(first.returncode, 0)
        self.assertEqual(json.loads(first.stdout)['missing'], 1)
        self.assertEqual(self.run_tool('--event').returncode, 0)

    def test_replaced_source_with_same_metadata_is_pending(self):
        self.assertEqual(self.run_tool('--event').returncode, 0)
        prior = self.voice.stat()
        replacement = self.mesh / 'replacement'
        replacement.write_bytes(self.voice.read_bytes().replace(b'do work', b'new job'))
        os.utime(replacement, ns=(prior.st_atime_ns, prior.st_mtime_ns))
        replacement.replace(self.voice)
        self.assertEqual(json.loads(self.run_tool('--status').stdout)['health'], 'PENDING')
        self.assertEqual(self.run_tool('--event').returncode, 0)
        self.assertEqual(len(replay(self.chat)), 2)

    def test_same_second_distinct_inputs_and_batch_bound(self):
        self.voice.write_text("".join(f"{self.stamp}  TEXT  message {i}\n" for i in range(3)))
        result = self.run_tool(MESH_OPERATOR_INTAKE_BATCH="2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(replay(self.chat)), 2)
        result = self.run_tool(MESH_OPERATOR_INTAKE_BATCH="2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(replay(self.chat)), 3)

    def test_unreadable_input_is_loud_and_no_task_is_created(self):
        self.voice.unlink()
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        state = json.loads((self.mesh / "operator-intake/status.json").read_text())
        self.assertEqual(state["health"], "UNKNOWN")
        self.assertIn("RUN health=UNKNOWN", (self.mesh / "operator-intake/run.log").read_text())
        self.assertEqual(self.chat.read_text(), "")

    def test_ledger_failure_is_logged_and_never_repaired(self):
        self.chat.unlink()
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RUN health=UNKNOWN", (self.mesh / "operator-intake/run.log").read_text())
        self.assertFalse((self.mesh / "operator-intake/plans").exists())

    def test_failed_creates_are_bounded_and_not_healthy(self):
        self.voice.write_text("".join(f"{self.stamp}  TEXT  message {i}\n" for i in range(5)))
        result = self.run_tool(MESH_OPERATOR_INTAKE_BATCH="2", MESH_OPERATOR_INTAKE_TASK="/bin/false")
        self.assertNotEqual(result.returncode, 0)
        state = json.loads((self.mesh / "operator-intake/status.json").read_text())
        self.assertEqual(state["health"], "DEGRADED")
        self.assertEqual(state["attempted"], 2)

    def test_dry_run_and_grace(self):
        result = self.run_tool("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.mesh / "operator-intake").exists())
        self.assertEqual(self.chat.read_text(), "")
        self.voice.write_text(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "  TEXT  new\n")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.chat.read_text(), "")

    def test_persisted_floor_survives_downtime(self):
        self.assertEqual(self.run_tool().returncode, 0)
        before = (self.mesh / "operator-intake/bootstrap-floor").read_bytes()
        # Restart with a shorter bootstrap window must still see the original backlog.
        with self.voice.open("a") as handle:
            handle.write(f"{self.stamp}  DOCUMENT  second source\n")
        result = self.run_tool(MESH_OPERATOR_INTAKE_BOOTSTRAP_HOURS="0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(replay(self.chat)), 2)
        self.assertEqual((self.mesh / "operator-intake/bootstrap-floor").read_bytes(), before)

    def test_partial_source_waits_for_completed_line(self):
        self.voice.write_text(f"{self.stamp}  TEXT  unfinished")
        self.assertEqual(self.run_tool().returncode, 0)
        self.assertEqual(self.chat.read_text(), "")

    def test_stale_status_is_unknown_not_healthy(self):
        self.assertEqual(self.run_tool().returncode, 0)
        status = self.mesh / "operator-intake/status.json"
        state = json.loads(status.read_text())
        state["run"] = "2000-01-01T00:00:00Z"
        status.write_text(json.dumps(state))
        result = self.run_tool("--status")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["health"], "STALE")


if __name__ == "__main__":
    unittest.main()
