#!/usr/bin/env python3
# Verify cross-chain saves cannot certify stale fast-position caches.
"""A save may certify its own chain, never unrelated stale cache files."""
import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mesh_task_fastpos", str(ROOT / "scripts/mesh-task"))
spec = importlib.util.spec_from_loader(loader.name, loader)
task = importlib.util.module_from_spec(spec)
loader.exec_module(task)


class Fastpos(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        task.ROOT = Path(self.temp.name)
        task.CHAINS = task.ROOT / "task-chains"
        task.CHAINS.mkdir()
        self.log = task.ROOT / "chat.log"
        self.log.touch()

    def data(self, chain):
        return dict(chain=chain, current=0, status="open", created="2026-09-19T00:00:00Z", steps=[
            dict(id=f"{chain}/work", slug="work", owner="alpha", status="open", description="work")])

    def append(self, data, revision):
        with self.log.open("a") as stream:
            stream.write("2026-09-19T00:00:00Z alpha@fixture :: " + task.encode_task_state(data, revision) + "\n")

    def certify(self, data, revision):
        task.path_for(data["chain"]).write_text(json.dumps(data))
        task.note_fastpos(data["chain"], revision)

    def test_external_append_then_other_save_does_not_recognize_stale_chain(self):
        first = self.data("first")
        self.append(first, 1)
        self.certify(first, 1)
        self.assertEqual(task.fast_chain_record("first")["revision"], 1)
        changed = copy.deepcopy(first)
        changed["steps"][0]["description"] = "fresh canonical description"
        self.append(changed, 2)
        self.assertIsNone(task.fast_chain_record("first"))
        second = self.data("second")
        self.append(second, 1)
        self.certify(second, 1)
        self.assertIsNone(task.fast_chain_record("first"))
        self.assertEqual(task.fast_chain_record("second")["data"], second)
        task._records = None
        _, loaded = task.load("first")
        self.assertEqual(loaded, changed)

    def test_malformed_sidecar_is_disposable(self):
        (task.CHAINS / ".fastpos.json").write_text("[]")
        self.assertIsNone(task.fast_chain_record("missing"))

    def test_legacy_multi_chain_certificate_is_not_trusted(self):
        first = self.data("first")
        self.append(first, 1)
        task.path_for("first").write_text(json.dumps(first))
        stat = self.log.stat()
        (task.CHAINS / ".fastpos.json").write_text(json.dumps({
            "rev": {"first": 1, "second": 7},
            "log": {"ino": stat.st_ino, "size": stat.st_size, "mtime_ns": stat.st_mtime_ns},
        }))
        self.assertIsNone(task.fast_chain_record("first"))


if __name__ == "__main__":
    unittest.main()
