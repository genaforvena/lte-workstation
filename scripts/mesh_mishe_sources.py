"""Node-local inputs for the candidate mishe fleet view (paths, not contents)."""

import os
from pathlib import Path


# name, periodic producer filenames, freshness limit in seconds. Keep these
# values aligned with the pane renderer's MISHE-SEMANTIC contract.
SEMANTIC_SOURCES = {
    "tg": ("tg-path", (".voice-rx-state", ".textin-cycle"), 120),
    "health": ("fleet-health", (".fleet-health.cache",), 600),
    "genome": ("vitality", ("vitality.log",), 10800),
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


def provenance_files(channel: str, mesh_dir: Path, repo: Path) -> tuple[Path, ...]:
    """Return candidate source paths without opening or resolving any of them.

    ``repo`` identifies where the cleaner adapter lives; that executable is
    not itself node-local evidence. The adapter's inputs live under the mesh
    root. The caller separately audits canonical owner tasks for event-driven
    adint, hire, wake and haunt; no file mtime establishes their cadence.
    """
    mesh = Path(os.environ.get("MESH_DIR", str(mesh_dir)))
    if channel == "cleaner":
        return (mesh / "cleaner/latest.json", mesh / "cleaner/settle-latest.json")
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
