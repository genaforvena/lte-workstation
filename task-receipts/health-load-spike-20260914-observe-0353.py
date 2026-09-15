#!/usr/bin/env python3
"""Read-only top-process samples around the next scheduled minute-53 load peak."""

from __future__ import annotations

import datetime as dt
import pathlib
import subprocess
import time


START = dt.datetime(2026, 9, 14, 3, 52, 30, tzinfo=dt.timezone.utc).timestamp()
END = dt.datetime(2026, 9, 14, 4, 1, 30, tzinfo=dt.timezone.utc).timestamp()
OUT = pathlib.Path("/home/mesh-home/lte-workstation/task-receipts/health-load-spike-20260914-observation.md")


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def capture(*args: str) -> str:
    try:
        p = subprocess.run(args, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=5, check=False)
        return p.stdout.strip() or f"(exit {p.returncode}, no output)"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"(probe error: {exc})"


def main() -> None:
    while time.time() < START:
        time.sleep(min(5, max(0.1, START - time.time())))
    rows = ["# Minute-53 load observation — 2026-09-14\n",
            "Read-only `/proc/loadavg` and process-table samples; no process or scheduler intervention.\n"]
    while time.time() <= END:
        ps = capture("ps", "-eo", "pid,ppid,etimes,pcpu,comm,args", "--sort=-pcpu")
        lines = ps.splitlines()
        targets = [line for line in lines if "mesh-random-track-grind" in line or "mesh-usb --urb" in line]
        rows.append(f"## {stamp()}\nloadavg: {capture('cat', '/proc/loadavg')}\n"
                    f"target processes:\n" + ("\n".join(targets) if targets else "(none sampled)") +
                    "\ntop processes:\n" + "\n".join(lines[:16]))
        time.sleep(30)
    OUT.write_text("\n\n".join(rows) + "\n")
    print(f"observation written: {OUT}")


if __name__ == "__main__":
    main()
