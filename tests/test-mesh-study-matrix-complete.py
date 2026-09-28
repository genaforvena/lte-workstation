#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


CHECK = Path(__file__).resolve().parents[1] / "scripts/mesh-study-matrix-complete"


class CompleteTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.study = Path(self.temp.name) / "study"
        self.root = self.study / "runs/fleet-study-v1"
        self.root.mkdir(parents=True)
        corpus = self.study / "corpus/study-v1"
        corpus.mkdir(parents=True)
        (corpus / "heldout.jsonl").write_text('{"case_id":"c1"}\n')
        (self.root / "registration.json").write_text(json.dumps({
            "study_id": "fleet-study-v1", "arms": [{"id": "base"}],
            "statistics": {"seeds": [17]},
        }))

    def check(self):
        return subprocess.run([str(CHECK), str(self.root)], capture_output=True, text=True)

    def complete(self):
        sub = self.root / "seed-17/base/base"
        sub.mkdir(parents=True)
        tape = sub / "predictions-base.jsonl"
        tape.write_text('{"case_id":"c1","seed":17,"arm":"base"}\n')
        digest = hashlib.sha256(tape.read_bytes()).hexdigest()
        execution = {"arm": "base", "records": 1, "records_sha256": digest,
                     "predictions": str(tape)}
        (self.root / "smoke-summary.json").write_text(json.dumps({
            "schema": "tiny-fleet.study-matrix-smoke/v1", "study_id": "fleet-study-v1",
            "verification_only": False, "training_executed": True, "max_cases": None,
            "rows": 1, "skipped": [], "arms": ["base"], "seeds": [17],
            "summaries": [{"registered_arm": "base", "seed": 17,
                           "verification_only": False, "execution": [execution]}],
        }))
        return tape

    def test_missing_summary_is_incomplete(self):
        self.assertEqual(self.check().returncode, 1)

    def test_valid_matrix_is_complete(self):
        self.complete()
        self.assertEqual(self.check().returncode, 0)

    def test_changed_tape_is_unknown(self):
        tape = self.complete()
        tape.write_text('{"case_id":"c1","seed":17,"arm":"base","new":1}\n')
        self.assertEqual(self.check().returncode, 2)

    def test_partial_tape_is_unknown(self):
        tape = self.complete()
        tape.write_text('')
        self.assertEqual(self.check().returncode, 2)


if __name__ == "__main__":
    unittest.main()
