#!/usr/bin/env python3
"""Durable at-most-once claim for keyed mesh-tell sends.

A crash after begin is UNKNOWN. The caller must reconcile it; retrying the same
identity would risk a second tmux injection.
"""

import fcntl
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
from pathlib import Path


KEY = re.compile(r"^[A-Za-z0-9_-]+:[1-9][0-9]*:[A-Za-z0-9_.-]{1,128}$")


def atomic(path: Path, data: dict) -> None:
    fd, name = tempfile.mkstemp(prefix=".receipt-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in {"begin", "finish", "status"} or not KEY.fullmatch(argv[2]):
        print("usage: mesh_tell_receipt.py begin|finish|status channel:generation:request-id ...", file=sys.stderr)
        return 2
    op, key = argv[1:3]
    if len(argv) != {"begin": 5, "finish": 5, "status": 3}[op]:
        return 2
    root = Path(os.environ.get("MESH_TELL_RECEIPT_DIR", str(Path.home() / ".mesh/tell-receipts")))
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if root.is_symlink() or root.stat().st_mode & 0o077:
        print("mesh-tell receipt directory is insecure", file=sys.stderr)
        return 2
    path = root / (hashlib.sha256(key.encode()).hexdigest() + ".json")
    with (root / ".lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            record = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        except (OSError, ValueError):
            print("mesh-tell receipt is unreadable", file=sys.stderr)
            return 2
        if record is not None and record.get("key") != key:
            return 2
        if op == "status":
            if record is None:
                print(json.dumps({"status": "unknown", "reason": "missing"}))
                return 3
            status = record.get("status")
            if status not in {"pending", "delivered", "refused", "unknown"}:
                return 2
            print(json.dumps({"status": "unknown" if status == "pending" else status}))
            return 0 if status in {"delivered", "refused"} else 3
        if op == "begin":
            channel, digest = argv[3:5]
            if key.split(":", 1)[0] != channel or not re.fullmatch(r"[a-f0-9]{64}", digest):
                return 2
            if record is not None:
                return 2 if (record.get("channel"), record.get("digest")) != (channel, digest) else 3
            token = secrets.token_hex(24)
            atomic(path, {"key": key, "channel": channel, "digest": digest, "token": token, "status": "pending"})
            print(token)
            return 0
        token, status = argv[3:5]
        if record is None or token != record.get("token") or status not in {"delivered", "refused", "unknown"}:
            return 2
        if record.get("status") not in {"pending", status}:
            return 2
        record["status"] = status
        atomic(path, record)
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
