"""Synthetic per-channel authority and durable outbox primitives.

This module cannot promote real channels. Legacy producer fencing and the live
sink are separate rollout gates.
"""
from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone


class BoundaryError(ValueError):
    pass


def home() -> Path:
    return Path(os.environ.get("MESH_MISHE_HOME", str(Path.home() / ".mesh/mishe-tauftauf")))


def core_feed():
    core = os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf")
    sys.path.insert(0, str(Path(core) / "src"))
    from mishe_tauftauf.feed import Feed
    return Feed(home())


def synthetic(channel: str) -> None:
    if channel != "synthetic":
        raise BoundaryError("only synthetic may switch or dispatch; real channel fence is not installed")


@contextmanager
def channel_lock(channel: str):
    synthetic(channel)
    directory = home() / "authority"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(directory / f"{channel}.lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
        dirfd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BoundaryError(f"invalid state {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoundaryError(f"invalid state {path.name}: expected object")
    return value


def authority_path(channel: str) -> Path:
    return home() / "authority" / f"{channel}.json"


def read_authority(channel: str) -> dict:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", channel):
        raise BoundaryError("invalid channel")
    path = authority_path(channel)
    if path.is_symlink():
        raise BoundaryError("authority record must not be a symlink")
    if not path.exists():
        return {"channel": channel, "generation": 0, "authority": "legacy", "active_feed_seq": 0,
                "installed_at": None}
    value = read_json(path)
    if (value.get("channel") != channel or type(value.get("generation")) is not int
            or value["generation"] < 1 or value.get("authority") not in ("legacy", "mishe")
            or type(value.get("active_feed_seq")) is not int or value["active_feed_seq"] < 0
            or not isinstance(value.get("installed_at"), str)):
        raise BoundaryError("invalid authority record")
    return value


def outbox_dir(channel: str) -> Path:
    return home() / "outbox" / channel


def switch(channel: str, target: str, expected: int, feed_seq: int) -> dict:
    with channel_lock(channel):
        current = read_authority(channel)
        if current["generation"] != expected:
            raise BoundaryError("stale authority generation")
        if target == current["authority"]:
            raise BoundaryError("authority already selected")
        if target not in ("legacy", "mishe") or feed_seq < current["active_feed_seq"]:
            raise BoundaryError("invalid target or feed sequence")
        tail = core_feed().tail_sequence()  # verified checkpoint; fail closed on malformed feed
        if feed_seq != tail:
            raise BoundaryError(f"feed sequence must equal current tail {tail}")
        if target == "legacy":
            for item in outbox_dir(channel).glob("*.json"):
                status = read_json(item).get("status")
                if status != "delivered":
                    raise BoundaryError(f"unreconciled sink identity {item.name}")
        record = {"channel": channel, "generation": expected + 1, "authority": target,
                  "active_feed_seq": feed_seq,
                  "installed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
        atomic_json(authority_path(channel), record)
        return record


REQUEST = re.compile(r"wake requested top-pain ([a-z][a-z0-9-]*) for entry ([1-9][0-9]*)\Z")


def sink_status(sink: str, key: str) -> str:
    try:
        result = subprocess.run([sink, "--idempotency-status", key], text=True, capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BoundaryError(f"sink status query unavailable: {type(exc).__name__}") from exc
    if result.returncode not in (0, 3):
        raise BoundaryError("sink status query failed")
    try:
        status = json.loads(result.stdout)["status"]
    except (ValueError, KeyError, TypeError) as exc:
        raise BoundaryError("sink status query malformed") from exc
    if status not in ("delivered", "refused", "unknown"):
        raise BoundaryError("sink status query invalid")
    if (result.returncode == 3) != (status == "unknown"):
        raise BoundaryError("sink status query exit code disagrees with status")
    return status


def synthetic_policy(channel: str) -> tuple[str, str]:
    """Deterministic synthetic admission, optionally using Mesh's live evidence adapter."""
    path = home() / "dispatch-policy" / f"{channel}.json"
    value = read_json(path)
    if (value.get("version") != 1 or value.get("channel") != channel
            or value.get("domain") != "synthetic"
            or type(value.get("private")) is not bool or type(value.get("protected")) is not bool
            or value.get("mind_state") not in ("idle", "busy", "unknown")
            or type(value.get("refractory_until")) is not int or value["refractory_until"] < 0
            or type(value.get("pace_allowed")) is not bool
            or value.get("task_owner") is not None and not isinstance(value["task_owner"], str)):
        raise BoundaryError("synthetic dispatch policy malformed or unavailable")
    if value["private"] or value["protected"]:
        return "refused", "private-or-protected-domain"
    if value.get("evidence_mode") == "live":
        kind = value.get("kind")
        task_id = value.get("task_id")
        if (kind not in ("task", "telemetry", "self-pick")
                or (kind == "task") != (task_id is not None)
                or task_id is not None and not isinstance(task_id, str)):
            raise BoundaryError("invalid live eligibility policy")
        command = os.environ.get("MESH_MISHE_ELIGIBILITY_BIN", str(Path(__file__).with_name("mesh-mishe-eligibility")))
        try:
            probe = subprocess.run([command, channel, kind, *([task_id] if task_id else [])],
                                   text=True, capture_output=True, timeout=45)
            evidence = json.loads(probe.stdout)
        except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
            raise BoundaryError("live eligibility unavailable") from exc
        status = evidence.get("status")
        if (evidence.get("channel") != channel or status not in ("eligible", "held", "refused", "unknown")
                or probe.returncode != {"eligible": 0, "held": 1, "refused": 1, "unknown": 2}[status]
                or not isinstance(evidence.get("reason"), str)):
            raise BoundaryError("live eligibility verdict invalid")
        if status == "unknown":
            raise BoundaryError(f"live eligibility UNKNOWN: {evidence['reason']}")
        return status, evidence["reason"]
    if value.get("evidence_mode", "fixture") != "fixture":
        raise BoundaryError("unknown eligibility evidence mode")
    if value["task_owner"] is not None:
        return "held", "canonical-task-eligibility-unverified"
    if value["mind_state"] == "unknown":
        raise BoundaryError("synthetic mind state UNKNOWN")
    if value["mind_state"] == "busy":
        return "held", "mind-busy"
    if value["refractory_until"] > time.time():
        return "held", "refractory"
    if not value["pace_allowed"]:
        return "held", "pace"
    return "eligible", "synthetic-admitted"


def retry_clock() -> int:
    fixture = os.environ.get("MESH_MISHE_NOW")
    if fixture is not None:
        if not fixture.isdecimal():
            raise BoundaryError("invalid retry clock fixture")
        return int(fixture)
    return int(time.time())


def hold_retry(item: dict, reason: str) -> dict:
    base = os.environ.get("MESH_MISHE_RETRY_BASE", "5")
    if not base.isdecimal() or int(base) > 300:
        raise BoundaryError("invalid retry base")
    attempts = item.get("hold_attempts", 0)
    if type(attempts) is not int or attempts < 0:
        raise BoundaryError("invalid hold attempts")
    attempts += 1
    item["hold_attempts"] = attempts
    item["status"] = "held"
    item["reason"] = reason
    item["next_retry_at"] = retry_clock() + min(300, int(base) * (2 ** min(attempts - 1, 10)))
    return item


def dispatch_once(channel: str, limit: int = 8) -> dict:
    if not 1 <= limit <= 64:
        raise BoundaryError("dispatch limit must be 1..64")
    with channel_lock(channel):
        current = read_authority(channel)
        if current["authority"] != "mishe":
            raise BoundaryError("mishe is not current authority")
        sink = os.environ.get("MESH_MISHE_SINK")
        if not sink or not os.path.isfile(sink) or not os.access(sink, os.X_OK):
            raise BoundaryError("idempotent sink capability absent")
        entries = core_feed().entries(start=current["active_feed_seq"] + 1)
        by_sequence = {entry.sequence: entry for entry in entries}
        results = []
        for entry in entries:
            if len(results) >= limit:
                break
            if entry.sequence <= current["active_feed_seq"] or entry.source != "mishe-tauftauf":
                continue
            if entry.body.startswith(f"wake requested top-pain {channel}") and not REQUEST.fullmatch(entry.body):
                raise BoundaryError(f"malformed request at feed sequence {entry.sequence}")
            match = REQUEST.fullmatch(entry.body)
            if not match or match.group(1) != channel:
                continue
            key = f"{channel}:{current['generation']}:{entry.sequence}"
            path = outbox_dir(channel) / f"{current['generation']}-{entry.sequence}.json"
            item = read_json(path) if path.exists() else {"channel": channel, "generation": current["generation"],
                "request_id": entry.sequence, "key": key, "status": "pending"}
            if (item.get("key") != key or item.get("status") not in
                    ("pending", "held", "claimed", "unknown", "refused", "delivered")):
                raise BoundaryError("outbox record invalid")
            if item["status"] == "held":
                retry_at = item.get("next_retry_at", 0)
                if type(retry_at) is not int or retry_at < 0:
                    raise BoundaryError("invalid retry deadline")
                if retry_at > retry_clock():
                    results.append({"key": key, "status": "held", "reason": item.get("reason"),
                                    "retry_after": retry_at})
                    continue
            stimulus = by_sequence.get(int(match.group(2)))
            if (stimulus is None or stimulus.sequence >= entry.sequence
                    or stimulus.source != "observation/synthetic"):
                if item["status"] not in ("pending", "held"):
                    raise BoundaryError("ungrounded request has an attempted sink identity")
                hold_retry(item, "ungrounded-stimulus")
                atomic_json(path, item)
                results.append({"key": key, "status": "held", "reason": item["reason"],
                                "retry_after": item["next_retry_at"]})
                continue
            if item["status"] == "delivered":
                results.append({"key": key, "status": "delivered"})
                continue
            if item["status"] == "refused":
                results.append({"key": key, "status": "refused"})
                continue
            if item["status"] in ("claimed", "unknown"):
                status = sink_status(sink, key)
                item["status"] = status if status in ("delivered", "refused") else "unknown"
                atomic_json(path, item)
                results.append({"key": key, "status": item["status"]})
                continue
            admission, reason = synthetic_policy(channel)
            if admission != "eligible":
                if admission == "held":
                    hold_retry(item, reason)
                else:
                    item["status"] = admission
                    item["reason"] = reason
                atomic_json(path, item)
                result = {"key": key, "status": admission, "reason": reason}
                if admission == "held":
                    result["retry_after"] = item["next_retry_at"]
                results.append(result)
                continue
            atomic_json(path, item)
            status = sink_status(sink, key)
            if status == "delivered":
                item["status"] = "delivered"
            elif status == "refused":
                item["status"] = "refused"
            else:
                # Lock covers this check and the side effect: a switch cannot race us.
                if read_authority(channel) != current:
                    raise BoundaryError("authority generation changed before sink")
                if os.environ.get("MESH_MISHE_FAULT") == "before-claim":
                    raise BoundaryError("injected crash before claim")
                item["status"] = "claimed"
                atomic_json(path, item)
                if os.environ.get("MESH_MISHE_FAULT") == "after-claim":
                    raise BoundaryError("injected crash after claim")
                try:
                    result = subprocess.run([sink, "--idempotency-key", key, channel,
                                             "Coordinator wake; read your charter and current state."],
                                            text=True, capture_output=True, timeout=15,
                                            env={**os.environ, "MESH_TELL_AUTOMATIC": "0"})
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise BoundaryError(f"sink call ambiguous: {type(exc).__name__}") from exc
                if os.environ.get("MESH_MISHE_FAULT") == "after-tell":
                    raise BoundaryError("injected crash after tell")
                status = sink_status(sink, key)
                item["status"] = status if status in ("delivered", "refused") else "unknown"
                if result.returncode != 0 and item["status"] == "unknown":
                    raise BoundaryError("sink call failed with unknown outcome")
            atomic_json(path, item)
            if os.environ.get("MESH_MISHE_FAULT") == "after-receipt":
                raise BoundaryError("injected crash after receipt")
            results.append({"key": key, "status": item["status"]})
        return {"channel": channel, "generation": current["generation"], "results": results}


def check(channel: str) -> dict:
    """Read-only health verdict for the synthetic fence and outbox."""
    with channel_lock(channel):
        current = read_authority(channel)
        feed = core_feed()
        tail = feed.tail_sequence()
        if current["active_feed_seq"] > tail:
            raise BoundaryError("activation cursor beyond feed tail")
        entries = feed.entries(start=current["active_feed_seq"] + 1)
        counts = {state: 0 for state in ("pending", "held", "refused", "claimed", "unknown", "delivered")}
        for path in outbox_dir(channel).glob("*.json"):
            item = read_json(path)
            state = item.get("status")
            if state not in counts or item.get("channel") != channel:
                raise BoundaryError(f"invalid outbox record {path.name}")
            counts[state] += 1
        missing = 0
        if current["authority"] == "mishe":
            for entry in entries:
                if entry.source == "mishe-tauftauf" and REQUEST.fullmatch(entry.body):
                    match = REQUEST.fullmatch(entry.body)
                    if match.group(1) != channel:
                        continue
                    path = outbox_dir(channel) / f"{current['generation']}-{entry.sequence}.json"
                    if not path.exists():
                        missing += 1
        status = "UNKNOWN" if missing or counts["claimed"] or counts["unknown"] or counts["held"] else "PASS"
        return {"status": status, "channel": channel, "authority": current["authority"],
                "generation": current["generation"], "active_feed_seq": current["active_feed_seq"],
                "feed_tail": tail, "missing_outbox": missing, "outbox": counts}
