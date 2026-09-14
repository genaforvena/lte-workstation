#!/usr/bin/env python3
"""Black-box fixture tests for paired shared-task routing shadow scoring."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "mesh-task-routing-shadow"
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_task_log import encode  # noqa: E402


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def event(chain: str, step: dict, when: datetime, revision: int = 1) -> bytes:
    row = {"slug": step["id"].split("/", 1)[1], **step}
    data = {"chain": chain, "created": iso(when), "current": 0,
            "status": "open" if row.get("status") == "open" else "active", "steps": [row]}
    payload = encode(data, revision).removeprefix("[task-ledger] ")
    return f"{iso(when)} test@host ::  [task-ledger] {payload}\n".encode()


class RoutingShadowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.chat = self.root / "chat.log"
        self.state = self.root / "state"
        self.reports = self.root / "reports"
        self.charters = self.root / "charters"
        self.charters.mkdir()
        self.registry = self.root / "capabilities.json"
        self.now = datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc)
        for mind in ("alpha", "beta"):
            (self.charters / f"{mind}.md").write_text(f"{mind} can do tooling.\n")
            os.utime(self.charters / f"{mind}.md", (self.now.timestamp() - 3600,) * 2)
        self.registry.write_text(json.dumps({
            "schema": 1,
            "capabilities": {
                "tooling": [
                    {"mind": "alpha", "charter": "alpha.md", "evidence": "can do tooling"},
                    {"mind": "beta", "charter": "beta.md", "evidence": "can do tooling"},
                ]
            },
        }))
        self.chat.write_bytes(b"")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_tool(self, now: datetime) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--chat-log", str(self.chat),
             "--state-dir", str(self.state), "--report-dir", str(self.reports),
             "--charter-dir", str(self.charters), "--capability-registry", str(self.registry),
             "--now", iso(now)], cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def rows(self) -> list[dict]:
        path = self.reports / "routing-shadow.jsonl"
        self.assertTrue(path.exists(), "shadow records must use a separate durable report")
        return [json.loads(line) for line in path.read_text().splitlines()]

    def test_scores_shared_unowned_candidate_from_queue_time_load_and_pairs_actual(self) -> None:
        baseline = self.run_tool(self.now)
        self.assertEqual(baseline.returncode, 0, baseline.stderr)

        queued = self.now + timedelta(minutes=1)
        load_a = {"id": "load-a/one", "owner": "alpha", "status": "open",
                  "queued_at": iso(queued - timedelta(minutes=20)), "description": "queued work"}
        load_b = {"id": "load-b/one", "owner": "alpha", "status": "open",
                  "queued_at": iso(queued - timedelta(minutes=10)), "description": "queued work"}
        candidate = {"id": "shared-1/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "Inspect shared tooling task",
                     "tags": "shared,tooling"}
        self.chat.write_bytes(event("load-a", load_a, queued - timedelta(seconds=20)) +
                              event("load-b", load_b, queued - timedelta(seconds=10)) +
                              event("shared-1", candidate, queued))
        original = hashlib.sha256(self.chat.read_bytes()).hexdigest()

        scored = self.run_tool(queued + timedelta(seconds=1))
        self.assertEqual(scored.returncode, 0, scored.stderr)
        self.assertEqual(hashlib.sha256(self.chat.read_bytes()).hexdigest(), original)
        report = self.rows()
        decision = next(row for row in report if row.get("task_id") == "shared-1/inspect")
        self.assertEqual(decision["required_capabilities"], ["tooling"])
        self.assertEqual(decision["eligible_set"], ["alpha", "beta"])
        self.assertEqual(decision["queue_time_load"]["alpha"]["queued_runnable"], 2)
        self.assertEqual(decision["recommendation"], "beta")
        self.assertIsNone(decision["actual_owner"])
        self.assertEqual(decision["assignment_disposition"], "unassigned")
        self.assertEqual(decision["capability_evidence"]["tooling"]["beta"]["status"], "verified")

        started = queued + timedelta(minutes=3)
        assigned = {**candidate, "owner": "alpha", "status": "active", "started": iso(started)}
        self.chat.write_bytes(self.chat.read_bytes() + event("shared-1", assigned, started, revision=2))
        paired_log_digest = hashlib.sha256(self.chat.read_bytes()).hexdigest()
        paired = self.run_tool(started + timedelta(seconds=1))
        self.assertEqual(paired.returncode, 0, paired.stderr)
        self.assertEqual(hashlib.sha256(self.chat.read_bytes()).hexdigest(), paired_log_digest)
        decision = next(row for row in reversed(self.rows())
                        if row.get("record_type") == "candidate" and row.get("task_id") == "shared-1/inspect")
        self.assertEqual(decision["actual_owner"], "alpha")
        self.assertTrue(decision["disagreement"])
        self.assertEqual(decision["assignment_disposition"], "override")
        self.assertEqual(decision["wait_seconds"], 180)

        artifact = self.root / "result.md"
        artifact.write_text("verified result\n")
        done = {**assigned, "status": "done", "finished": iso(started + timedelta(minutes=2)),
                "result": "completed with evidence", "artifact": str(artifact),
                "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}
        self.chat.write_bytes(self.chat.read_bytes() + event("shared-1", done, started + timedelta(minutes=2), revision=3))
        completed_log_digest = hashlib.sha256(self.chat.read_bytes()).hexdigest()
        completed = self.run_tool(started + timedelta(minutes=2, seconds=1))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(hashlib.sha256(self.chat.read_bytes()).hexdigest(), completed_log_digest)
        latest = next(row for row in reversed(self.rows())
                      if row.get("record_type") == "candidate" and row.get("task_id") == "shared-1/inspect")
        self.assertTrue(latest["outcome"]["evidence_backed"])

    def test_active_claim_excludes_only_that_mind_from_the_eligible_set(self) -> None:
        (self.charters / "gamma.md").write_text("gamma can do tooling.\n")
        os.utime(self.charters / "gamma.md", (self.now.timestamp() - 3600,) * 2)
        registry = json.loads(self.registry.read_text())
        registry["capabilities"]["tooling"].append(
            {"mind": "gamma", "charter": "gamma.md", "evidence": "can do tooling"})
        self.registry.write_text(json.dumps(registry))
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        active = {"id": "active/one", "owner": "alpha", "status": "active",
                  "queued_at": iso(queued - timedelta(minutes=2)), "started": iso(queued - timedelta(minutes=1)),
                  "description": "active work"}
        candidate = {"id": "shared-2/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "shared tooling", "tags": "shared,tooling"}
        self.chat.write_bytes(event("active", active, queued - timedelta(seconds=30)) +
                              event("shared-2", candidate, queued))

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 0, result.stderr)
        decision = next(row for row in self.rows()
                        if row.get("record_type") == "candidate" and row.get("task_id") == "shared-2/inspect")
        self.assertEqual(decision["eligible_set"], ["beta", "gamma"])
        self.assertEqual(decision["active_claim_excluded_minds"], ["alpha"])
        self.assertEqual(decision["queue_time_load"]["alpha"]["active"], 1)

    def test_exact_owner_incident_dependency_and_unknown_capability_are_excluded(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        candidates = [
            {"id": "fixed/one", "owner": None, "status": "open", "queued_at": iso(queued),
             "description": "owner: alpha shared tooling", "tags": "shared,tooling"},
            {"id": "incident/one", "owner": None, "status": "open", "queued_at": iso(queued),
             "description": "shared tooling", "tags": "shared,tooling,incident"},
            {"id": "dependency/one", "owner": None, "status": "open", "queued_at": iso(queued),
             "description": "shared tooling", "tags": "shared,tooling,dependency"},
            {"id": "unknown/one", "owner": None, "status": "open", "queued_at": iso(queued),
             "description": "shared specialty work", "tags": "shared,rare-skill"},
        ]
        self.chat.write_bytes(b"".join(event(step["id"].split("/", 1)[0], step, queued)
                                         for step in candidates))

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows()
        self.assertFalse(any(row.get("recommendation") for row in rows if row.get("record_type") == "candidate"))
        summary = [row for row in rows if row.get("record_type") == "summary"][-1]
        self.assertEqual(summary["excluded"]["exact-owner"], 1)
        self.assertEqual(summary["excluded"]["incident"], 1)
        self.assertEqual(summary["excluded"]["dependency-resolver"], 1)
        self.assertEqual(summary["excluded"]["unavailable-capability"], 1)

    def test_charter_claim_modified_after_queue_time_is_unknown(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        for mind in ("alpha", "beta"):
            path = self.charters / f"{mind}.md"
            os.utime(path, (queued.timestamp() + 60,) * 2)
        candidate = {"id": "shared-stale/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "shared tooling", "tags": "shared,tooling"}
        self.chat.write_bytes(event("shared-stale", candidate, queued))

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = [row for row in self.rows() if row.get("record_type") == "summary"][-1]
        excluded = next(row for row in summary["excluded_candidates"]
                        if row["task_id"] == "shared-stale/inspect")
        self.assertEqual(excluded["reason"], "unavailable-capability")
        self.assertEqual(excluded["capability_evidence"]["tooling"]["alpha"]["reason"],
                         "charter evidence is newer than queue time")

    def test_noncanonical_revision_gap_fails_closed(self) -> None:
        queued = self.now + timedelta(minutes=1)
        candidate = {"id": "gap/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "shared tooling", "tags": "shared,tooling"}
        self.chat.write_bytes(event("gap", candidate, queued, revision=2))

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing task-state revision", result.stderr)

    def test_charter_protected_mind_is_recorded_but_not_recommended(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        (self.charters / "gamma.md").write_text("gamma can do tooling. This charter reserves gamma.\n")
        os.utime(self.charters / "gamma.md", (self.now.timestamp() - 3600,) * 2)
        registry = json.loads(self.registry.read_text())
        registry["capabilities"]["tooling"].append(
            {"mind": "gamma", "charter": "gamma.md", "evidence": "can do tooling",
             "protected_by_charter": "This charter reserves gamma"})
        self.registry.write_text(json.dumps(registry))
        # Freeze a fresh trial with the expanded registry.
        self.state = self.root / "state-protected"
        self.reports = self.root / "reports-protected"
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        candidate = {"id": "shared-protected/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "shared tooling", "tags": "shared,tooling"}
        self.chat.write_bytes(event("shared-protected", candidate, queued))

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 0, result.stderr)
        decision = next(row for row in self.rows()
                        if row.get("record_type") == "candidate" and row.get("task_id") == "shared-protected/inspect")
        self.assertEqual(decision["eligible_set"], ["alpha", "beta"])
        self.assertEqual(decision["capability_evidence"]["tooling"]["gamma"]["status"], "protected")

    def test_ordered_successor_is_not_treated_as_a_runnable_shared_candidate(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        chain = "ordered"
        steps = [
            {"id": f"{chain}/first", "slug": "first", "owner": "alpha", "status": "blocked",
             "description": "waiting on dependency", "blocker_type": "dependency"},
            {"id": f"{chain}/second", "slug": "second", "owner": None, "status": "open",
             "description": "shared tooling successor", "tags": "shared,tooling", "queued_at": iso(queued)},
        ]
        data = {"chain": chain, "created": iso(queued), "current": 0,
                "status": "blocked", "steps": steps}
        payload = encode(data, 1).removeprefix("[task-ledger] ")
        self.chat.write_bytes(f"{iso(queued)} test@host ::  [task-ledger] {payload}\n".encode())

        result = self.run_tool(queued + timedelta(seconds=1))

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = [row for row in self.rows() if row.get("record_type") == "summary"][-1]
        self.assertEqual(summary["excluded"]["dependency-resolver"], 1)
        self.assertFalse(any(row.get("task_id") == f"{chain}/second"
                             for row in self.rows() if row.get("record_type") == "candidate"))

    def test_quarantined_terminal_mutation_cannot_replace_canonical_outcome(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued = self.now + timedelta(minutes=1)
        started = queued + timedelta(minutes=1)
        artifact = self.root / "verified.md"
        artifact.write_text("canonical result\n")
        candidate = {"id": "terminal/inspect", "owner": None, "status": "open",
                     "queued_at": iso(queued), "description": "shared tooling", "tags": "shared,tooling"}
        assigned = {**candidate, "owner": "alpha", "status": "active", "started": iso(started)}
        done = {**assigned, "status": "done", "finished": iso(started + timedelta(minutes=1)),
                "result": "verified", "artifact": str(artifact),
                "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}
        mutation = {**done, "artifact": str(self.root / "missing.md"), "artifact_sha256": "f" * 64}
        self.chat.write_bytes(event("terminal", candidate, queued, revision=1) +
                              event("terminal", assigned, started, revision=2) +
                              event("terminal", done, started + timedelta(minutes=1), revision=3) +
                              event("terminal", mutation, started + timedelta(minutes=2), revision=4))

        result = self.run_tool(started + timedelta(minutes=3))

        self.assertEqual(result.returncode, 0, result.stderr)
        decision = next(row for row in self.rows()
                        if row.get("record_type") == "candidate" and row.get("task_id") == "terminal/inspect")
        self.assertTrue(decision["outcome"]["evidence_backed"])
        self.assertEqual(decision["outcome"]["artifact"], str(artifact))

    def test_owner_concentration_denominator_ignores_unassigned_candidates(self) -> None:
        self.assertEqual(self.run_tool(self.now).returncode, 0)
        queued_a = self.now + timedelta(minutes=1)
        queued_b = self.now + timedelta(minutes=2)
        task_a = {"id": "paired-a/inspect", "owner": None, "status": "open",
                  "queued_at": iso(queued_a), "description": "shared tooling", "tags": "shared,tooling"}
        task_b = {"id": "paired-b/inspect", "owner": None, "status": "open",
                  "queued_at": iso(queued_b), "description": "shared tooling", "tags": "shared,tooling"}
        assigned_a = {**task_a, "owner": "alpha", "status": "active",
                      "started": iso(queued_b + timedelta(minutes=1))}
        self.chat.write_bytes(event("paired-a", task_a, queued_a) + event("paired-b", task_b, queued_b) +
                              event("paired-a", assigned_a, queued_b + timedelta(minutes=1), revision=2))

        result = self.run_tool(queued_b + timedelta(minutes=2))

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = [row for row in self.rows() if row.get("record_type") == "summary"][-1]
        self.assertEqual(summary["shadow"]["eligible_tasks"], 2)
        self.assertEqual(summary["shadow"]["assignment_dispositions"]["unassigned"], 1)
        self.assertEqual(summary["shadow"]["max_actual_owner_share"], 1.0)


if __name__ == "__main__":
    unittest.main()
