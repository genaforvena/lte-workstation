"""The legacy work horizon covers tasks, claims and holds without erasing text."""
import json
import os
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
old = (datetime.now(timezone.utc) - timedelta(hours=400)).strftime('%Y-%m-%dT%H:%M:%SZ')
recent = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    path.write_text(f'{old} alpha@n :: [task] old-task: investigate ; task:old-task, owner:alpha\n'
                    f'{old} alpha@n :: [taking] old-hold: investigate ; task:old-hold\n'
                    f'{old} beta@n :: [verify] old-check: investigate ; task:old-check, owner:alpha\n'
                    f'{old} operator@n :: [taking] human-hold: waiting ; task:human-hold\n'
                    f'{recent} alpha@n :: [taking] recent-hold: investigate ; task:recent-hold\n')
    before = path.read_bytes()
    env = dict(os.environ, MESH_DIR=td, MESH_CHAT_LOG=str(path), MESH_PROMISE_RETIRE_H='336',
               MESH_PROMISE_ROSTER='alpha beta operator', MESH_ASK_VOICE_IN='/nonexistent', MESH_ASK_TG_SENT='/nonexistent')
    p = subprocess.run(['bash', str(root / 'scripts/mesh-promises'), '--json'], env=env, text=True, capture_output=True)
    assert p.returncode in (0,1), p.stderr
    data = json.loads(p.stdout)
    assert not data['open'] and not data['claims'], data
    assert {r['slug'] for r in data['holds']} == {'human-hold', 'recent-hold'}, data
    assert data['retired_by_kind'] == {'tasks': 1, 'claims': 1, 'holds': 1}, data
    assert path.read_bytes() == before
print('PASS: old legacy work retires consistently; human/recent holds and historical bytes survive')
