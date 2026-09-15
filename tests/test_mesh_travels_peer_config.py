#!/usr/bin/env python3
"""Fixture-level tests for mesh-travels node-local SSH configuration."""
import contextlib
import importlib.util
from importlib.machinery import SourceFileLoader
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mesh-travels"


def load_script():
    loader = SourceFileLoader("mesh_travels_fixture", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MeshTravelsPeerConfigTest(unittest.TestCase):
    def test_reads_peer_and_remote_log_from_node_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            mesh = Path(tmp) / ".mesh"
            mesh.mkdir()
            (mesh / "nodes").write_text(
                'MESH_TRAVELS_PEER="travel-user@fixture-peer"\n'
                'MESH_TRAVELS_REMOTE_LOG="/fixture/phone-track.jsonl"\n'
            )
            env = {"HOME": tmp}
            with mock.patch.dict(os.environ, env, clear=True):
                module = load_script()
                completed = subprocess.CompletedProcess([], 0, "fixture line\n", "")
                with mock.patch.object(module.subprocess, "run", return_value=completed) as run:
                    self.assertEqual(module.pull_log(), ["fixture line"])
            command = run.call_args.args[0]
            self.assertEqual(command[-2], "travel-user@fixture-peer")
            self.assertEqual(command[-1], "cat /fixture/phone-track.jsonl 2>/dev/null")

    def test_missing_peer_fails_closed_without_ssh(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, ".mesh").mkdir()
            with mock.patch.dict(os.environ, {"HOME": tmp}, clear=True):
                module = load_script()
                err = io.StringIO()
                with mock.patch.object(module.subprocess, "run") as run:
                    with contextlib.redirect_stderr(err):
                        self.assertEqual(module.pull_log(), [])
                run.assert_not_called()
                self.assertIn("MESH_TRAVELS_PEER", err.getvalue())


if __name__ == "__main__":
    unittest.main()
