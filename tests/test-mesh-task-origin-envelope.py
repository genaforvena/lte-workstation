import json
import os
import subprocess
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'scripts' / 'mesh-task'

FIELDS = ('kind', 'source', 'hypothesis', 'question', 'acceptance', 'feedback')


def plan(origin=None):
    lines = []
    for key, value in (origin or {}).items():
        lines.append(f'#{key}={value}')
    lines.append('alpha\twork\tproduce evidence')
    return '\n'.join(lines) + '\n'


def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        mesh = tmp / 'mesh'
        board = tmp / 'board'
        writer = tmp / 'writer'
        writer.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "$TEST_BOARD"\n')
        writer.chmod(0o700)
        env = dict(os.environ, MESH_DIR=str(mesh), MESH_TASK_DIR=str(mesh / 'chains'),
                   MESH_TASK_CHAT_CMD=str(writer), TEST_BOARD=str(board), MESH_TASK_ACTOR='alpha')
        complete = dict(zip(FIELDS, ('literature', 'brief:42', 'claim', 'question', 'command', 'none')))

        def run(*args, code=0, **extra):
            p = subprocess.run(['python3', str(TASK), *args], env=dict(env, **extra),
                               text=True, capture_output=True)
            assert p.returncode == code, p.stdout + p.stderr
            return p

        p = tmp / 'complete.tsv'; p.write_text(plan({f'origin.{k}': v for k, v in complete.items()}))
        run('create', 'origin', str(p))
        state = json.loads((mesh / 'chains/origin.json').read_text())
        assert state['origin'] == complete
        assert 'brief:42' in run('replay', '--json').stdout

        for missing in FIELDS:
            partial = dict(zip(FIELDS, ('x',) * len(FIELDS)))
            partial.pop(missing)
            q = tmp / f'partial-{missing}.tsv'; q.write_text(plan({f'origin.{k}': v for k, v in partial.items()}))
            assert run('create', f'partial-{missing}', str(q), code=2).returncode == 2
        malformed = tmp / 'malformed.tsv'; malformed.write_text(plan({'origin.kind': 'literature', 'origin.source': '   '}))
        assert run('create', 'malformed', str(malformed), code=2).returncode == 2
        unknown = tmp / 'unknown.tsv'; unknown.write_text(plan({**{f'origin.{k}': v for k, v in complete.items()}, 'origin.provenance': 'typo'}))
        assert 'unknown origin header' in run('create', 'unknown', str(unknown), code=2).stderr
        duplicate_header = tmp / 'duplicate-header.tsv'; duplicate_header.write_text(
            plan({f'origin.{k}': v for k, v in complete.items()}).replace(
                '#origin.source=brief:42\n', '#origin.source=brief:42\n#origin.source=brief:43\n'))
        assert 'duplicate origin header' in run('create', 'duplicate-header', str(duplicate_header), code=2).stderr

        legacy = tmp / 'legacy.tsv'; legacy.write_text(plan())
        run('create', 'legacy', str(legacy))
        duplicate = tmp / 'duplicate.tsv'; duplicate.write_text(plan({f'origin.{k}': v for k, v in complete.items()}))
        err = run('create', 'duplicate', str(duplicate), code=2).stderr
        assert "origin.source 'brief:42' already exists in chain 'origin' (status: open)" in err
        assert 'origin' in run('status', 'origin').stdout
        # Settle the first chain, then ensure the canonical settled chain is still a duplicate.
        artifact = tmp / 'artifact'; artifact.write_text('evidence')
        run('take', 'origin', 'work')
        run('done', 'origin', 'work', str(artifact), 'verified')
        settled = run('create', 'settled-duplicate', str(duplicate), code=2).stderr
        assert "origin.source 'brief:42' already exists in chain 'origin' (status: complete)" in settled
        (mesh / 'chains/origin.json').unlink()
        run('rebuild')
        assert json.loads((mesh / 'chains/origin.json').read_text())['origin'] == complete

        # Canonical replay rejects an envelope with any key outside the exact six-key set.
        log = mesh / 'chat.log'
        record = json.loads((mesh / 'chains/origin.json').read_text())
        record['origin']['extra'] = 'must-refuse'
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location('mesh_task_log', ROOT / 'scripts' / 'mesh_task_log.py')
        module = module_from_spec(spec); spec.loader.exec_module(module)
        try:
            module.encode(record, 99)
        except ValueError as exc:
            assert 'exactly six' in str(exc)
        else:
            raise AssertionError('extra canonical origin key accepted')

        # Two independent creators race; canonical chat.log may contain only one source.
        race_plan = tmp / 'race.tsv'; race_plan.write_text(plan({f'origin.{k}': v for k, v in complete.items()}).replace('brief:42', 'race:1'))
        results = []
        def creator(name):
            results.append(subprocess.run(['python3', str(TASK), 'create', name, str(race_plan)],
                                          env=env, text=True, capture_output=True))
        a = threading.Thread(target=creator, args=('race-a',)); b = threading.Thread(target=creator, args=('race-b',))
        a.start(); b.start(); a.join(); b.join()
        assert sorted(p.returncode for p in results) == [0, 2]
        loser = next(p for p in results if p.returncode == 2)
        winner = next(p for p in results if p.returncode == 0)
        winner_name = 'race-a' if 'race-a' in winner.stdout else 'race-b'
        assert f"origin.source 'race:1' already exists in chain '{winner_name}' (status: open)" in loser.stderr
        replay = module.replay(log)
        assert sum(r['data'].get('origin', {}).get('source') == 'race:1' for r in replay.values()) == 1
    print('PASS: origin envelope, refusal, duplicate status, legacy replay, and cache rebuild')


if __name__ == '__main__':
    main()
