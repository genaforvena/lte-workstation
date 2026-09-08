"""Replay complete task-chain records from the append-only chat.log.

No persistent index: revisions make duplicate delivery harmless and conflicting
or missing records explicit. The writer must append before updating its cache.
"""
from __future__ import annotations

import json
import re
import fcntl
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

MARKER = '[task-state] '
EVENT = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\s+\S+\s+::\s+\[task-state\] (.*)$')
EVENT_BYTES = re.compile(EVENT.pattern.encode('ascii'))


class ReplayError(ValueError):
    pass


def validate(record: dict) -> None:
    if not isinstance(record, dict) or record.get('schema') != 1:
        raise ReplayError('unsupported task-state schema')
    revision = record.get('revision')
    data = record.get('data')
    if type(revision) is not int or revision < 1:
        raise ReplayError('invalid task-state revision')
    if not isinstance(data, dict) or not isinstance(data.get('chain'), str) or not data['chain']:
        raise ReplayError('missing task-state chain')
    steps = data.get('steps')
    current = data.get('current')
    if not isinstance(steps, list) or not steps or type(current) is not int or not 0 <= current < len(steps):
        raise ReplayError('invalid task-state steps/current')
    seen = set()
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get('slug'), str):
            raise ReplayError('invalid task-state step')
        if step.get('id') != f"{data['chain']}/{step['slug']}" or step['id'] in seen:
            raise ReplayError('invalid or duplicate task-state identity')
        seen.add(step['id'])
        if not step.get('status'):
            raise ReplayError('missing task-state status')
        owner = step.get('owner')
        if owner is not None and (not isinstance(owner, str) or not owner.strip()):
            raise ReplayError('invalid task-state owner')
        if step['status'] in ('active', 'running', 'claimed') and not owner:
            raise ReplayError('started task has no assigned owner')


def encode(data: dict, revision: int) -> str:
    record = {'schema': 1, 'revision': revision, 'data': data}
    validate(record)
    return MARKER + json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def eligibility(records: dict, task: str, mode: str, owner: str) -> int:
    """0 eligible, 2 canonical refusal, 3 not represented in structured records."""
    if mode not in ('dispatch', 'resume', 'pending'):
        raise ReplayError('invalid eligibility mode')
    matches = []
    for record in records.values():
        data = record['data']
        for index, step in enumerate(data['steps']):
            alias = re.sub(r'[\W_]+', '-', step['id'].lower()).strip('-')
            if task in (step['id'], alias):
                matches.append((data, index, step))
    if not matches:
        return 3
    if len(matches) != 1:
        raise ReplayError(f'ambiguous task identity: {task}')
    data, index, step = matches[0]
    if index != data['current'] or data.get('status') not in ('open', 'active'):
        return 2
    if mode != 'pending' and step.get('owner') and owner != step['owner']:
        return 2
    expected = ('open',) if mode in ('dispatch', 'pending') else ('active', 'running', 'claimed')
    return 0 if step['status'] in expected else 2


def ledger_projection(records: dict, events: list) -> list:
    """Derive legacy accounting views from committed tasks, never provisional prose.

    Generated tuples are in-memory accounting inputs, not board/start receipts.
    Keep them after unrelated prose so heuristics cannot settle canonical work.
    """
    aliases = {}
    for record in records.values():
        for step in record['data']['steps']:
            for key in (step['id'], re.sub(r'[\W_]+', '-', step['id'].lower()).strip('-')):
                aliases.setdefault(key, set()).add(step['id'])
    retained = []
    for event in events:
        body = event[4]
        tags = re.findall(r'task:([^\s,;()]+)', body)
        key = tags[0] if tags else body.partition(':')[0].strip()
        matches = aliases.get(key, set())
        if len(matches) > 1:
            raise ReplayError(f'ambiguous accounting task identity: {key}')
        if not matches:
            retained.append(event)
    def stamp(value):
        if not value:
            raise ReplayError('task accounting requires a recorded timestamp')
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    for record in records.values():
        data = record['data']
        for index, step in enumerate(data['steps']):
            status = step['status']
            if index > data['current'] or status in ('retired', 'cancelled'):
                continue
            owner = step.get('owner') or '-'
            body = f"{step['id']}: {step.get('description', '')} ; task:{step['id']}, owner:{owner}"
            opened = stamp(data.get('created') or step.get('started'))
            retained.append((opened, 'task', owner, owner, body))
            if status in ('active', 'running', 'claimed'):
                retained.append((stamp(step.get('started')), 'taking', owner, owner, body))
            elif status == 'done':
                retained.append((stamp(step.get('finished')), 'done', owner, owner,
                                 body + f" artifact={step.get('artifact', '')}"))
    return retained


def replay(path: Path) -> dict[str, dict]:
    """Return each chain's latest record; gaps/conflicts never become empty success."""
    records: dict[str, dict[int, dict]] = {}
    with path.open('rb') as source:
        for number, line in enumerate(source, 1):
            match = EVENT_BYTES.match(line.rstrip(b'\n'))
            if not match:
                continue
            try:
                if not line.endswith(b'\n'):
                    raise ReplayError('incomplete task-state line')
                record = json.loads(match.group(1).decode('utf-8'))
                validate(record)
                chain = record['data']['chain']
                revision = record['revision']
                revisions = records.setdefault(chain, {})
                if revision in revisions and revisions[revision] != record:
                    raise ReplayError(f'conflicting task-state revision {chain}/{revision}')
                revisions[revision] = record
            except (ValueError, TypeError, KeyError) as exc:
                raise ReplayError(f'{path}:{number}: {exc}') from exc
    latest = {}
    for chain, revisions in records.items():
        ordered = sorted(revisions)
        if ordered != list(range(1, ordered[-1] + 1)):
            raise ReplayError(f'missing task-state revision for {chain}')
        latest[chain] = revisions[ordered[-1]]
    return latest


def append(root: Path, who: str, payload: str) -> None:
    """The mesh-chat structured append path: exact bytes, locked and durable."""
    record = json.loads(payload)
    validate(record)
    if not who or any(c.isspace() for c in who):
        raise ReplayError('invalid task-state author')
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'chat.log'
    with (root / '.chat.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        states = replay(path) if path.exists() else {}
        previous = states.get(record['data']['chain'])
        if previous == record:
            return
        expected = previous['revision'] + 1 if previous else 1
        if record['revision'] != expected:
            raise ReplayError(f'task-state revision conflict: expected {expected}')
        line = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '  ' + who + '  ::  ' + encode(record['data'], record['revision']) + '\n'
        scrub = subprocess.run([sys.executable, str(Path(__file__).with_name('mesh-log-scrub'))],
                               input=line, text=True, capture_output=True, check=False)
        if scrub.returncode or scrub.stdout != line:
            raise ReplayError('task-state rejected: log scrub would alter structured data')
        with path.open('a', encoding='utf-8') as output:
            output.write(line)
            output.flush()
            os.fsync(output.fileno())


if __name__ == '__main__':
    try:
        if len(sys.argv) != 5 or sys.argv[1] != 'append':
            raise ReplayError('usage: mesh_task_log.py append <mesh-dir> <author> <json>')
        append(Path(sys.argv[2]), sys.argv[3], sys.argv[4])
    except (OSError, ValueError) as exc:
        print(f'mesh-task-log: {exc}', file=sys.stderr)
        sys.exit(1)
