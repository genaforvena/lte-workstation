#!/usr/bin/env python3
"""Offline fleet S1 trial refuses unreviewed and non-S0-bound evidence."""
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("fleet_s1_trial", str(ROOT / "scripts/mesh-mishe-fleet-s1-trial"))
spec = importlib.util.spec_from_loader(loader.name, loader)
trial = importlib.util.module_from_spec(spec)
loader.exec_module(trial)


class FleetS1TrialTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "evidence"
        self.root.mkdir(mode=0o700)
        self.cases = self.root / "cases"
        self.cases.mkdir(mode=0o700)
        self.review = self.root / "review.json"
        self.output = self.root / "report.json"
        self.old_core = os.environ.get("MESH_MISHE_CORE")
        os.environ["MESH_MISHE_CORE"] = str(Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf")))
        self.addCleanup(self.restore_core)

    def restore_core(self):
        if self.old_core is None:
            os.environ.pop("MESH_MISHE_CORE", None)
        else:
            os.environ["MESH_MISHE_CORE"] = self.old_core

    def add_case(self, number, *, phase="s0_projection_hash_matched", label="no", group=None):
        case_id = f"{number:020d}-{'a' * 16}"
        directory = self.cases / case_id
        directory.mkdir(mode=0o700)
        sources = directory / "sources"
        sources.mkdir(mode=0o700)
        raw = f"producer-{number}".encode()
        (sources / "0").write_bytes(raw)
        (sources / "0").chmod(0o600)
        projected = ("STATE: RED\nOBSERVATION: source=top-pane/check freshness=fresh "
                     "goal=fresh value-coverage=partial semantic=fleet-health:stale "
                     "signal=aaaaaaaaaaaaaaaa\n")
        event_id = "a" * 64
        source_digest = trial.digest(trial.digest(raw).encode())
        bound = {"version": 1, "tick": "b" * 32, "event_id": event_id,
                 "channel": "health", "projected_sha256": trial.digest(projected.encode()),
                 "sources": [{"origin": str(sources / "0"), "sha256": trial.digest(raw),
                              "mtime_ns": (sources / "0").stat().st_mtime_ns}],
                 "audit_sha256": None, "feed_seq": number}
        bound_path = directory / "s0-bound.json"
        bound_path.write_text(json.dumps(bound) + "\n")
        bound_path.chmod(0o600)
        manifest = {"version": 2, "status": "candidate_unreviewed", "provenance_phase": phase,
                    "case_id": case_id, "channel": "health", "projected_view": projected,
                    "safe_view": trial.safe_view(projected, "health"),
                    "original_feed_seq": number, "event_id": event_id,
                    "capture_key": trial.digest(f"health\0{event_id}".encode()),
                    "source_digest": source_digest, "bound_sha256": trial.digest(bound_path.read_bytes()),
                    "sources": [{"file": "sources/0", "origin": str(sources / "0"),
                                 "mtime_ns": (sources / "0").stat().st_mtime_ns,
                                 "sha256": trial.digest(raw)}]}
        path = directory / "case.json"
        path.write_text(json.dumps(manifest) + "\n")
        path.chmod(0o600)
        return {"case_id": case_id, "source_group": group or hashlib.sha256(raw).hexdigest(),
                "split": "holdout", "label": label, "evidence_sha256": trial.digest(path.read_bytes())}

    def write_review(self, rows):
        self.review.write_text(json.dumps({"version": 1, "reviewer": "independent-reviewer",
                                           "cases": rows}) + "\n")
        self.review.chmod(0o600)

    def test_missing_review_reports_zero_evidence_without_model_call(self):
        self.add_case(7)
        with patch.object(sys, "argv", ["trial", "--evidence-root", str(self.root),
                                      "--output", str(self.output), "--run-local-model"]):
            self.assertEqual(trial.main(), 2)
        report = json.loads(self.output.read_text())
        self.assertEqual(report["status"], "missing_review")
        self.assertEqual((report["readiness"]["heldout_yes"], report["readiness"]["heldout_no"]), (0, 0))
        self.assertEqual(report["independent_review"], "absent")
        self.assertFalse(report["authority_eligible"])

    def test_reviewed_s0_case_still_cannot_grant_authority_below_minimum(self):
        row = self.add_case(1)
        self.write_review([row])
        cases, checksum = trial.reviewed_cases(self.root, self.review)
        self.assertEqual(len(cases), 1)
        self.assertEqual(len(checksum), 64)
        with patch.object(sys, "argv", ["trial", "--evidence-root", str(self.root), "--review",
                                      str(self.review), "--output", str(self.output), "--run-local-model"]):
            self.assertEqual(trial.main(), 2)
        report = json.loads(self.output.read_text())
        self.assertEqual(report["status"], "missing_evidence")
        self.assertEqual(report["readiness"]["heldout_no"], 1)
        self.assertEqual(report["readiness"]["heldout_yes"], 0)
        self.assertFalse(report["authority_eligible"])
        self.assertIsNone(report["scores"])
        self.assertEqual(self.output.stat().st_mode & 0o077, 0)

    def test_rejects_post_observation_and_mutated_private_bytes(self):
        historical = self.add_case(2, phase="post_observation_reprojection")
        self.write_review([historical])
        with self.assertRaisesRegex(ValueError, "case lacks exact S0-bound"):
            trial.reviewed_cases(self.root, self.review)
        bound = self.add_case(3)
        self.write_review([bound])
        source = self.cases / bound["case_id"] / "sources/0"
        source.write_bytes(b"producer changed after review")
        with self.assertRaisesRegex(ValueError, "archived producer bytes changed"):
            trial.reviewed_cases(self.root, self.review)

    def test_duplicate_causal_group_and_bad_review_hash_fail_closed(self):
        one = self.add_case(4)
        two = self.add_case(5, group=one["source_group"])
        self.write_review([one, two])

        with self.assertRaisesRegex(ValueError, "duplicate or invalid reviewed case/group"):
            trial.reviewed_cases(self.root, self.review)
        one["evidence_sha256"] = "0" * 64
        self.write_review([one])
        with self.assertRaisesRegex(ValueError, "reviewed manifest digest mismatch"):
            trial.reviewed_cases(self.root, self.review)

    def test_rejects_tampered_s0_bound_artifact(self):
        row = self.add_case(6)
        self.write_review([row])
        bound = self.cases / row["case_id"] / "s0-bound.json"
        bound.write_text(bound.read_text() + " ")
        with self.assertRaisesRegex(ValueError, "S0 bound stamp or archived sources mismatch"):
            trial.reviewed_cases(self.root, self.review)

    def test_unknown_counts_against_coverage_and_accuracy(self):
        cases = [{"case_id": "a", "split": "holdout", "label": "yes"},
                 {"case_id": "b", "split": "holdout", "label": "yes"},
                 {"case_id": "c", "split": "holdout", "label": "no"},
                 {"case_id": "d", "split": "holdout", "label": "no"}]
        score = trial.score(cases, {"a": "yes", "b": "unknown", "c": "yes", "d": "no"})
        self.assertEqual((score["tp"], score["tn"], score["fp"], score["fn"], score["unknown"]),
                         (1, 1, 1, 0, 1))
        self.assertEqual(score["coverage"], 0.75)
        self.assertEqual(score["accuracy_all_including_unknown_as_incorrect"], 0.5)
        self.assertEqual(score["sensitivity_all"], 0.5)
        self.assertEqual(score["specificity_all"], 0.5)
        self.assertEqual((trial.classify(0.20), trial.classify(0.80), trial.classify(0.5)),
                         ("no", "yes", "unknown"))


if __name__ == "__main__":
    unittest.main()
