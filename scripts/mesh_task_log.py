"""Replay complete task-chain records from the append-only chat.log.

No persistent index: revisions make duplicate delivery harmless and conflicting
or missing records explicit. The writer must append before updating its cache.
"""
from __future__ import annotations

import base64
import json
import plistlib
import re
import fcntl
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

MARKER = '[task-ledger] '
LEGACY_MARKER = '[task-state] '
READABLE_HEADER = re.compile(r'^v1 r=([1-9][0-9]*)$')
EVENT = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\s+\S+\s+::\s+\[(task-state|task-ledger)\] (.*)$')
EVENT_BYTES = re.compile(EVENT.pattern.encode('ascii'))
ASK_KEY = re.compile(r'^(?:ask:)?(\d{8}T?\d{6}Z)$', re.IGNORECASE)
ASK_ISO = re.compile(r'^(?:ask:)?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)$', re.IGNORECASE)
ORIGIN_FIELDS = ('kind', 'source', 'hypothesis', 'question', 'acceptance', 'feedback')


class ReplayError(ValueError):
    pass


def replay_source(path: Path) -> dict[str, object]:
    """Consume every chat.log record line-by-line and return tamper-evident coverage.

    Ordinary prose and invalid UTF-8 are source events, but are not task entities.
    Malformed structured task-state records are counted as source errors and do not
    stop later records from being consumed. They must be accounted for without
    being interpreted as promises, claims, or holds in the task view.
    """
    events = 0
    errors = 0
    total_bytes = 0
    complete = True
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for raw_line in source:
            events += 1
            total_bytes += len(raw_line)
            digest.update(raw_line)
            if not raw_line.endswith(b'\n'):
                complete = False
            try:
                line = raw_line.rstrip(b'\n')
                match = EVENT_BYTES.match(line)
                if match:
                    decode(match.group(2))
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, KeyError):
                errors += 1
                continue
    return {
        "events": events,
        "replayed_events": events,
        "errors": errors,
        "bytes": total_bytes,
        "sha256": digest.hexdigest(),
        "complete": complete,
    }


def validate(record: dict) -> None:
    if not isinstance(record, dict) or record.get('schema') != 1:
        raise ReplayError('unsupported task-state schema')
    revision = record.get('revision')
    data = record.get('data')
    if type(revision) is not int or revision < 1:
        raise ReplayError('invalid task-state revision')
    if not isinstance(data, dict) or not isinstance(data.get('chain'), str) or not data['chain']:
        raise ReplayError('missing task-state chain')
    origin = data.get('origin')
    if origin is not None and (not isinstance(origin, dict) or set(origin) != set(ORIGIN_FIELDS) or any(
            not isinstance(origin.get(field), str) or not origin[field].strip()
            for field in ORIGIN_FIELDS)):
        raise ReplayError('origin envelope requires exactly six nonempty fields')
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
        if step['status'] == 'ignored' and (not isinstance(step.get('ignored_reason'), str)
                                           or not step['ignored_reason'].strip()):
            raise ReplayError('ignored task-state step has no reason')
        if step['status'] == 'rejected' and (not isinstance(step.get('rejected_reason'), str)
                                            or not step['rejected_reason'].strip()):
            raise ReplayError('rejected task-state step has no reason')
        owner = step.get('owner')
        if owner is not None and (not isinstance(owner, str) or not owner.strip()):
            raise ReplayError('invalid task-state owner')
        if step['status'] in ('active', 'running', 'claimed') and not owner:
            raise ReplayError('started task has no assigned owner')


def _escape(value: str) -> str:
    out = []
    for char in value:
        code = ord(char)
        if char in ('%', '|', '\n', '\r') or code < 0x20 or code == 0x7f:
            out.append(f'%{code:02X}')
        else:
            out.append(char)
    return ''.join(out)


def _unescape(value: str) -> str:
    out = []
    index = 0
    while index < len(value):
        if value[index] != '%':
            out.append(value[index])
            index += 1
            continue
        if index + 2 >= len(value) or not re.fullmatch(r'[0-9A-F]{2}', value[index + 1:index + 3]):
            raise ReplayError('malformed readable percent escape')
        code = int(value[index + 1:index + 3], 16)
        if code not in (0x25, 0x7c, 0x0a, 0x0d) and not (code < 0x20 or code == 0x7f):
            raise ReplayError('readable escape is not a grammar-breaking byte')
        out.append(chr(code))
        index += 3
    return ''.join(out)


def _pointer_key(value: str) -> str:
    return value.replace('~', '~0').replace('/', '~1')


def _pointer_unkey(value: str) -> str:
    out = []
    index = 0
    while index < len(value):
        if value[index] != '~':
            out.append(value[index])
            index += 1
        elif value[index:index + 2] == '~0':
            out.append('~')
            index += 2
        elif value[index:index + 2] == '~1':
            out.append('/')
            index += 2
        else:
            raise ReplayError('malformed readable JSON pointer escape')
    return ''.join(out)


def _typed(value: object) -> str:
    if isinstance(value, str):
        return 's:' + _escape(value)
    if value is None:
        return 'n:null'
    if type(value) is bool:
        return 'b:' + ('true' if value else 'false')
    if type(value) is int:
        return 'i:' + str(value)
    raise ReplayError('readable ledger supports only string, integer, boolean, and null leaves')


def _flatten(value: object, path: str = '') -> list[tuple[str, str]]:
    if isinstance(value, dict):
        if not value:
            raise ReplayError('readable ledger cannot encode an empty object')
        result = []
        for key in sorted(value):
            if not isinstance(key, str):
                raise ReplayError('readable ledger object key is not a string')
            result.extend(_flatten(value[key], path + '/' + _pointer_key(key)))
        return result
    if isinstance(value, list):
        if not value:
            raise ReplayError('readable ledger cannot encode an empty list')
        result = []
        for index, item in enumerate(value):
            result.extend(_flatten(item, path + '/' + str(index)))
        return result
    if not path:
        raise ReplayError('readable ledger root must be an object')
    return [(path, _typed(value))]


def encode_readable(data: dict, revision: int) -> str:
    record = {'schema': 1, 'revision': revision, 'data': data}
    validate(record)
    return MARKER + f'v1 r={revision} | ' + ' | '.join(
        f'{path}={typed}' for path, typed in _flatten(data))


def _parse_typed(value: str) -> object:
    if len(value) < 2 or value[1] != ':':
        raise ReplayError('malformed readable typed value')
    kind, raw = value[0], value[2:]
    if kind == 's':
        return _unescape(raw)
    if kind == 'n' and raw == 'null':
        return None
    if kind == 'b' and raw in ('true', 'false'):
        return raw == 'true'
    if kind == 'i' and re.fullmatch(r'-?(?:0|[1-9][0-9]*)', raw):
        return int(raw)
    raise ReplayError('invalid readable typed value')


def _container(next_part: str) -> object:
    return [] if re.fullmatch(r'(?:0|[1-9][0-9]*)', next_part) else {}


def _insert(root: dict, parts: list[str], value: object) -> None:
    current: object = root
    for index, part in enumerate(parts):
        last = index == len(parts) - 1
        if isinstance(current, dict):
            if not part:
                raise ReplayError('empty readable pointer segment')
            if last:
                if part in current:
                    raise ReplayError('duplicate readable ledger path')
                current[part] = value
                return
            if part not in current:
                current[part] = _container(parts[index + 1])
            current = current[part]
        elif isinstance(current, list):
            if not re.fullmatch(r'(?:0|[1-9][0-9]*)', part):
                raise ReplayError('readable list member is not a decimal index')
            position = int(part)
            if position > len(current):
                raise ReplayError('sparse readable list')
            if position == len(current):
                current.append(value if last else _container(parts[index + 1]))
                if last:
                    return
                current = current[position]
                continue
            if last:
                if current[position] is not None:
                    raise ReplayError('duplicate readable ledger path')
                current[position] = value
                return
            current = current[position]
        else:
            raise ReplayError('readable scalar/list shape conflict')


def decode_readable(payload: str) -> dict:
    fields = payload.split(' | ')
    header = READABLE_HEADER.fullmatch(fields[0]) if fields else None
    if not header or len(fields) < 2:
        raise ReplayError('invalid readable ledger header')
    revision = int(header.group(1))
    data: dict = {}
    seen_paths = set()
    for clause in fields[1:]:
        if '=' not in clause:
            raise ReplayError('malformed readable ledger field')
        pointer, typed = clause.split('=', 1)
        if not pointer.startswith('/'):
            raise ReplayError('readable ledger path is not rooted')
        parts = [_pointer_unkey(part) for part in pointer[1:].split('/')]
        if any(part == '' for part in parts):
            raise ReplayError('empty readable ledger path')
        if pointer in seen_paths:
            raise ReplayError('duplicate readable ledger path')
        seen_paths.add(pointer)
        _insert(data, parts, _parse_typed(typed))
    record = {'schema': 1, 'revision': revision, 'data': data}
    validate(record)
    return record


def encode(data: dict, revision: int) -> str:
    return encode_readable(data, revision)


def decode(payload: str | bytes) -> dict:
    """Decode readable v1 records and historical JSON/plist64 records."""
    if isinstance(payload, bytes):
        payload = payload.decode('utf-8')
    if payload.startswith('v1 '):
        return decode_readable(payload)
    if payload.startswith('plist64:'):
        encoded = payload.removeprefix('plist64:')
        encoded += '=' * (-len(encoded) % 4)
        try:
            record = plistlib.loads(base64.urlsafe_b64decode(encoded.encode('ascii')))
        except (ValueError, TypeError, plistlib.InvalidFileException) as exc:
            raise ReplayError(f'invalid plist64 task-state payload: {exc}') from exc
    else:
        record = json.loads(payload)
    validate(record)
    return record


def canonical_ask_records(records: dict) -> dict[str, dict]:
    """Project task-owned asks from committed state, keyed by the ask arrival id.

    ``mesh-promises`` historically replayed the voice inbox and board citations as
    an independent ASK commodity.  A task state's ``ask`` field is now the durable
    identity; this projection lets the accounting view use the task's explicit
    ``done``/``ignored`` terminal state without inventing a second closure path.
    Non-timestamp ask keys (for example human campaign labels) remain ordinary task
    metadata until they acquire a dedicated source record.
    """
    projected: dict[str, dict] = {}
    for record in records.values():
        data = record['data']
        raw = data.get('ask')
        if not isinstance(raw, str):
            continue
        value = raw.strip()
        iso_match = ASK_ISO.fullmatch(value)
        match = ASK_KEY.fullmatch(value)
        if iso_match:
            aid = re.sub(r'[-:]', '', iso_match.group(1)).upper()
            iso = iso_match.group(1).upper()
        elif match:
            aid = match.group(1).upper()
            if len(aid) == 16:  # compact YYYYMMDDTHHMMSSZ
                iso = f'{aid[:4]}-{aid[4:6]}-{aid[6:8]}T{aid[9:11]}:{aid[11:13]}:{aid[13:15]}Z'
            else:  # compact YYYYMMDDHHMMSSZ
                iso = f'{aid[:4]}-{aid[4:6]}-{aid[6:8]}T{aid[8:10]}:{aid[10:12]}:{aid[12:14]}Z'
        else:
            continue
        step = data['steps'][data['current']]
        terminal = data.get('status') in ('complete', 'ignored', 'rejected') or step.get('status') in ('done', 'ignored', 'rejected')
        closed = step.get('finished') if step.get('status') == 'done' else step.get('rejected') or step.get('ignored')
        if terminal and not closed:
            closed = data.get('finished') or data.get('rejected') or data.get('ignored')
        candidate = {
            'id': aid,
            'ts': iso,
            'kind': 'TASK',
            'text': step.get('description', ''),
            'closed': terminal,
            'closed_ts': closed,
            'disposition': 'REJECTED' if step.get('status') in ('ignored', 'rejected') or data.get('status') in ('ignored', 'rejected') else 'DONE',
        }
        prior = projected.get(aid)
        if prior is None or (not prior['closed'] and candidate['closed']):
            projected[aid] = candidate
    return projected


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
            if index > data['current'] or status in ('retired', 'cancelled', 'ignored', 'rejected'):
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
                record = decode(match.group(2))
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
    record = decode(payload)
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
        origin = record['data'].get('origin') or {}
        source = origin.get('source')
        if source:
            for existing_chain, existing_record in states.items():
                if existing_chain == record['data']['chain']:
                    continue
                existing_origin = existing_record['data'].get('origin') or {}
                if existing_origin.get('source') == source:
                    status = existing_record['data'].get('status', 'unknown')
                    raise ReplayError(
                        f"origin.source '{source}' already exists in chain '{existing_chain}' (status: {status})")
        expected = previous['revision'] + 1 if previous else 1
        if record['revision'] != expected:
            raise ReplayError(f'task-state revision conflict: expected {expected}')
        prefix = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '  ' + who + '  ::  '
        line = prefix + encode_readable(record['data'], record['revision']) + '\n'
        scrub = subprocess.run([sys.executable, str(Path(__file__).with_name('mesh-log-scrub'))],
                               input=line, text=True, capture_output=True, check=False)
        if scrub.returncode or scrub.stdout != line:
            raise ReplayError('task-ledger rejected: log scrub would alter structured data')
        with path.open('a', encoding='utf-8') as output:
            output.write(line)
            output.flush()
            os.fsync(output.fileno())


if __name__ == '__main__':
    try:
        if len(sys.argv) != 5 or sys.argv[1] != 'append':
            raise ReplayError('usage: mesh_task_log.py append <mesh-dir> <author> <task-state-payload>')
        append(Path(sys.argv[2]), sys.argv[3], sys.argv[4])
    except (OSError, ValueError) as exc:
        print(f'mesh-task-log: {exc}', file=sys.stderr)
        sys.exit(1)
