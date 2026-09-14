#!/usr/bin/env python3
"""Fixture-level contract tests for the on-demand self-review shadow."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "mesh-self-review-shadow"
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_task_log import encode  # noqa: E402


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def task_event(chain: str, slug: str, when: datetime, revision: int = 1,
               status: str = "done", artifact: Path | None = None) -> bytes:
    step = {
        "id": f"{chain}/{slug}", "slug": slug, "owner": "genome", "status": status,
        "description": f"Review evidence for {chain}", "queued_at": iso(when - timedelta(minutes=5)),
    }
    if status == "done":
        step.update({"started": iso(when - timedelta(minutes=2)), "finished": iso(when),
                     "result": "evidence reviewed"})
        if artifact is not None:
            payload = artifact.read_bytes()
            step.update({"artifact": str(artifact), "artifact_sha256": hashlib.sha256(payload).hexdigest()})
    data = {"chain": chain, "created": iso(when - timedelta(minutes=5)), "current": 0,
            "status": "complete" if status == "done" else "active", "steps": [step]}
    payload = encode(data, revision).removeprefix("[task-ledger] ")
    return f"{iso(when)} test@host ::  [task-ledger] {payload}\n".encode()


def board_line(when: datetime, marker: str, body: str) -> bytes:
    return f"{iso(when)} genome@host ::  [{marker}] {body}\n".encode()


class SelfReviewShadowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.chat = self.root / "chat.log"
        self.state = self.root / "state"
        self.reports = self.root / "reports"
        self.now = datetime(2026, 9, 14, 18, 0, tzinfo=timezone.utc)
        self.artifact = self.root / "receipt.md"
        self.artifact.write_text("verified receipt\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_tool(self, now: datetime | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "genome", "--chat-log", str(self.chat),
             "--state-dir", str(self.state), "--report-dir", str(self.reports),
             "--now", iso(now or self.now)], cwd=ROOT, text=True, capture_output=True,
            check=False,
        )

    def report(self) -> dict:
        paths = sorted(self.reports.glob("*.jsonl"))
        self.assertTrue(paths, "a due review must write a separate report artifact")
        rows = [json.loads(line) for line in paths[-1].read_text().splitlines()]
        self.assertEqual(len(rows), 1, "each review emits exactly one recommendation record")
        return rows[0]

    def test_reviews_latest_fifty_sources_and_caps_task_transitions_at_twenty(self) -> None:
        rows = []
        for i in range(25):
            rows.append(task_event(f"chain-{i:02d}", "review", self.now - timedelta(minutes=30-i),
                                   artifact=self.artifact))
        for i in range(30):
            rows.append(board_line(self.now - timedelta(minutes=25-i), "fyi", f"genome: evidence {i}"))
        rows.extend([
            board_line(self.now - timedelta(minutes=1), "handoff", "genome: routine handoff"),
            board_line(self.now, "idle", "genome: routine idle"),
        ])
        self.chat.write_bytes(b"".join(rows))

        result = self.run_tool()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("reviewed:", result.stdout)
        report = self.report()
        self.assertEqual(report["mind"], "genome")
        self.assertEqual(report["bounds"]["source_records"], 46)
        self.assertEqual(report["bounds"]["task_transitions"], 20)
        self.assertEqual(report["recommendation"]["type"], "no-action")
        self.assertTrue(report["recommendation"]["evidence"])
        self.assertEqual(report["source_coverage"]["excluded_routine_lines"], 2)

    def test_artifact_digest_mismatch_is_unknown_and_exact_task_refs_are_deduplicated(self) -> None:
        event = task_event("chain-unknown", "review", self.now - timedelta(minutes=10),
                           artifact=self.artifact)
        self.artifact.write_text("changed after completion\n")
        duplicate = board_line(self.now - timedelta(minutes=5), "done",
                               "genome: chain-unknown/review evidence changed")
        self.chat.write_bytes(event + duplicate * 49)

        result = self.run_tool()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("reviewed:", result.stdout)
        report = self.report()
        self.assertEqual(report["task_dispositions"][0]["evidence"], "unknown")
        self.assertEqual(report["task_dispositions"][0]["reason"], "artifact digest mismatch")
        self.assertIn("chain-unknown/review", report["duplicate_matches"])

    def test_one_hour_minimum_and_six_hour_fallback_bound_reviews(self) -> None:
        self.chat.write_bytes(b"".join(
            board_line(self.now - timedelta(minutes=10, seconds=i), "fyi", f"genome: item {i}")
            for i in range(50)
        ))
        first = self.run_tool()
        self.assertEqual(first.returncode, 0, first.stderr)
        first_report = self.report()
        first_report_mtime = next(self.reports.glob("*.jsonl")).stat().st_mtime_ns

        with self.chat.open("ab") as stream:
            stream.write(board_line(self.now + timedelta(minutes=10), "fyi", "genome: new item"))
        early = self.run_tool(self.now + timedelta(minutes=10))
        self.assertEqual(early.returncode, 0, early.stderr)
        self.assertIn("not due", early.stdout)
        self.assertEqual(next(self.reports.glob("*.jsonl")).stat().st_mtime_ns, first_report_mtime)

        due = self.run_tool(self.now + timedelta(hours=6))
        self.assertEqual(due.returncode, 0, due.stderr)
        self.assertEqual(len(list(self.reports.glob("*.jsonl"))), 2)

    def test_cursor_advances_before_report_write_failure(self) -> None:
        self.chat.write_bytes(b"".join(
            board_line(self.now - timedelta(minutes=10, seconds=i), "fyi", f"genome: item {i}")
            for i in range(50)
        ))
        self.reports.write_text("not a directory")

        result = self.run_tool()

        self.assertNotEqual(result.returncode, 0)
        cursor = json.loads((self.state / "genome.json").read_text())
        self.assertEqual(cursor["last_offset"], self.chat.stat().st_size)
        self.assertEqual(cursor["review_count"], 1)

    def test_exact_task_identity_is_deduplicated_across_reviews(self) -> None:
        task_id = "chain-repeat/review"
        self.chat.write_bytes(task_event("chain-repeat", "review", self.now - timedelta(minutes=10),
                                         artifact=self.artifact) + b"".join(
            board_line(self.now - timedelta(minutes=9, seconds=i), "fyi", f"genome: {task_id} source {i}")
            for i in range(49)
        ))
        first = self.run_tool()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn(task_id, json.loads((self.state / "genome.json").read_text())[
            "seen_recommendation_task_ids"])

        later = self.now + timedelta(minutes=10)
        with self.chat.open("ab") as stream:
            stream.write(board_line(later, "fyi", f"genome: {task_id} one exact repeat"))
            for i in range(49):
                stream.write(board_line(later + timedelta(seconds=i + 1), "fyi", f"genome: new source {i}"))
        second = self.run_tool(self.now + timedelta(hours=1))
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn(task_id, self.report()["duplicate_matches"])


if __name__ == "__main__":
    unittest.main()
