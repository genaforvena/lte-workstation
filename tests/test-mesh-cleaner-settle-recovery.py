#!/usr/bin/env python3
"""Exercise the real settle command against disposable synthetic repository state."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest


SETTLE = Path(__file__).resolve().parents[1] / 'scripts/cleaner/mesh-cleaner-settle'


class SettlementRecovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / 'repo'
        self.mesh = base / 'mesh'
        self.generated = self.root / '.firecrawl'
        self.generated.mkdir(parents=True)
        self.cleaner = self.mesh / 'cleaner'
        self.cleaner.mkdir(parents=True)
        self.old = self.generated / 'old.json'
        self.next = self.generated / 'next.json'
        self.old.write_bytes(b'old generated JSON\n')
        self.next.write_bytes(b'next generated JSON\n')
        age = time.time() - 7200
        for path in (self.old, self.next):
            os.utime(path, (age, age))
        self.manifest = self.cleaner / 'latest.json'
        self.manifest.write_text(json.dumps({'version': 1, 'scan_id': 'test-scan',
            'candidates': [self.candidate(self.old), self.candidate(self.next)]}))
        self.receipt = self.cleaner / 'settle-latest.json'
        self.dest = self.cleaner / 'quarantine/prior/.firecrawl/old.json'

    def candidate(self, path):
        st = path.stat()
        return {'path': '.firecrawl/' + path.name, 'reasons': ['disposable-generated'],
                'device_inode': f'{st.st_dev}:{st.st_ino}',
                'mtime_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime)),
                'active_refs': [], 'owner_refs': [], 'task_refs': []}

    def planned(self):
        row = self.candidate(self.old)
        receipt_row = {'path': row['path'], 'status': 'planned',
            'source': str(self.old), 'destination': str(self.dest),
            'device_inode': row['device_inode'], 'mtime_utc': row['mtime_utc'],
            'bytes': self.old.stat().st_size,
            'sha256': hashlib.sha256(self.old.read_bytes()).hexdigest()}
        receipt = {'version': 1, 'scan_id': 'test-scan', 'apply': True,
                   'mutations': 0, 'quarantine': str(self.dest.parent.parent),
                   'outcomes': [receipt_row]}
        # A checkpoint written before os.rename, matching the old gateway's crash window.
        self.receipt.write_text(json.dumps(receipt))
        return receipt_row

    def invoke(self, apply=False, extra_env=None):
        env = dict(os.environ, MESH_REPO=str(self.root), MESH_DIR=str(self.mesh),
                   MESH_CLEANER_APPLY='1' if apply else '0')
        env.update(extra_env or {})
        return subprocess.run([str(SETTLE), '--once'], env=env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_default_remains_dry_run(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('READY path=.firecrawl/old.json', result.stdout)
        self.assertTrue(self.old.exists())
        self.assertTrue(self.next.exists())
        self.assertFalse(json.loads(self.receipt.read_text())['apply'])

    def test_normal_apply_keeps_immutable_plans(self):
        result = self.invoke(apply=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(self.receipt.read_text())
        self.assertEqual(receipt['mutations'], 2)
        snapshots = sorted((self.cleaner / 'settle-receipts').glob(receipt['run_id'] + '-*.planned.json'))
        self.assertEqual(len(snapshots), 2)
        for snapshot in snapshots:
            planned = [row for row in json.loads(snapshot.read_text())['outcomes']
                       if row['status'] == 'planned']
            self.assertEqual(len(planned), 1)
            delivered = next(row for row in receipt['outcomes'] if row['path'] == planned[0]['path'])
            self.assertEqual(planned[0]['sha256'], delivered['sha256'])
            self.assertEqual(planned[0]['device_inode'], delivered['device_inode'])
            self.assertEqual(planned[0]['destination'], delivered['destination'])

    def test_crash_after_latest_checkpoint_before_audit(self):
        # Interpose only the embedded Python process; the shell's UUID helper
        # also starts Python, but its argv[0] is -c rather than -.
        hook = Path(self.temp.name) / 'sitecustomize.py'
        hook.write_text('''import os, sys
if sys.argv[0] == '-':
    original_fsync = os.fsync
    fsync_count = 0
    def fsync(fd):
        global fsync_count
        original_fsync(fd)
        fsync_count += 1
        if fsync_count == 2:  # latest.json directory is durable; audit not begun.
            os._exit(77)
    os.fsync = fsync
''')
        interrupted = self.invoke(apply=True, extra_env={'PYTHONPATH': str(hook.parent)})
        self.assertEqual(interrupted.returncode, 77, interrupted.stdout + interrupted.stderr)
        planned = json.loads(self.receipt.read_text())
        self.assertEqual(planned['outcomes'][0]['status'], 'planned')
        self.assertFalse((self.cleaner / 'settle-receipts' / (planned['run_id'] + '.json')).exists())
        self.assertTrue(self.old.exists())
        resumed = self.invoke(apply=True)
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertIn('mode=resumed-source-only', resumed.stdout)
        self.assertFalse(self.old.exists())
        self.assertTrue(self.next.exists())
        self.assertEqual(json.loads(self.receipt.read_text())['outcomes'][0]['status'], 'quarantined')


    def test_restart_recovers_moved_file_without_second_mutation(self):
        original = self.planned()
        self.dest.parent.mkdir(parents=True)
        os.rename(self.old, self.dest)  # Interrupted immediately after the gateway's move.
        inode = self.dest.stat().st_ino
        result = self.invoke(apply=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('RECOVERED path=.firecrawl/old.json mode=reconciled-destination-only', result.stdout)
        recovered = json.loads(self.receipt.read_text())
        self.assertEqual(recovered['outcomes'][0]['status'], 'quarantined')
        self.assertEqual(recovered['outcomes'][0]['destination'], original['destination'])
        self.assertEqual(recovered['outcomes'][0]['sha256'], original['sha256'])
        audit = self.cleaner / 'settle-receipts' / (recovered['run_id'] + '.json')
        self.assertEqual(json.loads(audit.read_text()), recovered)
        planned_snapshot = self.cleaner / 'settle-receipts' / (recovered['run_id'] + '-prior-pending.json')
        self.assertEqual(json.loads(planned_snapshot.read_text())['outcomes'][0]['status'], 'planned')
        self.assertTrue(self.next.exists())
        repeated = self.invoke(apply=True)
        self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
        self.assertIn('already-settled; mutations=0', repeated.stdout)
        self.assertEqual(self.receipt.read_text(), json.dumps(recovered, indent=2, sort_keys=True) + '\n')
        self.assertEqual(self.dest.stat().st_ino, inode)
        self.assertTrue(self.next.exists())

    def test_restart_resumes_unmoved_source_once(self):
        self.planned()
        inode = self.old.stat().st_ino
        result = self.invoke(apply=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('mode=resumed-source-only', result.stdout)
        self.assertFalse(self.old.exists())
        self.assertEqual(self.dest.stat().st_ino, inode)
        self.assertTrue(self.next.exists())
        self.assertEqual(json.loads(self.receipt.read_text())['mutations'], 1)
        self.assertIn('already-settled; mutations=0', self.invoke(apply=True).stdout)
        self.assertEqual(self.dest.stat().st_ino, inode)

    def test_recovery_does_not_need_the_old_scan_manifest(self):
        self.planned()
        self.dest.parent.mkdir(parents=True)
        os.rename(self.old, self.dest)
        self.manifest.unlink()
        result = self.invoke(apply=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('mode=reconciled-destination-only', result.stdout)
        self.assertTrue(self.next.exists())
        self.assertEqual(json.loads(self.receipt.read_text())['outcomes'][0]['status'], 'quarantined')


    def assert_unresolved(self, *, apply=True):
        before = self.receipt.read_bytes()
        result = self.invoke(apply=apply)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('UNKNOWN', result.stdout)
        self.assertEqual(self.receipt.read_bytes(), before)
        self.assertTrue(self.next.exists())
        self.assertFalse((self.cleaner / 'quarantine/prior/.firecrawl/next.json').exists())

    def test_tampered_destination_blocks_new_move(self):
        self.planned()
        self.dest.parent.mkdir(parents=True)
        os.rename(self.old, self.dest)
        self.dest.write_bytes(b'tampered')
        self.assert_unresolved()

    def test_tampered_source_blocks_retry(self):
        self.planned()
        self.old.write_bytes(b'tampered')
        self.assert_unresolved()

    def test_source_and_destination_present_is_ambiguous(self):
        self.planned()
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(self.old.read_bytes())
        self.assert_unresolved()

    def test_both_endpoints_missing_is_ambiguous(self):
        self.planned()
        self.old.unlink()
        self.assert_unresolved()

    def test_forged_destination_cannot_retarget_recovery(self):
        row = self.planned()
        row['destination'] = str(self.next)
        prior = json.loads(self.receipt.read_text())
        prior['outcomes'] = [row]
        self.receipt.write_text(json.dumps(prior))
        self.assert_unresolved()

    def test_dry_run_cannot_erase_pending_receipt(self):
        self.planned()
        self.assert_unresolved(apply=False)


if __name__ == '__main__':
    unittest.main()
