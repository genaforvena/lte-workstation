"""Private producer-byte hashes made during an opted-in S0 projection."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

MAX_SOURCE = 4_000_000
MAX_TOTAL = 16_000_000
EVENT_CHANNELS = frozenset(("adint", "hire", "wake", "haunt"))
TICK = re.compile(r"[0-9a-f]{32}\Z")
EVENT_ID = re.compile(r"[0-9a-f]{64}\Z")


def _signature(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _module_at(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError("provenance module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _hash_file(path: Path, allow_empty: bool) -> tuple[str, int, tuple]:
    before = path.lstat()
    if (not stat.S_ISREG(before.st_mode) or before.st_size > MAX_SOURCE
        or (before.st_size == 0 and not allow_empty)):
        raise ValueError("source unavailable")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or _signature(opened) != _signature(before):
            raise ValueError("source changed")
        digest = hashlib.sha256()
        count = 0
        with os.fdopen(fd, "rb", closefd=False) as stream:
            while chunk := stream.read(min(65536, MAX_SOURCE + 1 - count)):
                count += len(chunk)
                if count > MAX_SOURCE:
                    raise ValueError("source too large")
                digest.update(chunk)
        if count != opened.st_size or _signature(os.fstat(fd)) != _signature(opened):
            raise ValueError("source changed")
        if _signature(path.lstat()) != _signature(opened):
            raise ValueError("source changed")
        return digest.hexdigest(), opened.st_mtime_ns, _signature(opened)
    finally:
        os.close(fd)


def _audit_digest(channel: str, repo: Path) -> str:
    command = os.environ.get("MESH_MISHE_TASK_AUDIT_CMD", str(repo / "scripts/mesh-task"))
    result = subprocess.run([command, "audit"], capture_output=True, timeout=10)
    if result.returncode or len(result.stdout) > 4_000_000:
        raise ValueError("audit unavailable")
    text = result.stdout.decode("utf-8")
    overdue = re.compile(
        rf"OVERDUE\t{re.escape(channel)}\t[A-Za-z0-9._/-]{{1,120}}\t"
        r"lease=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ(?: independent_reason=[^\n]{1,160})?\Z"
    )
    rows = [row for row in text.splitlines() if overdue.fullmatch(row)]
    if not rows:
        raise ValueError("no exact-owner overdue row")
    return hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()


def source_stamp(channel: str, event_id: str, tick: str, home: Path,
                 repo: Path, projection: str) -> dict | None:
    """Return a private S0 stamp, or no stamp if evidence is unavailable.

    No source content or path is returned to the projector's public output.
    The stamp must be bound to a committed feed sequence before use.
    """
    home, repo = Path(home), Path(repo)
    sentinel = home / ".fleet-corpus-capture"
    try:
        if (not TICK.fullmatch(tick) or not EVENT_ID.fullmatch(event_id)
            or not stat.S_ISREG(sentinel.lstat().st_mode)):
            return None
        core = Path(os.environ.get("MESH_MISHE_CORE", str(Path.home() / "mishe-tauftauf")))
        view = _module_at("mishe_tauftauf.external_view", core / "src/mishe_tauftauf/external_view.py")
        safe = view.safe_fleet_view(projection, channel)
        if safe is None:
            return None
        audit = None
        if channel in EVENT_CHANNELS:
            if (not safe.startswith("STATE: RED\n")
                or "semantic=obligations:stale" not in safe.splitlines()[1].split()):
                return None
            audit = _audit_digest(channel, repo)
        registry = _module_at("mesh_mishe_sources", Path(__file__).with_name("mesh_mishe_sources.py"))
        mesh = Path(os.environ.get("MESH_DIR", str(home.parent)))
        paths = tuple(registry.provenance_files(channel, mesh, repo))
        if not paths or len(paths) > 32 or len(set(paths)) != len(paths):
            return None
        records = []
        signatures = []
        total = 0
        for path in paths:
            digest, mtime, signature = _hash_file(path, registry.allows_empty_marker(channel, path))
            total += signature[3]
            if total > MAX_TOTAL:
                return None
            records.append({"origin": str(path), "sha256": digest, "mtime_ns": mtime})
            signatures.append(signature)
        if any(_signature(path.lstat()) != signature
               for path, signature in zip(paths, signatures, strict=True)):
            return None
        return {"version": 1, "tick": tick, "event_id": event_id, "channel": channel,
                "projected_sha256": hashlib.sha256(projection.encode("utf-8")).hexdigest(),
                "sources": records, "audit_sha256": audit}
    except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired, ImportError):
        return None


def stage_source_stamp(home: Path, stamp: dict) -> None:
    """Atomically stage one private stamp without touching legacy event staging."""
    home = Path(home)
    if not TICK.fullmatch(stamp["tick"]) or not stat.S_ISREG(
            (home / ".fleet-corpus-capture").lstat().st_mode):
        return
    directory = home / "parity" / "source-staged"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    directory_info = directory.lstat()
    if (not stat.S_ISDIR(directory_info.st_mode)
        or directory_info.st_uid != os.getuid()
        or directory_info.st_mode & 0o077):
        raise ValueError("private source staging unavailable")
    target = directory / stamp["channel"]
    fd, temporary = tempfile.mkstemp(prefix=f'.{stamp["channel"]}.', dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(stamp, stream, separators=(",", ":"))
            stream.write("\n")
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
