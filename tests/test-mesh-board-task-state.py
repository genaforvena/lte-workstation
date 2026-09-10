"""Dispatch derives chain eligibility from canonical text, not stale balances."""
import runpy
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
board = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'))


class TaskQueueTests(unittest.TestCase):
    def records(self, status='open', owner=None):
        data = dict(chain='plan', current=0, status=status, steps=[
            dict(id='plan/work', slug='work', description='produce evidence', owner=owner, status=status),
            dict(id='plan/check', slug='check', description='verify', owner='beta', status='open')])
        return {'plan': dict(schema=1, revision=1, data=data)}

    def project(self, rows, records):
        return board['dispatch_rows'](rows, records)

    def test_blocked_active_done_and_future_steps_never_dispatch(self):
        rows = [dict(slug='plan-work', owner='old', lead='stale'),
                dict(slug='plan-check', owner='beta', lead='future')]
        for status in ('blocked', 'active', 'done', 'complete'):
            with self.subTest(status=status):
                self.assertEqual(self.project(rows, self.records(status, 'alpha')), [])

    def test_open_current_step_appears_without_a_prose_receipt(self):
        rows = self.project([], self.records())
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['slug'], 'plan/work')
        self.assertEqual(rows[0]['owner'], '-')
        self.assertIn('mesh-task take plan work', rows[0]['lead'])
        self.assertIn('task:plan/work', rows[0]['lead'])

    def test_current_owner_wins_stale_accounting_owner(self):
        rows = self.project([dict(slug='plan-work', owner='old', lead='old')], self.records('open', 'alpha'))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['owner'], 'alpha')

    def test_unrelated_task_mention_is_not_a_closure(self):
        row = dict(slug='investigate', owner='alpha', lead='Investigate why plan/work is blocked')
        self.assertEqual(self.project([row], self.records('blocked', 'alpha')), [row])

    def test_cli_uses_task_state_and_fails_on_missing_source(self):
        from mesh_task_log import encode
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            journal = root / 'promises.journal'
            journal.write_text('2026-09-08 * stale task\n    liabilities:promises:old:plan-work  1 PROMISE\n    equity:tasks  -1 PROMISE\n')
            source = root / 'chat.log'
            source.write_text('2026-09-08T00:00:00Z alpha :: ' + encode(self.records('blocked', 'alpha')['plan']['data'], 1) + '\n')
            env = dict(os.environ, MESH_DIR=td, MESH_CHAT_LOG=str(source), MESH_PROMISE_JOURNAL=str(journal))
            command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'), 'open', '--dispatch']
            result = subprocess.run(command, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, '')
            source.unlink()
            result = subprocess.run(command, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, '')

    def test_ambiguous_legacy_alias_fails_loudly(self):
        records = self.records('blocked', 'alpha')
        first = dict(chain='a-b', current=0, status='blocked', steps=[dict(id='a-b/c', slug='c', owner='alpha', status='blocked')])
        second = dict(chain='a', current=0, status='blocked', steps=[dict(id='a/b-c', slug='b-c', owner='alpha', status='blocked')])
        records = {'first': {'data': first}, 'second': {'data': second}}
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            self.project([dict(slug='a-b-c')], records)


if __name__ == '__main__':
    unittest.main()
