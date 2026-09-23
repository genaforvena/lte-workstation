#!/usr/bin/env python3
"""Reconciliation gates use synthetic live observations and the real caller scan."""

import importlib.machinery
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
channels = importlib.machinery.SourceFileLoader("channels", str(ROOT / "scripts/mesh-mishe-channels")).load_module()


class RosterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.env = root / "restore.env"
        self.env.write_text('export MESH_MIND_CHANNELS="wrong"\n'
                            'export MESH_MIND_CHANNELS="cleaner tiny-fleet"\n'
                            'export MESH_CONSUME_CHANNELS="cleaner:60"\n'
                            'export MESH_RETIRED_CHANNELS="diary"\n'
                            'export MESH_PRIMARY_MIND_CMD="omp --model test"\n')
        self.restore = root / "restore"
        self.restore.write_text('ensure_uniform_channel cleaner cleaner "$PRIMARY_MIND_TYPE" "$PRIMARY_MIND_CMD"\n')
        self.charters = root / "charter"
        self.charters.mkdir()
        (self.charters / "cleaner.md").write_text("# cleaner\n")
        self.card = root / "card"
        self.card.write_text("capabilities:\n  minds: omp codex\n")
        self.scripts = root / "scripts"
        self.scripts.mkdir()
        self.mesh = root / "mesh"
        self.mesh.mkdir()
        self.args = SimpleNamespace(env=self.env, restore=self.restore, charters=self.charters,
                                    card=self.card, scripts=self.scripts, mesh=self.mesh, session="test")
        self.lease = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.windows = "cleaner|2\n"
        self.process = "bash /bin/mesh-pane-consume cleaner --interval 60\n"
        self.top = f"-- pane live {self.lease} --\n"
        self.bottom = "bash -lc 'omp --model test'"
        self.tasks = "cleaner\ttask\topen\t1\n"

    def run_fake(self, *argv):
        if argv[:2] == ("hostname",):
            return "test\n"
        if argv[:2] == ("tmux", "list-windows"):
            return self.windows
        if argv[:2] == ("tmux", "display-message"):
            return "exec mesh-dash cleaner" if str(argv[3]).endswith(".0") else self.bottom
        if argv[:2] == ("tmux", "capture-pane"):
            return self.top
        if argv[:2] == ("ps", "-eo"):
            return self.process
        if argv[:3] == ("mesh-task", "queue", "--dispatch"):
            return self.tasks
        return ""

    def snapshot(self):
        with patch.object(channels, "run", side_effect=self.run_fake):
            return channels.inventory(self.args)

    def test_effective_last_export_and_inactive_lane(self):
        result = self.snapshot()
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertEqual([row["channel"] for row in result["channels"]], ["cleaner", "tiny-fleet"])
        self.assertEqual(result["channels"][1]["state"], "configured-inactive")
        self.assertEqual(result["channels"][0]["renderer_command"], "exec mesh-dash cleaner")
        self.assertFalse(result["channels"][1]["launch_allowed"])
        self.assertEqual(result["channels"][0]["exact_owner_queued_tasks"], 1)

    def test_restore_tmux_process_disagreement(self):
        self.process = ""
        self.assertIn("no consumer process", " ".join(self.snapshot()["errors"]))
        self.process = "bash /bin/mesh-pane-consume cleaner --interval 60\n"
        self.windows = ""
        self.assertIn("no live two-pane window", " ".join(self.snapshot()["errors"]))
        self.windows = "cleaner|2\n"
        self.restore.write_text("")
        self.assertIn("unknown configured channel", " ".join(self.snapshot()["errors"]))

    def test_missing_charter_engine_and_stale_pane(self):
        (self.charters / "cleaner.md").unlink()
        self.bottom = "bash -l"
        self.top = "-- pane live 2020-01-01T00:00:00Z --\n"
        result = self.snapshot()
        errors = " ".join(result["errors"])
        self.assertIn("missing charter", errors)
        self.assertIn("mind engine absent", errors)
        self.assertIn("stale top-pane", errors)
        self.assertFalse(result["channels"][0]["launch_allowed"])

    def test_unknown_duplicate_and_direct_caller(self):
        self.env.write_text(self.env.read_text() + 'export MESH_MIND_CHANNELS="cleaner cleaner"\n')
        self.assertIn("duplicate configured", " ".join(self.snapshot()["errors"]))
        self.env.write_text(self.env.read_text().replace("cleaner cleaner", "cleaner unknown"))
        self.assertIn("unknown configured channel", " ".join(self.snapshot()["errors"]))
        source = self.scripts / "mesh-feed"
        source.write_text("#!/bin/sh\nmesh-tell cleaner read\n")
        source.chmod(0o755)
        callers = channels.caller_inventory(self.scripts, self.mesh)
        self.assertEqual(callers[0]["class"], "sensor/peer event")
        self.assertEqual(callers[0]["lines"], [2])

    def test_unowned_task_fails_closed(self):
        self.tasks = "\ttask\topen\t1\n"
        self.assertIn("unowned task", " ".join(self.snapshot()["errors"]))
        self.tasks = None
        self.assertIn("journal unavailable", " ".join(self.snapshot()["errors"]))

    def test_live_derived_roster_fixture(self):
        fixture = json.loads((ROOT / "tests/fixtures/mesh-mishe-roster-20260923.json").read_text())
        self.assertEqual(len(fixture["active"]), 17)
        self.assertEqual(len(set(fixture["active"])), 17)
        self.assertTrue(set(fixture["active"]).isdisjoint(fixture["retired"]))
        self.assertEqual(fixture["configured_inactive"], ["tiny-fleet"])

    def test_tall_pane_lease_capture(self):
        self.top = "\n".join(["data"] * 25 + [f"-- pane live: as of {self.lease} --"] + [""] * 25)
        with patch.object(channels, "run", side_effect=self.run_fake) as fake:
            self.assertEqual(channels.inventory(self.args)["status"], "PASS")
        captures = [call.args for call in fake.call_args_list if call.args[:2] == ("tmux", "capture-pane")]
        self.assertTrue(all("-100" in call for call in captures))


if __name__ == "__main__":
    unittest.main()
