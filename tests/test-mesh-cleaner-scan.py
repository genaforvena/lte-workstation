#!/usr/bin/env python3
"""Cleaner manifest paths must identify the files Git actually reported."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCAN = Path(__file__).resolve().parents[1] / 'scripts/cleaner/mesh-cleaner-scan'


class CleanerScanPaths(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.state = Path(self.temp.name) / 'state'
        subprocess.run(['git', '-C', str(self.root), 'init', '-q'], check=True)
        subprocess.run(['git', '-C', str(self.root), 'config', 'user.email', 'scan@example.test'], check=True)
        subprocess.run(['git', '-C', str(self.root), 'config', 'user.name', 'scan'], check=True)
        (self.root / 'seed').write_text('seed\n')
        subprocess.run(['git', '-C', str(self.root), 'add', 'seed'], check=True)
        subprocess.run(['git', '-C', str(self.root), 'commit', '-qm', 'seed'], check=True)
        self.env = {**os.environ, 'MESH_REPO': str(self.root), 'MESH_DIR': str(self.state)}

    def run_scan(self):
        result = subprocess.run([str(SCAN), '--once'], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((self.state / 'cleaner/latest.json').read_text())

    def test_exact_untracked_paths_and_stat_identity(self):
        names = ['plain.txt', 'notes/name with spaces.txt', 'notes/quote"name.txt',
                 'notes/back\\slash.txt', 'notes/line\nbreak.txt',
                 'notes/кириллица.txt', 'notes/name -> destination.txt',
                 '.firecrawl/generated with spaces.json', 'scripts/protected with spaces.txt']
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('observed fixture\n')
        rows = {row['path']: row for row in self.run_scan()['candidates']}
        self.assertEqual(set(rows), set(names))
        for name in names:
            stat = (self.root / name).stat()
            self.assertEqual(rows[name]['bytes'], stat.st_size)
            self.assertEqual(rows[name]['device_inode'], f'{stat.st_dev}:{stat.st_ino}')
        self.assertEqual(rows['.firecrawl/generated with spaces.json']['reasons'], ['disposable-generated'])
        self.assertEqual(rows['scripts/protected with spaces.txt']['reasons'], ['protected-root'])
        self.assertEqual(rows['notes/name -> destination.txt']['reasons'], ['review-required'])

    def test_staged_rename_uses_existing_destination_not_old_name(self):
        old = 'notes/old -> quoted".txt'
        new = 'notes/new name\nкириллица.txt'
        (self.root / 'notes').mkdir()
        (self.root / old).write_text('rename content\n')
        subprocess.run(['git', '-C', str(self.root), 'add', old], check=True)
        subprocess.run(['git', '-C', str(self.root), 'commit', '-qm', 'old name'], check=True)
        subprocess.run(['git', '-C', str(self.root), 'mv', old, new], check=True)
        rows = {row['path']: row for row in self.run_scan()['candidates']}
        self.assertEqual(set(rows), {new})
        self.assertIn('R', rows[new]['git'])
        self.assertEqual(rows[new]['bytes'], (self.root / new).stat().st_size)

    def test_git_failure_does_not_publish_empty_success_manifest(self):
        self.run_scan()
        latest = (self.state / 'cleaner/latest.json').read_bytes()
        other = Path(self.temp.name) / 'not-a-repo'
        other.mkdir()
        result = subprocess.run([str(SCAN), '--once'], env={**self.env, 'MESH_REPO': str(other)},
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.state / 'cleaner/latest.json').read_bytes(), latest)


if __name__ == '__main__':
    unittest.main()
