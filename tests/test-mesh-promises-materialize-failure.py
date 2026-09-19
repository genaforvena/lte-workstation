# Verify failed promise replay preserves the journal and propagates failure.
"""A broken source must never replace the last valid promise journal."""
import os
import subprocess
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='promise-materialize-failure-') as temp:
    root = Path(temp)
    promises = root / 'promises'
    promises.mkdir()
    journal = promises / 'promises.journal'
    previous = b'; last valid promise journal\n'
    board = root / 'chat.log'
    board.write_text('2026-09-19T00:00:00Z alpha@n :: [task-ledger] v1 r=1 | broken=record\n')
    env = dict(os.environ, HOME=temp, MESH_DIR=temp, MESH_PROMISES_DIR=str(promises),
               MESH_CHAT_LOG=str(board), MESH_PROMISE_ROSTER='alpha',
               MESH_PROMISE_LIVE_WINDOWS='alpha', MESH_PROMISE_NO_POST='1')
    for mode in ('--check', '--balance', '--feed'):
        journal.write_bytes(previous)
        result = subprocess.run(['bash', str(repo / 'scripts/mesh-promises'), mode],
                                env=env, capture_output=True, text=True, timeout=15)
        assert journal.read_bytes() == previous, (mode, 'journal replaced after failed replay')
        assert result.returncode != 0, (mode, result.stdout, result.stderr)
        assert 'replay failed' in result.stderr, (mode, result.stderr)
        print('PASS:', mode, 'preserves journal and propagates failed replay')
