#!/usr/bin/env python3
"""Boundedly observe only the wired 2026-09-14 03:23Z doctor cron run."""

from __future__ import annotations

import datetime as dt
import pathlib
import subprocess
import time


ROOT = pathlib.Path("/home/mesh-home/lte-workstation")
LOG = pathlib.Path("/home/mesh-home/.mesh/doctor.log")
LOCK = pathlib.Path("/home/mesh-home/.mesh/.doctor.lock")
CRON = pathlib.Path("/home/mesh-home/.mesh/reflexes.cron")
RECEIPT = ROOT / "task-receipts/health-doctor-next-slot-20260914-observation.md"
PREFLIGHT = dt.datetime(2026, 9, 14, 3, 0, tzinfo=dt.timezone.utc).timestamp()
SLOT = dt.datetime(2026, 9, 14, 3, 23, tzinfo=dt.timezone.utc).timestamp()
DEADLINE = SLOT + 11 * 60


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def run(*args: str) -> str:
    try:
        p = subprocess.run(args, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=5, check=False)
        return p.stdout.strip() or f"(exit {p.returncode}, no output)"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"(probe error: {exc})"


def doctors() -> list[tuple[int, list[str]]]:
    found = []
    for entry in pathlib.Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            argv = (entry / "cmdline").read_bytes().decode(errors="replace").split("\0")
        except OSError:
            continue
        if "--cron" in argv and any("mesh-doctor" in arg for arg in argv):
            found.append((int(entry.name), [arg for arg in argv if arg]))
    return found


def tree(pid: int) -> str:
    try:
        output = subprocess.run(
            ["ps", "-eo", "pid=,ppid=,etimes=,comm=,args="], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5, check=False,
        ).stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"(ps error: {exc})"
    rows = {}
    for line in output.splitlines():
        cols = line.strip().split(None, 4)
        if len(cols) == 5:
            try:
                rows[int(cols[0])] = (int(cols[1]), " ".join(cols[2:]))
            except ValueError:
                pass
    children: dict[int, list[int]] = {}
    for child, (parent, _) in rows.items():
        children.setdefault(parent, []).append(child)
    keep, pending = {pid}, [pid]
    while pending:
        for child in children.get(pending.pop(), []):
            if child not in keep:
                keep.add(child)
                pending.append(child)
    return "\n".join(f"  {proc}: {rows.get(proc, ('?', 'gone'))[1]}"
                     for proc in sorted(keep))


def snapshot(label: str) -> str:
    processes = doctors()
    lock = run("lslocks", "-o", "COMMAND,PID,TYPE,MODE,PATH")
    matching_lock = "\n".join(line for line in lock.splitlines() if ".doctor.lock" in line)
    lines = [f"### {label} {now()}", f"lock-file: {'present' if LOCK.exists() else 'absent'}",
             "lock-holder:\n" + (matching_lock or "(none reported)")]
    if processes:
        for pid, argv in processes:
            lines.append(f"doctor pid={pid} argv={' '.join(argv)}\nprocess-tree:\n{tree(pid)}")
    else:
        lines.append("doctor-process: none")
    try:
        st = LOG.stat()
        lines.append(f"doctor.log mtime={dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat()} size={st.st_size}")
        lines.append("doctor.log tail:\n" + run("tail", "-n", "4", str(LOG)))
    except OSError as exc:
        lines.append(f"doctor.log: {exc}")
    return "\n".join(lines)


def main() -> None:
    while time.time() < PREFLIGHT:
        time.sleep(min(5, max(0.1, PREFLIGHT - time.time())))
    entries = ["# Natural doctor cron observation — 2026-09-14\n",
               "This observer does not invoke, signal, or attach to mesh-doctor.\n",
               snapshot("03:00Z preflight"), "\nWired entry: " + run("grep", "-n", "mesh-doctor --cron", str(CRON))]
    while time.time() < SLOT - 2:
        time.sleep(min(2, max(0.1, SLOT - 2 - time.time())))
    started = False
    while time.time() < min(SLOT + 90, DEADLINE):
        processes = doctors()
        if processes:
            started = True
            entries.append(snapshot("natural invocation sample"))
            break
        time.sleep(1)
    if started:
        while time.time() < DEADLINE:
            entries.append(snapshot("30-second sample"))
            if not doctors():
                break
            time.sleep(30)
        entries.append(snapshot("completion"))
    else:
        entries.append(snapshot("no natural invocation detected by 03:24:30Z"))
    RECEIPT.write_text("\n\n".join(entries) + "\n")
    print(f"observation written: {RECEIPT}")


if __name__ == "__main__":
    main()
