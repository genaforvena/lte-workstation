"""One-time import and disposable cache recovery from the text board."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

tool = Path(__file__).resolve().parents[1] / 'scripts/mesh-task'
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    chains = root / 'task-chains'
    chains.mkdir()
    data = dict(chain='legacy', current=0, status='blocked', dispatch='sent', steps=[
        dict(id='legacy/work', slug='work', owner='alpha', status='blocked',
             description='produce evidence', block_type='dependency', retry='event:ready')])
    cache = chains / 'legacy.json'
    cache.write_text(json.dumps(data))
    env = dict(os.environ, MESH_DIR=str(root), MESH_TASK_DIR=str(chains))
    def run(*args, code=0):
        p = subprocess.run(['python3', str(tool), *args], env=env, text=True, capture_output=True)
        assert p.returncode == code, p.stdout + p.stderr
        return p.stdout
    assert 'imported=1' in run('import')
    tape = (root / 'chat.log').read_bytes()
    assert 'imported=0' in run('import')
    assert (root / 'chat.log').read_bytes() == tape
    cache.write_text('{broken cache')
    contexts = root / 'task-context'
    contexts.mkdir(exist_ok=True)
    (contexts / 'alpha.json').write_text('{broken context')
    assert 'legacy [blocked]' in run('status', 'legacy')
    run('rebuild')
    assert json.loads(cache.read_text()) == data
    assert json.loads((contexts / 'alpha.json').read_text())[0]['status'] == 'blocked'
    assert (root / 'chat.log').read_bytes() == tape
    cache.unlink()
    (contexts / 'alpha.json').unlink()
    run('rebuild')
    assert json.loads(cache.read_text()) == data
    assert 'BLOCKED\talpha\tlegacy/work' in run('audit')
    ghost = dict(data, chain='unimported', steps=[dict(data['steps'][0], id='unimported/work')])
    (chains / 'unimported.json').write_text(json.dumps(ghost))
    run('status', 'unimported', code=2)
    assert 'unimported/work' not in run('audit')
    (root / 'chat.log').unlink()
    run('audit', code=1)
    run('rebuild', code=1)
print('PASS: explicit idempotent import; deleted/corrupt caches rebuild solely from chat.log')
