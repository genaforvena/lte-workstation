#!/usr/bin/env python3
"""Behavioral tests for the witness chat-range review reflex."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mesh-chat-range-review"
LOADER = importlib.machinery.SourceFileLoader("mesh_chat_range_review", str(SCRIPT))
SPEC = importlib.util.spec_from_loader("mesh_chat_range_review", LOADER)
assert SPEC and SPEC.loader
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class ChatRangeReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.chat = self.root / "chat.log"
        self.state = self.root / "state.json"
        self.tasks = self.root / "tasks.json"
        self.calls = self.root / "calls.jsonl"
        self.cli = self.root / "mesh-task"
        self.cli.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "tasks=pathlib.Path(os.environ['FAKE_TASKS'])\n"
            "chat=pathlib.Path(os.environ['MESH_CHAT_REVIEW_CHAT_LOG'])\n"
            "calls=pathlib.Path(os.environ['FAKE_CALLS'])\n"
            "data=json.loads(tasks.read_text()) if tasks.exists() else {}\n"
            "calls.open('a').write(json.dumps(sys.argv[1:])+'\\n')\n"
            "if sys.argv[1]=='replay': print(json.dumps(data)); raise SystemExit(0)\n"
            "if sys.argv[1]=='create':\n"
            " chain=sys.argv[2]; plan=pathlib.Path(sys.argv[3]).read_text()\n"
            " data[chain]={'data':{'chain':chain,'status':'open','current':0,'dispatch':'pending','steps':[{'owner':'witness','status':'open','description':plan}]}}\n"
            " tasks.write_text(json.dumps(data))\n"
            " with chat.open('a') as f: f.write('2026-09-12T00:00:00Z test :: [task-state] '+chain+'\\n')\n"
            " raise SystemExit(0)\n"
            "if sys.argv[1]=='dispatch':\n"
            " marker=os.environ.get('FAKE_FAIL_MARKER')\n"
            " if marker and not pathlib.Path(marker).exists(): pathlib.Path(marker).write_text('failed'); raise SystemExit(1)\n"
            " chain=sys.argv[2]; data[chain]['data']['dispatch']='sent'; tasks.write_text(json.dumps(data))\n"
            " with chat.open('a') as f: f.write('2026-09-12T00:00:01Z test :: [task] '+chain+'\\n')\n"
            " raise SystemExit(0)\n"
            "raise SystemExit(2)\n",
            encoding="utf-8",
        )
        self.cli.chmod(0o755)
        self.env = {
            "MESH_CHAT_REVIEW_CHAT_LOG": str(self.chat),
            "MESH_CHAT_REVIEW_STATE": str(self.state),
            "MESH_CHAT_REVIEW_TASK_CMD": str(self.cli),
            "FAKE_TASKS": str(self.tasks),
            "FAKE_CALLS": str(self.calls),
            "MESH_DIR": str(self.root),
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def add_messages(self, count: int, base: int = 0) -> None:
        with self.chat.open("a", encoding="utf-8") as handle:
            for index in range(count):
                handle.write(f"2026-09-12T00:00:{index % 60:02d}Z mind :: message-{base + index}\n")

    def run_reflex(self) -> None:
        with patch.dict(os.environ, self.env, clear=False), patch.multiple(
            review,
            MESH=self.root,
            CHAT=self.chat,
            STATE=self.state,
            TASK_CMD=str(self.cli),
        ):
            review.run()

    def read_tasks(self) -> dict:
        return json.loads(self.tasks.read_text(encoding="utf-8")) if self.tasks.exists() else {}

    def test_distinct_tiers_use_nonoverlapping_ranges_and_ignore_their_own_posts(self) -> None:
        self.add_messages(5)
        self.run_reflex()  # first run anchors at the current tail; no historical sweep
        self.add_messages(100, base=5)

        self.run_reflex()
        self.run_reflex()

        records = self.read_tasks()
        near = sorted(((key, item) for key, item in records.items() if "near" in key),
                      key=lambda item: int(item[0].rsplit("-", 1)[1]))
        self.assertEqual(len(near), 2)
        descriptions = [item["data"]["steps"][0]["description"] for _, item in near]
        self.assertIn("chat.log physical lines 6-55; exactly 50 source messages", descriptions[0])
        self.assertIn("chat.log physical lines 56-105; exactly 50 source messages", descriptions[1])
        self.assertTrue(all(item["data"]["dispatch"] == "sent" for _, item in near))
        self.assertEqual(sum("medium" in key for key in records), 0)
        self.assertEqual(sum("deep" in key for key in records), 0)

    def test_each_tier_has_its_declared_message_range_and_structured_rows_do_not_count(self) -> None:
        self.assertEqual(dict(review.TIERS), {"near": 50, "medium": 250, "deep": 1000})
        lines = [f"2026-09-12T00:00:00Z mind :: message-{i}" for i in range(1000)]
        lines.insert(100, "2026-09-12T00:00:00Z mesh-task :: [task-state] encoded-ledger-row")
        for _tier, size in review.TIERS:
            batch = review.next_batch(lines, 0, size)
            self.assertEqual(batch["count"], size)
            self.assertEqual(batch["start_line"], 1)
            self.assertEqual(batch["end_line"], size + (1 if size > 100 else 0))

    def test_dispatch_failure_retries_the_same_range_without_duplicate_chain(self) -> None:
        self.add_messages(50)
        self.run_reflex()
        # Initialized at EOF: the existing lines are intentionally baseline only.
        self.add_messages(50, base=50)
        marker = self.root / "fail-dispatch-once"
        self.env["FAKE_FAIL_MARKER"] = str(marker)
        with self.assertRaises(RuntimeError):
            self.run_reflex()
        pending_state = json.loads(self.state.read_text(encoding="utf-8"))
        pending = pending_state["tiers"]["near"]["pending"]
        self.assertEqual((pending["start_line"], pending["end_line"]), (51, 100))

        self.run_reflex()
        records = self.read_tasks()
        self.assertEqual(len(records), 1)
        state = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertIsNone(state["tiers"]["near"]["pending"])
        self.assertEqual(state["tiers"]["near"]["cursor"], 100)
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(sum(call[0] == "create" for call in calls), 1)
        self.assertEqual(sum(call[0] == "dispatch" for call in calls), 2)


if __name__ == "__main__":
    unittest.main()
