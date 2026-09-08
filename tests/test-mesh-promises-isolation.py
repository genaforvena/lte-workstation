"""A custom mesh directory isolates every summary/state output from real HOME."""
import os
import subprocess
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    home = root / 'home'
    default = home / '.mesh'
    custom = root / 'fixture-mesh'
    default.mkdir(parents=True)
    custom.mkdir()
    sentinel = default / '.promises-summary'
    sentinel.write_text('REAL STATE MUST SURVIVE\n')
    (custom / 'chat.log').write_text(
        '2026-09-08T00:00:00Z test@n :: [task] isolated: fixture owner:genome\n')
    env = dict(os.environ, HOME=str(home), MESH_DIR=str(custom),
               MESH_CHAT_LOG=str(custom / 'chat.log'),
               MESH_PROMISES_DIR=str(custom / 'promises'),
               MESH_PROMISE_ROSTER='genome', MESH_PROMISE_RETIRE_H='0',
               MESH_ASK_VOICE_IN=str(custom / 'no-voice'),
               MESH_ASK_TG_SENT=str(custom / 'no-tg'))
    result = subprocess.run(['bash', str(repo / 'scripts/mesh-promises'), '--feed'],
                            env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sentinel.read_text() == 'REAL STATE MUST SURVIVE\n', 'fixture overwrote default summary'
    assert (custom / '.promises-summary').is_file(), 'custom summary missing'
    assert (custom / 'promises/promises.journal').is_file(), 'custom journal missing'
print('PASS: custom mesh feed leaves default HOME summary untouched')
