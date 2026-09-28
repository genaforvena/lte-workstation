"""Node-local inputs for the candidate mishe fleet view (paths, not contents)."""

import os
from pathlib import Path
import re
import stat
import sys
from datetime import datetime


# name, periodic producer filenames, freshness limit in seconds. Keep these
# values aligned with the pane renderer's MISHE-SEMANTIC contract.
SEMANTIC_SOURCES = {
    "tg": ("tg-path", (".voice-rx-state", ".textin-cycle"), 120),
    "health": ("fleet-health", (".fleet-health.cache",), 600),
    "genome": ("vitality", (".vitality-state",), 10800),
    "senses": ("sense-map", ("sense-map.txt",), 1800),
    "minds": ("mind-wall", (".mind-state-watch.cache",), 300),
    "sound": ("archivist", (".records-tick",), 300),
    "vpn": ("vpn-probe", ("vpn-health.log",), 1800),
    "discover": ("field-study", ("study.log",), 43200),
    "job": ("job-liability", ("job-act.log",), 10800),
    "adint": ("obligations", (), 0),
    "hire": ("obligations", (), 0),
    "wake": ("obligations", (), 0),
    "haunt": ("obligations", (), 0),
    "tg-roz": ("roz-intake", (), 0),
}


def parse_vitality_state(raw: bytes) -> dict[str, str] | None:
    """Accept only the bounded verdict written by mesh-vitality."""
    if not raw or len(raw) > 4096 or not raw.endswith(b"\n"):
        return None
    try:
        lines = raw.decode("ascii").splitlines()
        pairs = [line.split("=", 1) for line in lines]
        if (len(pairs) != 6 or any(len(pair) != 2 for pair in pairs)
            or [pair[0] for pair in pairs] !=
                ["fails", "verdict", "tools", "beta", "autonomy", "ts"]):
            return None
        state = dict(pairs)
        if (not re.fullmatch(r"\d{1,12}", state["fails"])
            or state["verdict"] not in ("OK", "LOW")
            or not re.fullmatch(r"\d{1,12}", state["tools"])
            or not re.fullmatch(r"(?:\d{1,4}(?:\.\d{1,6})?|n/a)", state["beta"])
            or not re.fullmatch(r"(?:\d{1,4}(?:\.\d{1,6})?|n/a)", state["autonomy"])
            or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", state["ts"])):
            return None
        datetime.fromisoformat(state["ts"].replace("Z", "+00:00"))
        return state
    except (UnicodeError, ValueError):
        return None


def read_vitality_state(path: Path) -> dict[str, str] | None:
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= 4096:
            return None
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino,
                opened.st_size, opened.st_mtime_ns) != (before.st_dev, before.st_ino,
                before.st_size, before.st_mtime_ns):
                return None
            raw = os.read(fd, 4097)
            if len(raw) != opened.st_size or os.fstat(fd).st_mtime_ns != opened.st_mtime_ns:
                return None
            return parse_vitality_state(raw)
        finally:
            os.close(fd)
    except OSError:
        return None


def allows_empty_marker(channel: str, path: Path) -> bool:
    """The archivist's successful-tick source is deliberately mtime-only."""
    return channel == "sound" and path.name == ".records-tick"


def provenance_files(channel: str, mesh_dir: Path, repo: Path) -> tuple[Path, ...]:
    """Return candidate source paths without opening or resolving any of them.

    ``repo`` identifies where the cleaner adapter lives; that executable is
    not itself node-local evidence. The adapter's inputs live under the mesh
    root. The caller separately audits canonical owner tasks for event-driven
    adint, hire, wake and haunt; no file mtime establishes their cadence.
    """
    mesh = Path(os.environ.get("MESH_DIR", str(mesh_dir)))
    if channel == "cleaner":
        latest = mesh / "cleaner/latest.json"
        if latest.is_symlink():
            target = os.readlink(latest)
            if not re.fullmatch(r"scan-\d{14}\.json", target):
                raise ValueError("cleaner scan link leaves its owned root")
            latest = latest.parent / target
        return (latest, mesh / "cleaner/settle-latest.json")
    if channel == "pub":
        return (Path(os.environ.get("MESH_MISHE_PUB_CACHE",
                                    str(Path.home() / ".mesh/.pub-right.cache"))),)

    goal_dir = Path(os.environ.get("MESH_MISHE_GOAL_DIR", str(mesh)))
    goal = goal_dir / f".goal-{channel}.cache"
    if channel in ("adint", "hire", "wake", "haunt"):
        # Their goal cache is a pane input, not proof of a business run:
        # canonical owner obligations are classified separately via mesh-task audit.
        return (goal,)
    if channel == "witness":
        journal = Path(os.environ.get("MESH_TASK_JOURNAL", str(mesh / "tasks.journal")))
        return (journal,)

    directory = Path(os.environ.get("MESH_MISHE_SEMANTIC_DIR", str(mesh)))
    if channel == "tg-roz":
        return (goal, directory / "tg-strangers.log", directory / ".roz-channel.offset")
    if channel == "minds":
        restore = Path(os.environ.get("MESH_MISHE_RESTORE_ENV",
                                      str(Path.home() / ".mesh/restore.env")))
        return (goal, directory / ".mind-state-watch.cache", restore)
    if channel in SEMANTIC_SOURCES:
        return (goal, *(directory / filename for filename in SEMANTIC_SOURCES[channel][1]))
    raise ValueError(f"channel not enrolled: {channel}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--vitality-summary":
        raise SystemExit(2)
    value = read_vitality_state(Path(sys.argv[2]))
    if value is None:
        print("UNKNOWN")
    else:
        print(f"{value['verdict']} fails={value['fails']} tools={value['tools']} "
              f"beta={value['beta']} autonomy={value['autonomy']} at={value['ts']}")
