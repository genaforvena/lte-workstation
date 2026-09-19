#!/usr/bin/env python3
"""Exercise the live commit function with a refused board lock."""
from pathlib import Path
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]


class SyncLockTests(unittest.TestCase):
    def test_refused_lock_never_appends_and_retry_preserves_union(self):
        source = (REPO / "scripts/mesh-chat-sync").read_text()
        function = source.split("commit_converged(){", 1)[1].split("\n}\n", 1)[0]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log, candidate = root / "chat.log", root / "candidate"
            original = "2026-09-19T00:00:00Z  fixture  ::  original\n"
            merged = original + "2026-09-19T00:00:01Z  fixture  ::  peer\n"
            log.write_text(original)
            candidate.write_text(merged)
            script = "commit_converged(){" + function + "\n}\n" + '''
LOG="$1"; LOCKF="$2"; cand="$3"
flock(){ return 1; }
if commit_converged "$LOG" "$cand"; then exit 90; fi
test -n "$SHIP_REFUSED" || exit 91
cmp "$LOG" "$4" || exit 92
unset -f flock
commit_converged "$LOG" "$cand" || exit 93
commit_converged "$LOG" "$cand" || exit 94
'''
            snapshot = root / "before"
            snapshot.write_text(original)
            result = subprocess.run(["bash", "-c", script, "test", str(log),
                                     str(root / "lock"), str(candidate), str(snapshot)],
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text(), merged)


if __name__ == "__main__":
    unittest.main()
