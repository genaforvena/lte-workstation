import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('task_log', Path(__file__).resolve().parents[1] / 'scripts/mesh_task_log.py')
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)


class ReplayTests(unittest.TestCase):
    def test_delivery_and_resume_require_current_state_and_exact_owner(self):
        records = {'plan': {'data': self.data}}
        self.assertEqual(log.eligibility(records, 'plan-first', 'dispatch', 'alpha'), 0)
        self.assertEqual(log.eligibility(records, 'plan/first', 'dispatch', 'beta'), 2)
        self.assertEqual(log.eligibility(records, 'plan/check', 'dispatch', 'beta'), 2)
        self.assertEqual(log.eligibility(records, 'untracked', 'dispatch', 'alpha'), 3)
        self.data['steps'][0]['status'] = self.data['status'] = 'active'
        self.assertEqual(log.eligibility(records, 'plan/first', 'dispatch', 'alpha'), 2)
        self.assertEqual(log.eligibility(records, 'plan/first', 'resume', 'alpha'), 0)
        self.data['steps'][0]['status'] = self.data['status'] = 'blocked'
        self.assertEqual(log.eligibility(records, 'plan/first', 'resume', 'alpha'), 2)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'chat.log'
        self.data = dict(chain='plan', current=0, status='open', steps=[
            dict(id='plan/first', slug='first', owner='alpha', status='open', description='first'),
            dict(id='plan/check', slug='check', owner='beta', status='open', description='check')])

    def event(self, data, rev):
        return '2026-09-08T00:00:00Z  alpha@node  ::  ' + log.encode(data, rev) + '\n'

    def test_rebuild_with_future_steps_and_duplicate_reordered_delivery(self):
        started = copy.deepcopy(self.data)
        started['status'] = started['steps'][0]['status'] = 'active'
        first, second = self.event(self.data, 1), self.event(started, 2)
        self.path.write_text(second + first + second)
        self.assertEqual(log.replay(self.path)['plan']['data'], started)

    def test_gap_conflict_and_truncation_refused(self):
        first = self.event(self.data, 1)
        changed = copy.deepcopy(self.data)
        changed['steps'][0]['owner'] = 'other'
        for text in (self.event(self.data, 2), first + self.event(changed, 1), first.rstrip('\n')):
            with self.subTest(text=text):
                self.path.write_text(text)
                with self.assertRaises(log.ReplayError):
                    log.replay(self.path)

    def test_fyi_quoted_event_cannot_change_state(self):
        self.path.write_text('2026-09-08T00:00:00Z  alpha@node  ::  [fyi] quoting ' + log.encode(self.data, 1) + '\n')
        self.assertEqual(log.replay(self.path), {})

    def test_missing_source_is_not_empty(self):
        with self.assertRaises(FileNotFoundError):
            log.replay(self.path)

    def test_non_utf8_prose_is_not_task_state_but_damaged_state_is_refused(self):
        self.path.write_bytes(b'2026-09-08T00:00:00Z alpha :: [fyi] old prose \xd0\n' + self.event(self.data, 1).encode())
        self.assertEqual(log.replay(self.path)['plan']['data'], self.data)
        self.path.write_bytes(b'2026-09-08T00:00:00Z alpha :: [task-state] \xd0\n')
        with self.assertRaises(log.ReplayError):
            log.replay(self.path)

    def test_unassigned_task_can_be_queued_then_assigned_and_started(self):
        self.data['steps'][0].pop('owner')
        queued = self.event(self.data, 1)
        assigned = copy.deepcopy(self.data)
        assigned['steps'][0]['owner'] = 'least-busy'
        assigned['steps'][0]['status'] = 'active'
        self.path.write_text(queued + self.event(assigned, 2))
        self.assertEqual(log.replay(self.path)['plan']['data'], assigned)
        self.data['steps'][0]['status'] = 'active'
        with self.assertRaises(log.ReplayError):
            log.encode(self.data, 3)

    def test_append_is_durable_replayable_and_duplicate_safe(self):
        payload = log.encode(self.data, 1).removeprefix(log.MARKER)
        log.append(self.path.parent, 'alpha@node', payload)
        before = self.path.read_bytes()
        self.assertEqual(log.replay(self.path)['plan']['data'], self.data)
        log.append(self.path.parent, 'alpha@node', payload)
        self.assertEqual(self.path.read_bytes(), before)
        changed = copy.deepcopy(self.data)
        changed['steps'][0]['owner'] = 'other'
        with self.assertRaises(log.ReplayError):
            log.append(self.path.parent, 'alpha@node', log.encode(changed, 1).removeprefix(log.MARKER))
        self.assertEqual(self.path.read_bytes(), before)

    def test_scrub_rejection_does_not_commit_partial_state(self):
        payload = log.encode(self.data, 1).removeprefix(log.MARKER)
        log.append(self.path.parent, 'alpha@node', payload)
        before = self.path.read_bytes()
        self.data['steps'][0]['description'] = 'token=sk-' + 'x' * 48
        with self.assertRaisesRegex(log.ReplayError, 'scrub'):
            log.append(self.path.parent, 'alpha@node', log.encode(self.data, 2).removeprefix(log.MARKER))
        self.assertEqual(self.path.read_bytes(), before)

    def test_git_object_path_is_evidence_not_a_secret(self):
        self.data['steps'][0]['description'] = 'Inspect .git/objects/dc/' + 'a' * 38 + ' before repair'
        log.append(self.path.parent, 'alpha@node', log.encode(self.data, 1).removeprefix(log.MARKER))
        self.assertEqual(log.replay(self.path)['plan']['data'], self.data)
        before = self.path.read_bytes()
        for description in ('bare ' + 'a' * 38, '.git/objects/dc/' + 'a' * 39,
                            '.git/objects/dc/sk-' + 'x' * 48):
            self.data['steps'][0]['description'] = description
            with self.assertRaises(log.ReplayError):
                log.append(self.path.parent, 'alpha@node', log.encode(self.data, 2).removeprefix(log.MARKER))
            self.assertEqual(self.path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
