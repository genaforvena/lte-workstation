#!/usr/bin/env python3
"""Consumer-visible cleaner report checks; all paths stay inside a temporary fixture."""
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cleaner/mesh-cleaner-mishe"
loader = importlib.machinery.SourceFileLoader("mesh_cleaner_mishe", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
pilot = importlib.util.module_from_spec(spec)
loader.exec_module(pilot)


class CleanerReportBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.repo = root / "repo"
        self.repo.mkdir()
        self.mesh = root / "mesh"
        (self.mesh / "cleaner").mkdir(parents=True)
        self.evidence = root / "evidence"
        old = (pilot.REPO, pilot.MESH, pilot.EVIDENCE)
        pilot.REPO, pilot.MESH, pilot.EVIDENCE = self.repo, self.mesh, self.evidence
        self.addCleanup(lambda: setattr(pilot, "REPO", old[0]))
        self.addCleanup(lambda: setattr(pilot, "MESH", old[1]))
        self.addCleanup(lambda: setattr(pilot, "EVIDENCE", old[2]))
        self.rows = [
            {"path": "scripts/live", "git": "M", "bytes": 7, "mtime_utc": "2026-09-24T00:00:00Z",
             "reasons": ["protected-root"]},
            {"path": "notes.txt", "git": "??", "bytes": 5, "mtime_utc": "2026-09-24T00:00:01Z",
             "reasons": ["review-required"]},
        ]
        self.scan = {"version": 1, "repository": str(self.repo), "scan_id": "sample",
                     "head": "abc", "candidate_count": 2, "candidates": self.rows}
        self.settle = {"version": 1, "scan_id": "sample", "apply": False, "mutations": 0,
                       "outcomes": [{"path": r["path"], "status": "held"} for r in self.rows]}
        self.flush()

    def flush(self):
        (self.mesh / "cleaner/latest.json").write_text(json.dumps(self.scan))
        (self.mesh / "cleaner/settle-latest.json").write_text(json.dumps(self.settle))

    def packet(self):
        identity, _, raw_scan, raw_settle, _ = pilot.snapshot()
        for label, raw in (("scan", raw_scan), ("settle", raw_settle)):
            pilot.immutable(self.evidence / "sources" / f"{label}-{pilot.digest(raw)}.json", raw)
        return {"inventory_sha256": identity,
                "source_scan_sha256": pilot.digest(raw_scan),
                "source_settle_sha256": pilot.digest(raw_settle),
                "candidates": [
                    {"path": "scripts/live", "disposition": "hold-protected",
                     "reason": "protected-root is active code, owner unverified",
                     "next_check": "Read current owner task before considering it"},
                    {"path": "notes.txt", "disposition": "hold-review",
                     "reason": "untracked note is not proven disposable",
                     "next_check": "Find an owner or prior disposition receipt"},
                ]}

    def test_current_full_review_and_changed_live_inventory(self):
        with self.assertRaises(FileNotFoundError):
            pilot.checked()
        packet = self.packet()
        pilot.immutable(pilot.packet_path(packet["inventory_sha256"]), pilot.encoded(packet))
        self.assertEqual(pilot.checked()[2], 2)
        self.scan["scan_id"] = self.settle["scan_id"] = "later"
        self.flush()
        self.assertEqual(pilot.checked()[2], 2)  # New scan, same evidence-bearing state.
        self.scan["candidates"][1]["bytes"] = 6
        self.flush()
        with self.assertRaises(FileNotFoundError):
            pilot.checked()  # A genuine inventory change needs a new review.

    def test_missing_row_delete_and_mismatched_sources_never_pass(self):
        packet = self.packet()
        identity, rows, _, _, _ = pilot.snapshot()
        packet["candidates"].pop()
        with self.assertRaises(ValueError):
            pilot.validate(packet, identity, rows)
        packet = self.packet()
        packet["candidates"][0]["disposition"] = "quarantine"
        with self.assertRaises(ValueError):
            pilot.validate(packet, identity, rows)
        packet = self.packet()
        unrelated = b'{}\n'
        pilot.immutable(self.evidence / "sources" / f"scan-{hashlib.sha256(unrelated).hexdigest()}.json", unrelated)
        packet["source_scan_sha256"] = hashlib.sha256(unrelated).hexdigest()
        with self.assertRaises((AttributeError, ValueError)):
            pilot.validate(packet, identity, rows)

    def test_stale_or_applying_settlement_cannot_be_called_reviewed(self):
        self.settle["scan_id"] = "older"
        self.flush()
        with self.assertRaises(ValueError):
            pilot.snapshot()
        self.settle["scan_id"] = "sample"
        self.settle["apply"] = True
        self.flush()
        with self.assertRaises(ValueError):
            pilot.snapshot()


if __name__ == "__main__":
    unittest.main()
