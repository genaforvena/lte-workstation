"""Single-writer guard for the shared HH browser daemon."""

from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import signal
import sys
import time


def _holder(fd):
    try:
        return os.pread(fd, 200, 0).decode("utf-8", "replace").strip() or "(нет записи)"
    except OSError:
        return "(не прочиталось)"


def install_hh_lock_signal_handlers():
    """Make TERM/HUP unwind a lock-owning context instead of skipping finally blocks."""
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, lambda signum, _frame: sys.exit(128 + signum))


@contextmanager
def hh_driver_lock(path, wait=0.0, mode="job"):
    """Yield (acquired, reason), holding the lock for the context lifetime."""
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o644)
    except OSError as exc:
        yield False, "не удалось открыть замок %s: %s" % (path, exc)
        return
    start = time.monotonic()
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                if time.monotonic() - start >= wait:
                    yield False, "замок %s занят — держит: %s" % (path, _holder(fd))
                    return
                time.sleep(min(0.25, wait - (time.monotonic() - start)))
                continue
            os.ftruncate(fd, 0)
            os.write(fd, ("pid=%d mode=%s since=%s\n" % (
                os.getpid(), mode,
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))).encode())
            os.fsync(fd)
            yield True, ""
            return
    finally:
        # chatwatch uses this shared marker as its cheap cross-process stand-down signal.
        # A reply process has released the flock at this point but must not leave a fresh
        # mtime that makes chatwatch stand down for another 15 minutes.
        if mode in ("reply", "confirm") and path.name == ".apply.lock":
            old = time.time() - 901
            try:
                os.utime(path, (old, old))
            except OSError:
                pass
        os.close(fd)
