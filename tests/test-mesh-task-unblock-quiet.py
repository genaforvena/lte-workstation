#!/usr/bin/env python3
"""Unchanged resolver sweeps must never rewrite canonical task history."""
import copy
import fcntl
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
loader = importlib.machinery.SourceFileLoader("quiet_task", str(REPO / "scripts/mesh-task"))
spec = importlib.util.spec_from_loader(loader.name, loader)
task = importlib.util.module_from_spec(spec)
loader.exec_module(task)
from mesh_task_log import encode


class QuietSweepTests(unittest.TestCase):
    def resolver(self, status, **fields):
        return dict(chain="unblock/alpha/example", current=0, status=status,
                    dispatch="sent", unblock_attempt=1, created="2020-01-01T00:00:00Z",
                    steps=[dict(id="unblock/alpha/example/resolve", owner="alpha",
                                status="done" if status == "complete" else status,
                                next_update="2020-01-01T00:00:00Z")], **fields)

    def refresh(self, cover):
        with patch.object(task, "load", return_value=(Path("unused"), cover)), \
             patch.object(task, "save") as save, patch.object(task, "dispatch") as dispatch:
            task._refresh_unblock_resolver(cover["chain"], {"id": "parent/work"})
            return save.call_count, dispatch.call_count

    def test_unchanged_resolvers_never_append_even_without_recent_marker(self):
        for status in ("open", "active", "blocked", "complete"):
            for marker in (None, "2020-01-01T00:00:00Z"):
                with self.subTest(status=status, marker=marker):
                    cover = self.resolver(status)
                    if marker:
                        cover["unblock_reused_at"] = marker
                    before = copy.deepcopy(cover)
                    self.assertEqual(self.refresh(cover), (0, 0))
                    self.assertEqual(cover, before)

    def test_drained_rejection_and_cleared_completion_remain_unchanged(self):
        for status, fields in (("rejected", {"rejected_reason": "operator-drained"}),
                               ("complete", {"result": "unblock=cleared event=ready"})):
            cover = self.resolver(status)
            cover["steps"][0].update(fields)
            before = copy.deepcopy(cover)
            self.assertEqual(self.refresh(cover), (0, 0))
            self.assertEqual(cover, before)

    def test_future_retry_does_not_append(self):
        cover = self.resolver("rejected")
        with patch.object(task, "_unblock_retry_date", return_value=float("inf")):
            self.assertEqual(self.refresh(cover), (0, 0))

    def test_due_retry_is_saved_and_dispatched(self):
        cover = self.resolver("rejected")
        def append(_path, data, _step):
            data.update(status="open", dispatch="pending", unblock_attempt=2)
        with patch.object(task, "_unblock_retry_date", return_value=0), \
             patch.object(task, "_append_unblock_retry", side_effect=append) as retry:
            self.assertEqual(self.refresh(cover), (1, 1))
            retry.assert_called_once()

    def test_pending_dispatch_is_not_suppressed_by_recent_marker(self):
        cover = self.resolver("open", unblock_reused_at=task.now())
        cover["dispatch"] = "pending"
        self.assertEqual(self.refresh(cover), (0, 1))

    def test_scheduled_sweep_skips_when_another_sweep_holds_lock(self):
        with tempfile.TemporaryDirectory() as temp:
            with (Path(temp) / ".task-unblock-sweep.lock").open("w") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                result = subprocess.run(
                    ["bash", str(REPO / "scripts/mesh-task-unblock-sweep"), "--run"],
                    env=os.environ | {"MESH_DIR": temp, "MESH_UNBLOCK_SWEEP_DRY_RUN": "1"},
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("skip", result.stdout)
                self.assertNotIn("mesh-task route-unowned", result.stdout)

    def test_real_sweeps_leave_log_and_revisions_byte_identical(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = dict(version=2, chain="parent", current=0, status="blocked",
                          created="2020-01-01T00:00:00Z", steps=[dict(
                              id="parent/work", slug="work", owner="alpha", status="blocked",
                              description="wait for evidence", block_epoch=1,
                              blocker_type="external-event", needs="input", retry="event:ready")])
            cover = self.resolver("complete", version=2, unblock_parent="parent",
                                  unblock_step="parent/work", unblock_epoch=1)
            cover["steps"][0].update(slug="resolve", description="gate remains closed")
            log = root / "chat.log"
            log.write_text("".join("2020-01-01T00:00:00Z  fixture  ::  " + encode(state, 1) + "\n"
                                   for state in (parent, cover)))
            before = log.read_bytes()
            for _ in range(2):
                got = subprocess.run([sys.executable, str(REPO / "scripts/mesh-task"), "unblock-sweep"],
                                     env=os.environ | {"MESH_DIR": temp,
                                         "MESH_TASK_DIR": str(root / "chains"),
                                         "MESH_TASK_CHAT_CMD": "/bin/false",
                                         "MESH_TASK_HANDOFF_CMD": "/bin/false",
                                         "MESH_TASK_ACTOR": "witness"},
                                     text=True, capture_output=True, timeout=10)
                self.assertEqual(got.returncode, 0, got.stderr)
                self.assertIn("created=0", got.stdout)
                self.assertEqual(log.read_bytes(), before)

    def test_scheduled_routing_uses_the_configured_coordinator(self):
        with tempfile.TemporaryDirectory() as temp:
            script = '''
mesh-task(){
  if [ "$1" = route-unowned ]; then
    [ "${MESH_TASK_ACTOR:-}" = repair-coordinator ] || return 83
  fi
}
mesh-witness-task-autonomy(){ return 0; }
export -f mesh-task mesh-witness-task-autonomy
exec bash "$1" --run
'''
            got = subprocess.run(["bash", "-c", script, "test",
                                  str(REPO / "scripts/mesh-task-unblock-sweep")],
                                 env=os.environ | {"MESH_DIR": temp,
                                     "MESH_TASK_COORDINATOR": "repair-coordinator",
                                     "MESH_TASK_ACTOR": "mesh-task",
                                     "MESH_UNBLOCK_SWEEP_DRY_RUN": "0"},
                                 text=True, capture_output=True, timeout=5)
            self.assertEqual(got.returncode, 0, got.stderr)


if __name__ == "__main__":
    unittest.main()
