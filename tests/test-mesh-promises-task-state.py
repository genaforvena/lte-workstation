"""Prose receipts cannot override committed structured task state."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from mesh_task_log import encode
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    env = dict(os.environ, MESH_DIR=td, MESH_CHAT_LOG=str(path), MESH_ASK_VOICE_IN='/nonexistent',
               MESH_ASK_TG_SENT='/nonexistent', MESH_PROMISE_ROSTER='alpha beta', MESH_PROMISE_RETIRE_H='0')
    data = dict(chain='plan', current=0, status='open', created='2026-09-08T00:00:00Z', steps=[
        dict(id='plan/work', slug='work', owner='alpha', status='open', description='produce evidence'),
        dict(id='plan/check', slug='check', owner='beta', status='open', description='verify evidence')])
    def query(prose):
        path.write_text(prose + '2026-09-08T00:00:02Z alpha@n :: ' + encode(data, 1) + '\n')
        p = subprocess.run(['bash', str(root / 'scripts/mesh-promises'), '--json'], env=env, text=True, capture_output=True)
        assert p.returncode in (0, 1), p.stderr
        result = json.loads(p.stdout)
        assert 'error' not in result, result
        return result
    task = '2026-09-08T00:00:00Z alpha@n :: [task] plan/work: produce evidence ; task:plan/work, owner:alpha\n'
    taking = '2026-09-08T00:00:01Z alpha@n :: [taking] plan/work: starting ; task:plan/work\n'
    done = '2026-09-08T00:00:03Z alpha@n :: [done] plan/work: purported completion ; task:plan/work\n'
    result = query(task + taking + done)
    assert len(result['open']) == 1 and not result['holds'], result
    data['status'] = data['steps'][0]['status'] = 'active'
    data['steps'][0]['started'] = '2026-09-08T00:00:01Z'
    result = query(task + done)
    assert len(result['open']) == 1 and len(result['holds']) == 1, result
    data['status'] = data['steps'][0]['status'] = 'blocked'
    result = query(task + taking)
    assert len(result['open']) == 1 and not result['holds'], result
    data['status'] = 'complete'
    data['current'] = 1
    for step in data['steps']:
        step.update(status='done', finished='2026-09-08T00:00:04Z', artifact='/evidence', artifact_sha256='a'*64)
    result = query(task + taking)
    assert not result['open'] and not result['holds'] and result['kept'] == 2, result
    independent = ('2026-09-08T00:00:00Z alpha@n :: [task] independent: produce evidence ; task:independent, owner:alpha\n'
                   '2026-09-08T00:00:01Z alpha@n :: [taking] independent: produce evidence ; task:independent\n'
                   '2026-09-08T00:00:01Z beta@n :: [verify] check-other: produce evidence ; task:check-other, owner:alpha\n')
    result = query(task + independent)
    assert [row['slug'] for row in result['open']] == ['independent'], result
    assert len(result['holds']) == 1, result
    assert len(result['claims']) == 1, result
print('PASS: committed task state wins provisional receipts; blocked/future steps hold no worker; completed work stays closed')
