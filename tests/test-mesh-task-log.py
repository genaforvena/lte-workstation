import copy
import importlib.util
from importlib.machinery import SourceFileLoader
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('task_log', Path(__file__).resolve().parents[1] / 'scripts/mesh_task_log.py')
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)
scrub_path = Path(__file__).resolve().parents[1] / 'scripts/mesh-log-scrub'
scrub_spec = importlib.util.spec_from_loader('log_scrub', SourceFileLoader('log_scrub', str(scrub_path)))
scrub = importlib.util.module_from_spec(scrub_spec)
scrub_spec.loader.exec_module(scrub)


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

    def legacy_event(self, data, rev):
        record = {'schema': 1, 'revision': rev, 'data': data}
        return ('2026-09-08T00:00:00Z  alpha@node  ::  [task-state] '
                + json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n')

    def test_new_encoding_is_not_json_and_mixed_history_replays(self):
        encoded = log.encode(self.data, 1)
        self.assertTrue(encoded.startswith('[task-ledger] v1 r=1 | '))
        self.assertIn('/chain=s:plan', encoded)
        self.assertIn('/steps/0/description=s:first', encoded)
        self.assertNotIn('plist64:', encoded)
        self.assertNotIn('{"schema"', encoded)

        started = copy.deepcopy(self.data)
        started['status'] = started['steps'][0]['status'] = 'active'
        self.path.write_text(self.legacy_event(self.data, 1) + self.event(started, 2))
        self.assertEqual(log.replay(self.path)['plan']['data'], started)

    def test_readable_round_trip_escapes_typed_values_and_unicode(self):
        data = copy.deepcopy(self.data)
        data['steps'][0]['description'] = 'Юникод % | pipe\nline\rreturn'
        data['steps'][0]['nullable'] = None
        data['steps'][0]['enabled'] = True
        data['steps'][0]['count'] = 7
        encoded = log.encode(data, 4)
        self.assertIn('%25', encoded)
        self.assertIn('%7C', encoded)
        self.assertIn('%0A', encoded)
        self.assertIn('%0D', encoded)
        self.assertEqual(log.decode(encoded.removeprefix(log.MARKER))['data'], data)

    def test_malformed_readable_payloads_are_refused(self):
        good = log.encode(self.data, 1).removeprefix(log.MARKER)
        for bad in (good.replace('/chain=s:plan', '/chain=s:one | /chain=s:two', 1),
                    good.replace('/chain=s:plan', '/steps/9/status=s:open', 1),
                    good.replace('/chain=s:plan', '/chain=x:%ZZ', 1),
                    good.replace('/chain=s:plan', '/chain=i:3', 1)):
            with self.subTest(bad=bad):
                with self.assertRaises(log.ReplayError):
                    log.decode(bad)

    def test_rebuild_with_future_steps_and_duplicate_reordered_delivery(self):
        started = copy.deepcopy(self.data)
        started['status'] = started['steps'][0]['status'] = 'active'
        first, second = self.event(self.data, 1), self.event(started, 2)
        self.path.write_text(second + first + second)
        self.assertEqual(log.replay(self.path)['plan']['data'], started)

    def test_transition_rejects_done_step_replaced_by_blocked_revision(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        blocked = copy.deepcopy(done)
        blocked['status'] = blocked['steps'][0]['status'] = 'blocked'
        blocked['steps'][0].pop('finished')
        blocked['steps'][0].pop('artifact')
        blocked['steps'][0].pop('artifact_sha256')
        with self.assertRaisesRegex(log.ReplayError, 'terminal task-state regression'):
            log.validate_transition({'data': done}, {'data': blocked})

    def test_replay_quarantines_historical_regression_and_keeps_restored_done(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        blocked = copy.deepcopy(done)
        blocked['status'] = blocked['steps'][0]['status'] = 'blocked'
        blocked['steps'][0].pop('finished')
        blocked['steps'][0].pop('artifact')
        blocked['steps'][0].pop('artifact_sha256')
        self.path.write_text(self.event(done, 1) + self.event(blocked, 2) + self.event(done, 3))
        self.assertEqual(log.replay(self.path)['plan']['data'], done)

    def test_live_history_r15_r16_r17_quarantine_does_not_block_unrelated_append(self):
        open_state = copy.deepcopy(self.data)
        done = copy.deepcopy(open_state)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        blocked = copy.deepcopy(done)
        blocked['status'] = blocked['steps'][0]['status'] = 'blocked'
        blocked['steps'][0].pop('finished')
        blocked['steps'][0].pop('artifact')
        blocked['steps'][0].pop('artifact_sha256')
        history = ''.join(self.event(open_state, revision) for revision in range(1, 15))
        history += self.event(done, 15) + self.event(blocked, 16) + self.event(done, 17)
        self.path.write_text(history)
        self.assertEqual(log.replay(self.path)['plan']['revision'], 17)
        unrelated = copy.deepcopy(open_state)
        unrelated['chain'] = 'unrelated'
        unrelated['steps'][0]['id'] = 'unrelated/first'
        unrelated['steps'][1]['id'] = 'unrelated/check'
        log.append(self.path.parent, 'alpha@node', log.encode(unrelated, 1).removeprefix(log.MARKER))
        self.assertEqual(log.replay(self.path)['unrelated']['data'], unrelated)

    def test_replay_allows_artifact_backed_recovery_to_a_different_successor_step(self):
        rejected = copy.deepcopy(self.data)
        rejected['status'] = rejected['steps'][0]['status'] = 'rejected'
        rejected['steps'][0]['rejected'] = '2026-09-09T18:17:53Z'
        rejected['steps'][0]['rejected_reason'] = 'dependency was not independently verified'
        recovery = copy.deepcopy(rejected)
        recovery['current'] = 1
        recovery['status'] = recovery['steps'][1]['status'] = 'blocked'
        recovery['steps'][1].update(
            recovery_action='hold', recovery_artifact='/tmp/recovery.md',
            recovery_artifact_sha256='abc123', recovered_from=rejected['steps'][0]['id'])
        released = copy.deepcopy(recovery)
        released['status'] = released['steps'][1]['status'] = 'open'
        self.path.write_text(self.event(rejected, 1) + self.event(recovery, 2) + self.event(released, 3))
        self.assertEqual(log.replay(self.path)['plan']['data'], released)

    def test_tinyfleet_rejected_a02v_recovers_and_reaches_done(self):
        data = dict(chain='tinyfleet-applications-20260908', current=0, status='open', steps=[
            dict(id='tinyfleet-applications-20260908/verify-ticket-extraction',
                 slug='verify-ticket-extraction', owner='vpn', status='open'),
            dict(id='tinyfleet-applications-20260908/support-routing',
                 slug='support-routing', owner='haunt', status='open'),
        ])
        rejected = copy.deepcopy(data)
        rejected['status'] = rejected['steps'][0]['status'] = 'rejected'
        rejected['steps'][0].update(
            rejected='2026-09-09T18:17:53Z',
            rejected_reason='A02-V environment prerequisite was not independently verified')
        recovery = copy.deepcopy(rejected)
        recovery['current'] = 1
        recovery['status'] = recovery['steps'][1]['status'] = 'blocked'
        recovery['steps'][1].update(
            recovery_action='hold', recovery_artifact='/tiny-fleet/A02-verification.md',
            recovery_artifact_sha256='a02-recovery-sha256',
            recovered_from=rejected['steps'][0]['id'])
        released = copy.deepcopy(recovery)
        released['status'] = released['steps'][1]['status'] = 'open'
        done = copy.deepcopy(released)
        done['status'] = done['steps'][1]['status'] = 'complete'
        done['steps'][1].update(
            finished='2026-09-09T19:04:07Z', artifact='/tiny-fleet/A06-implementation.md',
            artifact_sha256='a06-implementation-sha256')
        history = ''.join(self.event(data, revision) for revision in range(1, 7))
        history += ''.join(self.event(record, revision) for revision, record in enumerate(
            (rejected, recovery, released, done), 7))
        self.path.write_text(history)
        result = log.replay(self.path)['tinyfleet-applications-20260908']
        self.assertEqual(result['revision'], 10)
        self.assertEqual(result['data']['current'], 1)
        self.assertEqual(result['data']['steps'][1]['id'],
                         'tinyfleet-applications-20260908/support-routing')
        self.assertEqual(result['data']['steps'][1]['status'], 'complete')

    def test_recovery_cannot_skip_a_successor_step(self):
        rejected = copy.deepcopy(self.data)
        rejected['status'] = rejected['steps'][0]['status'] = 'rejected'
        rejected['steps'][0]['rejected_reason'] = 'dependency was not independently verified'
        skipped = copy.deepcopy(rejected)
        skipped['current'] = 2
        skipped['steps'].append(dict(id='plan/finish', slug='finish', owner='gamma', status='blocked'))
        skipped['status'] = skipped['steps'][2]['status'] = 'blocked'
        skipped['steps'][2].update(
            recovery_action='hold', recovery_artifact='/tmp/recovery.md',
            recovery_artifact_sha256='abc123', recovered_from=rejected['steps'][0]['id'])
        with self.assertRaisesRegex(log.ReplayError, 'terminal task-state'):
            log.validate_transition({'data': rejected}, {'data': skipped})

    def test_replay_rejects_recovery_from_done_step(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        recovery = copy.deepcopy(done)
        recovery['current'] = 1
        recovery['status'] = recovery['steps'][1]['status'] = 'blocked'
        recovery['steps'][1].update(
            recovery_action='hold', recovery_artifact='/tmp/recovery.md',
            recovery_artifact_sha256='abc123', recovered_from=done['steps'][0]['id'])
        self.path.write_text(self.event(done, 1) + self.event(recovery, 2))
        self.assertEqual(log.replay(self.path)['plan']['data'], done)

    def test_replay_quarantines_recovery_that_changes_rejected_predecessor(self):
        rejected = copy.deepcopy(self.data)
        rejected['status'] = rejected['steps'][0]['status'] = 'rejected'
        rejected['steps'][0]['rejected'] = '2026-09-09T18:17:53Z'
        rejected['steps'][0]['rejected_reason'] = 'dependency was not independently verified'
        recovery = copy.deepcopy(rejected)
        recovery['current'] = 1
        recovery['status'] = recovery['steps'][1]['status'] = 'blocked'
        recovery['steps'][0]['rejected_reason'] = 'changed receipt'
        recovery['steps'][1].update(
            recovery_action='hold', recovery_artifact='/tmp/recovery.md',
            recovery_artifact_sha256='abc123', recovered_from=rejected['steps'][0]['id'])
        self.path.write_text(self.event(rejected, 1) + self.event(recovery, 2))
        self.assertEqual(log.replay(self.path)['plan']['data'], rejected)

    def test_append_refuses_post_done_block_without_writing_bytes(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        blocked = copy.deepcopy(done)
        blocked['status'] = blocked['steps'][0]['status'] = 'blocked'
        blocked['steps'][0].pop('finished')
        blocked['steps'][0].pop('artifact')
        blocked['steps'][0].pop('artifact_sha256')
        log.append(self.path.parent, 'alpha@node', log.encode(done, 1).removeprefix(log.MARKER))
        before = self.path.read_bytes()
        with self.assertRaisesRegex(log.ReplayError, 'terminal task-state regression'):
            log.append(self.path.parent, 'alpha@node', log.encode(blocked, 2).removeprefix(log.MARKER))
        self.assertEqual(self.path.read_bytes(), before)

    def test_owner_rejection_with_malformed_sha_receipt_survives_scrub_and_appends(self):
        active = copy.deepcopy(self.data)
        active['status'] = active['steps'][0]['status'] = 'active'
        log.append(self.path.parent, 'vpn@node', log.encode(active, 1).removeprefix(log.MARKER))
        rejected = copy.deepcopy(active)
        rejected['status'] = rejected['steps'][0]['status'] = 'rejected'
        digest = 'a' * 63
        rejected['steps'][0].update(
            rejected='2026-09-09T19:41:00Z',
            rejected_reason=f'raw SHA-256 in receipt is malformed: {digest}')
        encoded = log.encode(rejected, 2).removeprefix(log.MARKER)
        self.assertIn(digest, scrub.sanitize(encoded))
        self.assertNotIn(digest, scrub.sanitize(f'ordinary prose {digest}'))
        log.append(self.path.parent, 'vpn@node', encoded)
        result = log.replay(self.path)['plan']
        self.assertEqual(result['data']['status'], 'rejected')
        self.assertEqual(result['data']['steps'][0]['rejected_reason'],
                         f'raw SHA-256 in receipt is malformed: {digest}')

    def test_append_rejects_fresh_regression_but_allows_unrelated_chain(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        blocked = copy.deepcopy(done)
        blocked['status'] = blocked['steps'][0]['status'] = 'blocked'
        blocked['steps'][0].pop('finished')
        blocked['steps'][0].pop('artifact')
        blocked['steps'][0].pop('artifact_sha256')
        log.append(self.path.parent, 'alpha@node', log.encode(done, 1).removeprefix(log.MARKER))
        with self.assertRaisesRegex(log.ReplayError, 'terminal task-state regression'):
            log.append(self.path.parent, 'alpha@node', log.encode(blocked, 2).removeprefix(log.MARKER))
        other = copy.deepcopy(self.data)
        other['chain'] = 'other'
        other['steps'][0]['id'] = 'other/first'
        other['steps'][1]['id'] = 'other/check'
        log.append(self.path.parent, 'alpha@node', log.encode(other, 1).removeprefix(log.MARKER))
        self.assertEqual(log.replay(self.path)['other']['data'], other)

    def test_replay_rejects_terminal_receipt_mutation(self):
        done = copy.deepcopy(self.data)
        done['status'] = done['steps'][0]['status'] = 'complete'
        done['steps'][0].update(finished='2026-09-09T19:06:35Z', artifact='/receipt.md',
                                artifact_sha256='abc123')
        mutated = copy.deepcopy(done)
        mutated['steps'][0]['artifact_sha256'] = 'different'
        self.path.write_text(self.event(done, 1) + self.event(mutated, 2))
        self.assertEqual(log.replay(self.path)['plan']['data'], done)

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

    def test_ignored_task_requires_a_nonempty_reason(self):
        self.data['status'] = self.data['steps'][0]['status'] = 'ignored'
        with self.assertRaises(log.ReplayError):
            log.encode(self.data, 1)
        self.data['steps'][0]['ignored_reason'] = 'superseded by an operator decision'
        encoded = log.encode(self.data, 1).removeprefix(log.MARKER)
        self.assertEqual(log.decode(encoded)['data']['steps'][0]['ignored_reason'],
                         'superseded by an operator decision')

    def test_append_is_durable_replayable_and_duplicate_safe(self):
        payload = log.encode(self.data, 1).removeprefix(log.MARKER)
        log.append(self.path.parent, 'alpha@node', payload)
        before = self.path.read_bytes()
        self.assertIn(b'[task-ledger] v1 r=1 | ', before)
        self.assertNotIn(b'[task-state]', before)
        self.assertNotIn(b'plist64:', before)
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
