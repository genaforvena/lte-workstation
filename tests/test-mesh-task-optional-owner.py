"""Create, claim, complete and hand off a chain whose owners are not predefined."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    plan = tmp / 'plan.tsv'
    plan.write_text('-\twork\tproduce evidence\n\tcheck\tverify evidence\n')
    artifact = tmp / 'evidence.txt'
    artifact.write_text('result\n')
    board = tmp / 'board'
    writer = tmp / 'writer'
    writer.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "$TEST_BOARD"\n')
    writer.chmod(0o700)
    env = dict(os.environ, MESH_DIR=str(tmp / 'mesh'), MESH_TASK_DIR=str(tmp / 'mesh/chains'),
               MESH_TASK_CHAT_CMD=str(writer), MESH_TASK_HANDOFF_CMD='/bin/false',
               TEST_BOARD=str(board), MESH_TASK_ACTOR='alpha')
    def run(*args, code=0, **overrides):
        p = subprocess.run(['python3', str(root / 'scripts/mesh-task'), *args],
                           env=dict(env, **overrides), text=True, capture_output=True)
        assert p.returncode == code, p.stdout + p.stderr
        return p
    def state():
        return json.loads((tmp / 'mesh/chains/demo.json').read_text())
    run('create', 'demo', str(plan))
    assert state()['steps'][0]['owner'] is None
    assert 'owner:' not in board.read_text()
    run('take', 'demo', 'work', code=1, MESH_TASK_CHAT_CMD='/bin/false')
    assert state()['steps'][0]['owner'] is None
    run('take', 'demo', 'work')
    assert state()['steps'][0]['owner'] == 'alpha'
    (tmp / 'mesh/chains/demo.json').unlink()
    (tmp / 'mesh/task-context/alpha.json').unlink()
    assert 'demo [active]' in run('status', 'demo').stdout
    assert 'demo/work' in run('audit').stdout
    run('create', 'second', str(plan))
    busy = run('take', 'second', 'work', code=2)
    assert 'already has active task' in busy.stderr
    run('take', 'demo', 'work', code=2, MESH_TASK_ACTOR='beta')
    run('done', 'demo', 'work', str(artifact), 'verified')
    assert state()['current'] == 1 and state()['steps'][1]['owner'] is None
    assert 'successor task:demo/check awaits assignment' in board.read_text()
    run('take', 'demo', 'check', MESH_TASK_ACTOR='beta')
    run('done', 'demo', 'check', str(artifact), 'checked', MESH_TASK_ACTOR='beta')
    assert state()['status'] == 'complete'
    run('create', 'cache-failure', str(plan))
    cache = tmp / 'mesh/chains/cache-failure.json'
    cache.unlink()
    cache.mkdir()  # Force cache replacement to fail AFTER the text record commits.
    run('take', 'cache-failure', 'work', code=1, MESH_TASK_ACTOR='gamma')
    assert 'cache-failure [active]' in run('status', 'cache-failure').stdout
    assert 'cache-failure/work' in run('audit').stdout
    cache.rmdir()
    run('done', 'cache-failure', 'work', str(artifact), 'recovered', MESH_TASK_ACTOR='gamma')
    assert json.loads(cache.read_text())['steps'][0]['status'] == 'done'
print('PASS: optional owner, failed receipt rollback, cache-loss/write-failure recovery, exclusive claim, and unassigned successor')
