#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
python3 - "$repo" <<'PY'
import os, subprocess, sys, tempfile, time
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "job"))
import mesh_job_hh_lock

lock = Path(tempfile.mkdtemp()) / ".apply.lock"
holder = subprocess.Popen([
    sys.executable, "-c",
    "import sys,time\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "from mesh_job_hh_lock import hh_driver_lock\n"
    "with hh_driver_lock(sys.argv[2], wait=0.5) as (ok, why):\n"
    " print('held' if ok else 'not-held', flush=True)\n"
    " time.sleep(2)\n",
    str(repo / "job"), str(lock),
], stdout=subprocess.PIPE, text=True)
assert holder.stdout.readline().strip() == "held"
with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05) as (ok, why):
    assert not ok, "a second HH writer entered while the first held the lock"
    assert "держит" in why
holder.wait(timeout=5)
with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05, mode="reply") as (ok, why):
    assert ok
assert time.time() - lock.stat().st_mtime > 900, "released reply marker still looks busy to chatwatch"
with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05, mode="confirm") as (ok, why):
    assert ok

# A live holder is authoritative even when its marker's mtime is old.  The old
# chatwatch mtime heuristic allowed this TOCTOU: it began reading while apply
# still owned the browser, then queued navigation into the application flow.
import importlib.machinery, importlib.util
chatwatch_path = repo / "job" / "mesh-job-chatwatch"
loader = importlib.machinery.SourceFileLoader("mesh_job_chatwatch", str(chatwatch_path))
spec = importlib.util.spec_from_loader(loader.name, loader)
chatwatch = importlib.util.module_from_spec(spec)
loader.exec_module(chatwatch)
chatwatch.LOCK = lock
with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05, mode="apply") as (ok, why):
    assert ok
    old = time.time() - chatwatch.LOCK_AGE - 60
    os.utime(lock, (old, old))
    assert chatwatch.busy_writer(), "chatwatch entered despite a live flock holder"
# A completed apply leaves a fresh marker.  The flock, not that historical mtime,
# decides ownership; otherwise every successful batch silences the watcher for 15m.
os.utime(lock, None)
assert not chatwatch.busy_writer(), "chatwatch treated a released fresh marker as a live writer"
chatwatch.LOCK = chatwatch.JOB / ".apply.lock"
assert not chatwatch.busy_writer(), "released confirm marker must not look busy to chatwatch"

try:
    with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05, mode="confirm") as (ok, why):
        assert ok
        raise OSError("body failure must escape the lock context unchanged")
except OSError as exc:
    assert str(exc) == "body failure must escape the lock context unchanged"

term = subprocess.Popen([
    sys.executable, "-c",
    "import os,signal,sys,time\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "from mesh_job_hh_lock import hh_driver_lock, install_hh_lock_signal_handlers\n"
    "install_hh_lock_signal_handlers()\n"
    "with hh_driver_lock(sys.argv[2], wait=0, mode='reply') as (ok, why):\n"
    " print('term-held' if ok else 'term-not-held', flush=True)\n"
    " time.sleep(30)\n",
    str(repo / "job"), str(lock),
], stdout=subprocess.PIPE, text=True)
assert term.stdout.readline().strip() == "term-held"
term.terminate()
term.wait(timeout=5)
with mesh_job_hh_lock.hh_driver_lock(lock, wait=0.05) as (ok, why):
    assert ok, "SIGTERM left the HH lock held"
print("job HH serialization: PASS")
PY
