#!/usr/bin/env python3
"""A disposable Mind cannot change a task without its exact authority lease."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest


REPO = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get('MESH_MISHE_CORE', '/home/mesh-home/mishe-tauftauf'))
TASK = REPO / 'scripts/mesh-task'
AUTHORITY = REPO / 'scripts/mesh-mishe-authority'
LOG = REPO / 'scripts/mesh_task_log.py'


class MisheTaskAuthority(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.test-mishe-task-', dir=REPO)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mesh = self.root / 'mesh'
        self.mishe = self.root / 'mishe'
        self.board = self.root / 'board.log'
        self.entered = self.root / 'entered'
        self.release = self.root / 'release'
        self.writer = self.root / 'chat'
        self.writer.write_text(
            '#!/bin/sh\nset -eu\n'
            'if [ "$1" = "--task-state" ]; then\n'
            f'  exec python3 "{LOG}" append "$MESH_DIR" fixture "$2"\n'
            'fi\n'
            'case "$1" in\n'
            '  "[taking] "*)\n'
            '    if [ "${TEST_STALL_TAKING:-0}" = 1 ]; then\n'
            '      : > "$TEST_ENTERED"\n'
            '      while [ ! -e "$TEST_RELEASE" ]; do sleep 0.05; done\n'
            '    fi ;;\n'
            'esac\n'
            'printf "%s\\n" "$1" >> "$TEST_BOARD"\n')
        self.writer.chmod(0o700)
        self.env = dict(os.environ, MESH_DIR=str(self.mesh), MESH_TASK_DIR=str(self.mesh / 'chains'),
                        MESH_CHAT_LOG=str(self.mesh / 'chat.log'), MESH_TASK_CHAT_CMD=str(self.writer),
                        MESH_TASK_HANDOFF_CMD='/bin/true', MESH_TASK_ACTOR='synthetic',
                        MESH_MISHE_HOME=str(self.mishe), MESH_MISHE_CORE=str(CORE),
                        TEST_BOARD=str(self.board), TEST_ENTERED=str(self.entered),
                        TEST_RELEASE=str(self.release))
        self.plan = self.root / 'plan.tsv'
        self.plan.write_text('synthetic\treview\tReview a report-only fixture with an inspectable artifact\n')
        self.command('create', 'case', str(self.plan), 'fixture-mishe-task', expected=0)
        self.artifact = self.root / 'report.json'
        self.artifact.write_text('{"result":"held"}\n')

    def command(self, *args, expected=None, **overrides):
        result = subprocess.run([str(TASK), *args], env=dict(self.env, **overrides),
                                capture_output=True, text=True, timeout=15)
        if expected is not None:
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def mind(self, **extra):
        value = dict(MISHE_TAUFTAUF_INVOCATION='synthetic-1-1-fixture',
                     MISHE_TAUFTAUF_SLUG='synthetic', MISHE_TAUFTAUF_GENERATION='1')
        value.update(extra)
        return value

    def state(self):
        result = self.command('replay', '--json', expected=0)
        return json.loads(result.stdout)['case']['data']['steps'][0]

    def switch(self, target, generation):
        result = subprocess.run([str(AUTHORITY), 'switch', 'synthetic', '--to', target,
                                 '--expect-generation', str(generation), '--feed-seq', '1'],
                                env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)

    def feed(self):
        subprocess.run(['python3', '-c',
                        "from mishe_tauftauf.feed import Feed; import sys; Feed(sys.argv[1]).append_runtime('mishe-tauftauf','shadow')",
                        str(self.mishe)], env=dict(self.env, PYTHONPATH=str(CORE / 'src')), check=True)

    def test_legacy_and_partial_markers_refuse_without_board_effect(self):
        before = self.board.read_bytes()
        legacy = self.command('take', 'case', 'review', **self.mind())
        self.assertEqual(legacy.returncode, 2, legacy.stderr)
        self.assertIn('legacy', legacy.stderr)
        partial = self.command('take', 'case', 'review', MISHE_TAUFTAUF_SLUG='synthetic')
        self.assertEqual(partial.returncode, 2, partial.stderr)
        self.assertEqual(self.board.read_bytes(), before)
        self.assertEqual(self.state()['status'], 'open')

    def test_exact_generation_owner_and_artifact_gate(self):
        self.feed(); self.switch('mishe', 0)
        before = self.board.read_bytes()
        for overrides in (self.mind(MISHE_TAUFTAUF_GENERATION='2'),
                          self.mind(MESH_TASK_ACTOR='other'),
                          {'MISHE_TAUFTAUF_INVOCATION': 'synthetic-1-1-fixture',
                           'MISHE_TAUFTAUF_SLUG': 'synthetic'}):
            result = self.command('take', 'case', 'review', **overrides)
            self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.board.read_bytes(), before)
        self.command('take', 'case', 'review', expected=0, **self.mind())
        self.command('done', 'case', 'review', str(self.artifact), 'checked report pane:check',
                     expected=0, **self.mind())
        settled = self.state()
        self.assertEqual(settled['status'], 'done')
        self.assertEqual(settled['artifact'], str(self.artifact))
        delivered = self.board.read_bytes()
        self.command('done', 'case', 'review', str(self.artifact), 'checked report pane:check',
                     expected=0, **self.mind())
        self.assertEqual(self.board.read_bytes(), delivered)
        self.artifact.write_text('{"result":"tampered"}\n')
        tampered = self.command('done', 'case', 'review', str(self.artifact),
                                'checked report pane:check', **self.mind())
        self.assertEqual(tampered.returncode, 2, tampered.stderr)
        self.assertEqual(self.board.read_bytes(), delivered)
        self.assertEqual(self.state()['artifact_sha256'], settled['artifact_sha256'])

    def test_switch_waits_for_claim_and_stale_mind_cannot_settle(self):
        self.feed(); self.switch('mishe', 0)
        claim = subprocess.Popen([str(TASK), 'take', 'case', 'review'],
                                 env=dict(self.env, **self.mind(), TEST_STALL_TAKING='1'),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        change = None
        try:
            for _ in range(150):
                if self.entered.exists():
                    break
                if claim.poll() is not None:
                    break
                time.sleep(0.02)
            self.assertTrue(self.entered.exists(), 'task writer never held shared authority lease')
            change = subprocess.Popen([str(AUTHORITY), 'switch', 'synthetic', '--to', 'legacy',
                                       '--expect-generation', '1', '--feed-seq', '1'],
                                      env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.15)
            self.assertIsNone(change.poll(), 'authority switched during task claim')
            self.release.touch()
            _, claim_error = claim.communicate(timeout=15)
            self.assertEqual(claim.returncode, 0, claim_error)
            _, switch_error = change.communicate(timeout=15)
            self.assertEqual(change.returncode, 0, switch_error)
            self.assertEqual(self.state()['status'], 'active')
            stale = self.command('done', 'case', 'review', str(self.artifact), 'checked report',
                                 **self.mind())
            self.assertEqual(stale.returncode, 2, stale.stderr)
            self.assertEqual(self.state()['status'], 'active')
            self.switch('mishe', 2)
            self.command('done', 'case', 'review', str(self.artifact), 'checked report',
                         expected=0, **self.mind(MISHE_TAUFTAUF_GENERATION='3'))
        finally:
            self.release.touch()
            for process in (claim, change):
                if process is not None and process.poll() is None:
                    process.kill()
                    process.communicate()

    def test_killed_claim_does_not_hold_switch_or_complete_task(self):
        self.feed(); self.switch('mishe', 0)
        claim = subprocess.Popen([str(TASK), 'take', 'case', 'review'],
                                 env=dict(self.env, **self.mind(), TEST_STALL_TAKING='1'),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            for _ in range(150):
                if self.entered.exists() or claim.poll() is not None:
                    break
                time.sleep(0.02)
            self.assertTrue(self.entered.exists(), 'claim did not enter the sink')
            claim.kill()
            self.release.touch()
            claim.communicate(timeout=15)
            self.switch('legacy', 1)
            self.assertEqual(self.state()['status'], 'open')
            stale = self.command('take', 'case', 'review', **self.mind())
            self.assertEqual(stale.returncode, 2, stale.stderr)
            self.assertEqual(self.state()['status'], 'open')
        finally:
            self.release.touch()
            if claim.poll() is None:
                claim.kill()
                claim.communicate()


    def test_doctor_renders_authority_fence_red_then_green(self):
        from datetime import datetime, timezone
        env = dict(self.env, PYTHONPATH=str(CORE / 'src'))
        for directory in ('top-pains', 'projectors', 'minds'):
            (self.mishe / directory).mkdir(parents=True, exist_ok=True)
        for name in ('top-pains/synthetic', 'top-pains/cleaner', 'projectors/synthetic'):
            path = self.mishe / name
            path.write_text('#!/bin/sh\nprintf "STATE: GREEN\\n"\n')
            path.chmod(0o700)
        append = (
            'from mishe_tauftauf.feed import Feed; import sys; '
            "f=Feed(sys.argv[1]); f.append_runtime('observation/synthetic','STATE: GREEN'); "
            "f.append_runtime('observation/cleaner','STATE: GREEN')"
        )
        subprocess.run(['python3', '-c', append, str(self.mishe)], env=env, check=True)
        (self.mishe / '.mesh-mishe-pass').write_text(str(time.time()) + '\n')
        record = self.mishe / 'authority/cleaner.json'
        record.parent.mkdir(parents=True)
        record.write_text(json.dumps({'channel': 'cleaner', 'generation': 1,
                                      'authority': 'mishe', 'active_feed_seq': 0,
                                      'installed_at': datetime.now(timezone.utc).isoformat()}))
        doctor = REPO / 'scripts/mesh-mishe-doctor'
        red = subprocess.run([str(doctor)], env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(red.returncode, 1, red.stdout + red.stderr)
        self.assertIn('task mutation fence: UNKNOWN', red.stdout)
        record.unlink()
        green = subprocess.run([str(doctor)], env=env, capture_output=True, text=True, timeout=20)
        self.assertIn('task mutation fence: PASS legacy Mind refused', green.stdout)
        self.assertNotIn('task mutation fence: UNKNOWN', green.stdout)


    def test_authority_lock_symlink_refuses_without_claim(self):
        self.feed(); self.switch('mishe', 0)
        lock = self.mishe / 'authority/synthetic.lock'
        lock.unlink()
        outside = self.root / 'outside.lock'
        outside.write_text('outside\n')
        lock.symlink_to(outside)
        before = self.board.read_bytes()
        refused = self.command('take', 'case', 'review', **self.mind())
        self.assertEqual(refused.returncode, 2, refused.stderr)
        self.assertIn('UNKNOWN mishe task authority lock', refused.stderr)
        self.assertEqual(self.board.read_bytes(), before)
        self.assertEqual(outside.read_text(), 'outside\n')
        self.assertEqual(self.state()['status'], 'open')


    def test_corrupt_authority_and_tampered_artifact_fail_closed(self):
        self.feed(); self.switch('mishe', 0)
        record = self.mishe / 'authority/synthetic.json'
        original = record.read_bytes()
        record.write_text('{bad')
        attempt = self.command('take', 'case', 'review', **self.mind())
        self.assertEqual(attempt.returncode, 2, attempt.stderr)
        self.assertEqual(self.state()['status'], 'open')
        record.write_bytes(original)
        self.command('take', 'case', 'review', expected=0, **self.mind())
        absent = self.command('done', 'case', 'review', str(self.root / 'absent.json'), 'checked report',
                              **self.mind())
        self.assertEqual(absent.returncode, 2, absent.stderr)
        self.assertEqual(self.state()['status'], 'active')


    def test_crash_after_board_refuses_changed_artifact_on_retry(self):
        chat = REPO / 'scripts/mesh-chat'
        wrapper = self.root / 'crash-after-board'
        wrapper.write_text(
            '#!/bin/sh\n'
            f'"{chat}" "$@" || exit $?\n'
            'case "$1" in\n'
            '  "[done] boardcase/review:"*)\n'
            '    if [ "${TEST_KILL_AFTER_BOARD:-0}" = 1 ]; then kill -KILL "$PPID"; fi ;;\n'
            'esac\n')
        wrapper.chmod(0o700)
        self.env['MESH_TASK_CHAT_CMD'] = str(wrapper)
        self.command('create', 'boardcase', str(self.plan), 'fixture-board-crash', expected=0)
        self.command('take', 'boardcase', 'review', expected=0)
        crashed = self.command('done', 'boardcase', 'review', str(self.artifact),
                               'checked report', TEST_KILL_AFTER_BOARD='1')
        self.assertEqual(crashed.returncode, -9, crashed.stdout + crashed.stderr)
        log = self.mesh / 'chat.log'
        posted = [line for line in log.read_text().splitlines()
                  if ' ::  [done] boardcase/review:' in line]
        self.assertEqual(len(posted), 1)
        self.assertEqual(json.loads(self.command('replay', '--json', expected=0).stdout)
                         ['boardcase']['data']['steps'][0]['status'], 'active')
        self.artifact.write_text('{"result":"changed-after-board"}\n')
        retry = self.command('done', 'boardcase', 'review', str(self.artifact), 'checked report')
        self.assertEqual(retry.returncode, 2, retry.stdout + retry.stderr)
        self.assertIn('UNKNOWN', retry.stderr)
        self.assertEqual([line for line in log.read_text().splitlines()
                          if ' ::  [done] boardcase/review:' in line], posted)
        self.assertEqual(json.loads(self.command('replay', '--json', expected=0).stdout)
                         ['boardcase']['data']['steps'][0]['status'], 'active')
        self.artifact.write_text('{"result":"held"}\n')
        different_result = self.command('done', 'boardcase', 'review', str(self.artifact),
                                        'a different report')
        self.assertEqual(different_result.returncode, 2, different_result.stderr)
        self.assertIn('UNKNOWN completion intent mismatch', different_result.stderr)
        self.command('done', 'boardcase', 'review', str(self.artifact),
                     'checked report', expected=0)
        self.assertEqual([line for line in log.read_text().splitlines()
                          if ' ::  [done] boardcase/review:' in line], posted)
        self.assertEqual(json.loads(self.command('replay', '--json', expected=0).stdout)
                         ['boardcase']['data']['steps'][0]['status'], 'done')


    def test_crash_after_intent_retries_once_before_board(self):
        chat = REPO / 'scripts/mesh-chat'
        wrapper = self.root / 'crash-after-intent'
        wrapper.write_text(
            '#!/bin/sh\n'
            f'"{chat}" "$@" || exit $?\n'
            'if [ "$1" = "--task-state" ] && [ "${TEST_KILL_AFTER_INTENT:-0}" = 1 ]; then\n'
            '  case "$2" in *"/completion_intent_sha256="*) kill -KILL "$PPID" ;; esac\n'
            'fi\n')
        wrapper.chmod(0o700)
        self.env['MESH_TASK_CHAT_CMD'] = str(wrapper)
        self.command('create', 'intentcase', str(self.plan), 'fixture-intent-crash', expected=0)
        self.command('take', 'intentcase', 'review', expected=0)
        crashed = self.command('done', 'intentcase', 'review', str(self.artifact),
                               'checked report', TEST_KILL_AFTER_INTENT='1')
        self.assertEqual(crashed.returncode, -9, crashed.stdout + crashed.stderr)
        log = self.mesh / 'chat.log'
        self.assertNotIn(' ::  [done] intentcase/review:', log.read_text())
        pending = json.loads(self.command('replay', '--json', expected=0).stdout)
        self.assertEqual(pending['intentcase']['data']['steps'][0]['status'], 'active')
        self.command('done', 'intentcase', 'review', str(self.artifact),
                     'checked report', expected=0)
        self.assertEqual(sum(' ::  [done] intentcase/review:' in line
                             for line in log.read_text().splitlines()), 1)
        settled = json.loads(self.command('replay', '--json', expected=0).stdout)
        self.assertEqual(settled['intentcase']['data']['steps'][0]['status'], 'done')


if __name__ == '__main__':
    unittest.main()
