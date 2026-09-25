#!/usr/bin/env python3
"""Exercise actual launch boundaries with real authority records and isolated commands."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


def function(script, name):
    """Load the production function, including its real admission/actuator code."""
    source = (SCRIPTS / script).read_text()
    start = list(re.finditer(rf"(?m)^{re.escape(name)}\(\)", source))[-1].start()
    end = re.search(r"(?m)^[})]$", source[start:]).end() + start
    return source[start:end] + "\n"


TMUX = r'''#!/usr/bin/python3
import fcntl, json, os, sys
from pathlib import Path
args = sys.argv[1:]
cmd = args[0]
scenario = os.environ['SCENARIO']
if cmd == 'has-session':
    pass
elif cmd == 'list-windows':
    print('unrelated')
    if scenario != 'absent': print('synthetic')
elif cmd == 'list-panes':
    fmt = args[args.index('-F') + 1] if '-F' in args else ''
    two = scenario in ('collision', 'placeholder', 'channel')
    if fmt == '#{pane_top} #{pane_index}': print('0 0\n12 1' if two else '0 0')
    elif fmt == '#{pane_index}': print('0\n1' if two else '0')
    elif fmt == '#{pane_current_command}': print('bash')
    else: print('pane0\npane1' if two else 'pane0')
elif cmd in ('display', 'display-message'):
    print('12346' if '.1' in ' '.join(args) else '12345')
elif cmd == 'capture-pane':
    if scenario == 'placeholder': print('mind type __lean_skip__ is REMOTE')
    else: print('fixture ready')
elif cmd in ('new-window', 'split-window', 'respawn-pane', 'kill-pane',
             'send-keys', 'load-buffer', 'paste-buffer', 'select-layout'):
    lock = Path(os.environ['MESH_MISHE_HOME']) / 'authority/synthetic.lock'
    held = False
    if lock.exists():
        with lock.open('a') as stream:
            try: fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: held = True
    try:
        os.fstat(201)
        inherited = True
    except OSError: inherited = False
    with open(os.environ['EFFECTS'], 'a') as stream:
        stream.write(json.dumps({'args': args, 'locked': held, 'inherited': inherited}) + '\n')
else:
    raise SystemExit('unexpected tmux command: ' + repr(args))
'''

PS = r'''#!/usr/bin/python3
import os, sys
if 'comm=' in sys.argv:
    print('bash')
else:
    scenario = os.environ['SCENARIO']
    print('mesh-dash synthetic' if scenario in ('data', 'collision') else
          'ssh elsewhere' if scenario == 'occupied' else 'bash -l')
'''


class LaunchBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.bin = self.home / '.local/bin'
        self.bin.mkdir(parents=True)
        (self.home / '.mesh').mkdir()
        self.effects = self.home / 'effects.jsonl'
        self.env = {
            'HOME': str(self.home), 'PATH': f'{self.bin}:/usr/bin:/bin',
            'LANG': 'C.UTF-8', 'MESH_MISHE_HOME': str(self.home / 'mishe'),
            'MESH_MISHE_CORE': str(CORE),
            'MESH_MISHE_AUTHORITY_BIN': str(SCRIPTS / 'mesh-mishe-authority'),
            'EFFECTS': str(self.effects), 'SCENARIO': 'channel',
            'MESH_MIND_WIN': 'synthetic', 'MESH_MIND_CHANNELS': 'synthetic',
            'MESH_CHANNEL_NOTIFY': '0', 'MESH_TELL_ALLOW_SHELL': '1',
            'MESH_TELL_RESUBMIT_CMD': str(SCRIPTS / 'mesh-tell'),
        }
        for name, body in {
            'tmux': TMUX, 'ps': PS, 'pgrep': '#!/bin/sh\nexit 1\n',
            'hostname': '#!/bin/sh\necho fixture\n',
            'sleep': '#!/bin/sh\nexit 0\n',
            'fixture-mind': '#!/bin/sh\nexit 0\n',
            'mesh-chat': '#!/bin/sh\nexit 0\n',
        }.items():
            path = self.bin / name
            path.write_text(body)
            path.chmod(0o755)

    def authority(self, state):
        record = Path(self.env['MESH_MISHE_HOME']) / 'authority/synthetic.json'
        record.parent.mkdir(parents=True, exist_ok=True)
        record.unlink(missing_ok=True)
        if state in ('mishe', 'legacy-record'):
            result = self.authority_cmd('switch', 'synthetic', '--to', 'mishe',
                                        '--expect-generation', '0', '--feed-seq', '0')
            self.assertEqual(result.returncode, 0, result.stderr)
            if state == 'legacy-record':
                result = self.authority_cmd('switch', 'synthetic', '--to', 'legacy',
                                            '--expect-generation', '1', '--feed-seq', '0')
                self.assertEqual(result.returncode, 0, result.stderr)
        elif state == 'unknown':
            record.write_text('unreadable authority JSON')
        for path in (self.home / '.mesh').glob('.mind-relaunch-*'):
            path.unlink()
        self.effects.write_text('')

    def authority_cmd(self, *args):
        return subprocess.run([str(SCRIPTS / 'mesh-mishe-authority'), *args],
                              env=self.env, text=True, capture_output=True, timeout=10)

    def run_shell(self, source, scenario):
        result = subprocess.run(['bash', '-c', source],
                                env={**self.env, 'SCENARIO': scenario}, text=True,
                                capture_output=True, timeout=12)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return self.events()

    def events(self):
        return [json.loads(row) for row in self.effects.read_text().splitlines()]

    def restore(self, scenario):
        return self.run_shell('set -uo pipefail\nS=fixture\n' +
                              function('mesh-restore', 'ensure_channel') +
                              'ensure_channel synthetic synthetic "fixture-mind --persistent"\n',
                              scenario)

    def keep_source(self):
        source = (SCRIPTS / 'mesh-channel-keepalive').read_text()
        definitions = source.split('\nif [ "${1:-}" = --test ]; then', 1)[0]
        return definitions + '\n' + function('mesh-channel-keepalive', 'keep') + \
            function('mesh-channel-keepalive', 'keep_legacy')

    def test_restore_fences_all_mind_creation_without_destroying_data(self):
        for state in ('legacy', 'legacy-record', 'mishe', 'unknown'):
            for scenario in ('absent', 'data', 'shell', 'occupied', 'collision', 'placeholder'):
                with self.subTest(state=state, scenario=scenario):
                    self.authority(state)
                    events = self.restore(scenario)
                    mind = [e for e in events if 'fixture-mind --persistent' in ' '.join(e['args'])]
                    allowed = state.startswith('legacy') and scenario != 'occupied'
                    self.assertEqual(bool(mind), allowed, events)
                    for event in mind:
                        self.assertTrue(event['locked'], event)
                        self.assertFalse(event['inherited'], event)
                    if not state.startswith('legacy') and scenario in ('data', 'collision', 'placeholder'):
                        self.assertFalse(any(e['args'][0] in ('kill-pane', 'respawn-pane', 'send-keys',
                                                             'split-window', 'new-window') for e in events), events)
                    if scenario in ('absent', 'shell', 'occupied'):
                        self.assertTrue(any('mesh-dash synthetic' in ' '.join(e['args']) for e in events), events)
                    self.assertFalse(any('unrelated' in ' '.join(e['args']) for e in events), events)

    def test_keepalive_fences_dead_channel_and_holds_lock_through_relaunch(self):
        for state in ('legacy', 'legacy-record', 'mishe', 'unknown'):
            with self.subTest(state=state):
                self.authority(state)
                events = self.run_shell(self.keep_source() + '\nkeep synthetic fixture-mind\n', 'channel')
                sends = [e for e in events if e['args'][0] == 'send-keys']
                self.assertEqual(len(sends), 2 if state.startswith('legacy') else 0, events)
                for event in sends:
                    self.assertIn('fixture:synthetic.1', event['args'])
                    self.assertTrue(event['locked'], event)
                    self.assertFalse(event['inherited'], event)

    def test_window_keepalive_fences_creation_and_relaunch(self):
        for state in ('legacy', 'legacy-record', 'mishe', 'unknown'):
            for scenario in ('absent', 'shell', 'channel'):
                with self.subTest(state=state, scenario=scenario):
                    self.authority(state)
                    result = subprocess.run([str(SCRIPTS / 'mesh-mind-keepalive')],
                                            env={**self.env, 'SCENARIO': scenario},
                                            text=True, capture_output=True, timeout=12)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    events = self.events()
                    allowed = state.startswith('legacy') and scenario != 'channel'
                    self.assertEqual(sum(e['args'][0] == 'send-keys' for e in events), 2 if allowed else 0, events)
                    self.assertEqual(sum(e['args'][0] == 'new-window' for e in events),
                                     int(allowed and scenario == 'absent'), events)
                    for event in events:
                        self.assertTrue(event['locked'], event)
                        self.assertFalse(event['inherited'], event)

    def test_status_does_not_create_absent_window(self):
        self.authority('legacy')
        result = subprocess.run([str(SCRIPTS / 'mesh-mind-keepalive'), '--status'],
                                env={**self.env, 'SCENARIO': 'absent'},
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.events(), [])

    def test_strand_redrive_fences_direct_key_and_nested_automatic_tell(self):
        for state in ('legacy', 'mishe', 'unknown'):
            with self.subTest(state=state):
                self.authority(state)
                source = function('mesh-channel-keepalive', 'strand_resubmit') + \
                    'strand_resubmit synthetic fixture:synthetic.1 "recover fixture payload"\n'
                result = subprocess.run(['bash', '-c', source],
                                        env=self.env, text=True, capture_output=True, timeout=12)
                events = self.events()
                if state == 'legacy':
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue(any(e['args'][0] == 'send-keys' and e['args'][-1] == 'C-m'
                                        for e in events), events)
                    self.assertTrue(any(e['args'][0] == 'paste-buffer' for e in events), events)
                    for event in events:
                        self.assertTrue(event['locked'], event)
                        self.assertFalse(event['inherited'], event)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(events, [])

    def test_missing_authority_program_is_not_legacy(self):
        self.authority('legacy')
        self.env['MESH_MISHE_AUTHORITY_BIN'] = str(self.home / 'missing-authority')
        events = self.restore('absent')
        self.assertEqual([e['args'][0] for e in events], ['new-window', 'select-layout'])
        self.effects.write_text('')
        self.assertEqual(self.run_shell(self.keep_source() + '\nkeep synthetic fixture-mind\n', 'channel'), [])


if __name__ == '__main__':
    unittest.main()
