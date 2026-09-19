# Verify cached replay detects changed history and incomplete structured tails.
"""The shared cache must preserve full replay's content and failure semantics."""
import copy
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from mesh_task_log import ReplayError, encode, replay, replay_cached

data = dict(chain='plan', current=0, status='open', created='2026-09-08T00:00:00Z', steps=[
    dict(id='plan/work', slug='work', owner='alpha', status='open', description='produce evidence')])

def line(record, revision=1):
    return '2026-09-08T00:00:00Z alpha@n :: ' + encode(record, revision) + '\n'

def verdict(fn, path):
    try:
        return fn(path)
    except ReplayError:
        return 'ERROR'

with tempfile.TemporaryDirectory(prefix='task-cache-integrity-') as temp:
    for scenario in ('same-size', 'preserved-mtime', 'rewrite-append', 'partial', 'append', 'conflict'):
        folder = Path(temp) / scenario
        folder.mkdir()
        path = folder / 'chat.log'
        initial = line(data)
        path.write_text(initial)
        assert replay_cached(path) == replay(path)
        before = path.stat()
        changed = copy.deepcopy(data)
        changed['steps'][0]['owner'] = 'bravo'
        if scenario in ('same-size', 'preserved-mtime', 'rewrite-append'):
            path.write_text(line(changed) + ('ordinary appended prose\n' if scenario == 'rewrite-append' else ''))
            os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns + (0 if scenario == 'preserved-mtime' else 1000000)))
        elif scenario == 'partial':
            with path.open('a') as out:
                out.write(line(changed, 2).rstrip('\n'))
        else:
            with path.open('a') as out:
                out.write(line(changed, 1 if scenario == 'conflict' else 2))
        expected = verdict(replay, path)
        actual = verdict(replay_cached, path)
        assert actual == expected, (scenario, actual, expected)
        print('PASS:', scenario)
