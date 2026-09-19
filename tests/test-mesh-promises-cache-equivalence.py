# Verify cold, warm and appended promise accounting matches uncached replay.
"""Cached promises replay produces exactly the uncached accounting output."""
import copy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo / 'scripts'))
from mesh_task_log import encode

source = (repo / 'scripts/mesh-promises').read_text()
code = source.split("  python3 - \"$@\" <<'PYEOF'\n", 1)[1].split('\nPYEOF', 1)[0]
original = code.replace('replay_cached as replay_tasks', 'replay as replay_tasks')
assert original != code, 'promises must use the shared content-verified cache'

with tempfile.TemporaryDirectory(prefix='promises-cache-equivalence-') as temp:
    path = Path(temp) / 'chat.log'
    env = dict(os.environ, MESH_TASK_LIB=str(repo / 'scripts'), MESH_PROMISE_ROSTER='alpha beta',
               MESH_ASK_VOICE_IN=str(Path(temp) / 'voice'), MESH_ASK_TG_SENT=str(Path(temp) / 'sent'))
    data = dict(chain='plan', current=0, status='open', created='2026-09-08T00:00:00Z', steps=[
        dict(id='plan/work', slug='work', owner='alpha', status='open', description='produce evidence')])
    path.write_text('2026-09-08T00:00:00Z alpha@n :: [task] independent: retain old obligation\n'
                    + '2026-09-08T00:00:01Z alpha@n :: ' + encode(data, 1) + '\n')
    def compare(label):
        outputs = []
        for implementation in (code, original):
            run = subprocess.run([sys.executable, '-', 'json', str(path),
                                  '2026-09-19T13:00:00Z', '24', '6', '2'],
                                 env=env, input=implementation, capture_output=True, text=True, timeout=15)
            outputs.append((run.returncode, run.stdout, run.stderr))
        assert outputs[0] == outputs[1], (label, outputs)
        assert outputs[0][0] in (0, 1), outputs
        print('PASS:', label)
    compare('cold accounting equivalence')
    assert path.with_name('.task-replay-cache.json').exists()
    compare('warm accounting equivalence')
    active = copy.deepcopy(data)
    active['status'] = active['steps'][0]['status'] = 'active'
    active['steps'][0]['started'] = '2026-09-08T00:00:02Z'
    with path.open('a') as out:
        out.write('2026-09-08T00:00:02Z alpha@n :: ' + encode(active, 2) + '\n')
    compare('appended accounting equivalence')
