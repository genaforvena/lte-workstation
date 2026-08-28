#!/usr/bin/env bash
# mesh-pidfile.sh — THE ONE PREDICATE deciding whether a pid read back from a persisted file is
# still the process that wrote it. Sourced; never wired to cron.
#
#   . "${MESH_PIDFILE_LIB:-$HOME/.local/bin/mesh-pidfile.sh}" 2>/dev/null || \
#     . "$(dirname "$0")/mesh-pidfile.sh" 2>/dev/null || true
#
#   mesh_pidfile_write <file> [pid]   # record pid + its starttime (default: $$)
#   mesh_pidfile_pid   <file>         # the bare pid on stdout (rc 1 if the file holds none)
#   mesh_pidfile_alive <file>         # rc 0 ONLY if the writer itself is still running
#   mesh_pid_starttime <pid>          # /proc/<pid>/stat field 22, rc 1 if the pid is gone
#   mesh_pid_alive     <pid> [start]  # the same verdict from an unfiled pid+starttime pair
#
# WHY THIS FILE EXISTS. `kill -0 "$(cat pidfile)"` asks "is SOME process wearing this number", never
# "is MY process still there", and on this node the difference has an hourly clock: the pid space is
# 4194304 wide and mesh-home hands numbers out fast enough to WRAP IT EVERY 26-60 MINUTES (measured
# 2026-08-28). So a pidfile written an hour ago names a live stranger with better-than-coin odds, and
# seven tools were deciding load-bearing questions on that lottery. The failure DIRECTION differs by
# site and both are bad:
#   - as a LOCK (mesh-snapshot, mesh-pull, mesh-hh-drive) a stale file read as HELD makes the tool
#     silently DECLINE TO RUN — forever, because nothing ever clears a lock nobody holds;
#   - as an ARMED FLAG (mesh-exit's auto-revert timer, mesh-dms's rollback record) a dead timer read
#     as ARMED tells an operator a dead-man's switch is standing guard when nothing is.
# One predicate serves both, because both want the same fact: is the WRITER alive.
#
# THE RECYCLE-PROOF HALF IS /proc/<pid>/stat FIELD 22 (starttime, jiffies since boot). It is not
# unique on its own and it is not meant to be — it is unique WITH the pid, because the kernel cannot
# hand the same number to two processes that started at the same tick. Storing the pair turns
# "someone is wearing this number" into "the one that wrote this is still here".
#
# READING FIELD 22 IS NOT `awk '{print $22}'`. Field 2 is comm, in parentheses, and comm is arbitrary
# bytes — it may contain spaces AND ')' (a kworker's comm is mutable; see
# [[a-kworkers-comm-is-mutable-so-naming-one-is-attribution-not-identity]]). Strip through the LAST
# ") " and count from the remainder, or a process named "foo) bar" shifts every field right.
#
# BACKWARD COMPATIBILITY IS DELIBERATE, NOT AN OVERSIGHT. A file holding a bare pid — written by an
# older build, or by a test fixture — cannot be verified: the starttime it would be compared against
# was never captured and cannot be recovered. Such a file falls through to the plain `kill -0`, i.e.
# EXACTLY the pre-existing behaviour. This library never makes a caller worse than it was; it only
# adds a red where the old predicate was falsely green, and one run of the writer upgrades the file.

# mesh_pid_starttime <pid> — starttime (field 22) on stdout; rc 1 if the pid is gone.
mesh_pid_starttime() {
  local s
  case "${1:-}" in ''|*[!0-9]*) return 1 ;; esac
  s="$(cat "/proc/${1}/stat" 2>/dev/null)" || return 1
  s="${s##*") "}"                          # drop "pid (comm) " — LONGEST match; comm may hold ") "
  s="$(printf '%s\n' "$s" | awk '{print $20}')"   # field 22 overall = 20 in the remainder
  [ -n "$s" ] || return 1
  printf '%s\n' "$s"
}

# mesh_pid_alive <pid> [starttime] — rc 0 if that exact process is running.
# An EMPTY/absent starttime is the unverifiable legacy case and degrades to `kill -0` (see above).
mesh_pid_alive() {
  local pid="${1:-}" want="${2:-}" live
  case "$pid" in ''|*[!0-9]*|0) return 1 ;; esac
  case "$want" in ''|'-') kill -0 "$pid" 2>/dev/null; return $? ;; esac
  live="$(mesh_pid_starttime "$pid")" || return 1
  [ "$live" = "$want" ]
}

# mesh_pidfile_write <file> [pid] — record "<pid> <starttime>". Default pid is $$.
# A pid whose starttime cannot be read (already gone, or not ours) is recorded with '-', which the
# reader treats as the legacy unverifiable case rather than as a lie.
mesh_pidfile_write() {
  local f="${1:?mesh_pidfile_write: file}" pid="${2:-$$}" st
  st="$(mesh_pid_starttime "$pid")" || st='-'
  mkdir -p "$(dirname "$f")" 2>/dev/null || true
  printf '%s %s\n' "$pid" "$st" > "$f"
}

# mesh_pidfile_pid <file> — the bare pid, for callers that must signal or print it.
mesh_pidfile_pid() {
  local pid
  pid="$(awk 'NR==1{print $1}' "${1:-/nonexistent}" 2>/dev/null)" || return 1
  case "$pid" in ''|*[!0-9]*) return 1 ;; esac
  printf '%s\n' "$pid"
}

# mesh_pidfile_alive <file> — THE predicate. rc 0 only if the process that wrote the file is running.
mesh_pidfile_alive() {
  local f="${1:-}" pid st
  [ -s "$f" ] || return 1
  pid="$(awk 'NR==1{print $1}' "$f" 2>/dev/null)"
  st="$(awk 'NR==1{print $2}' "$f" 2>/dev/null)"
  mesh_pid_alive "$pid" "$st"
}

# ── smoke test ────────────────────────────────────────────────────────────────────────────────────
# A SOURCED FILE INHERITS THE CALLER'S POSITIONAL PARAMETERS, so without the BASH_SOURCE guard a
# consumer's own `--test` would run THIS suite and `exit 0` out of the parent's first leg
# ([[a-sourced-library-inherits-the-callers-argv]]). Driven directly only.
if [ "${BASH_SOURCE[0]}" = "$0" ] && [ "${1:-}" = "--test" ]; then
  set -u
  fail=0
  tmp="$(mktemp -d)"
  # THE EXIT TRAP MUST BE PINNED TO THE MAIN SHELL. A backgrounded simple command is a forked bash
  # that INHERITS this trap and has not yet exec'd; the drill kills discarded claimants, so a TERM
  # landing in that window makes the CHILD run `rm -rf "$tmp"` and delete the suite's own fixtures
  # mid-run ([[a-bash-exit-trap-does-run-under-sigterm]]). Measured here: the mutant with the
  # starttime comparison removed passed GREEN in 3 of 5 runs, because the victim pidfile was gone by
  # the time the predicate read it — red for the wrong reason, which is a vacuous gate. $$ stays the
  # main shell's pid inside a fork; $BASHPID does not.
  trap '[ "$BASHPID" = "$$" ] && rm -rf "$tmp"' EXIT

  # (1) live self — must read alive, and the file must carry a real starttime (not the '-' degrade).
  mesh_pidfile_write "$tmp/self.pid" "$$"
  mesh_pidfile_alive "$tmp/self.pid" || { echo "smoke-test: FAIL (own pid not alive)"; fail=1; }
  [ "$(awk '{print $2}' "$tmp/self.pid")" != '-' ] \
    || { echo "smoke-test: FAIL (own starttime unreadable — the pair was never stored)"; fail=1; }

  # (2) legacy bare-pid file must behave EXACTLY as `kill -0` did — no regression on old files.
  printf '%s\n' "$$" > "$tmp/legacy.pid"
  mesh_pidfile_alive "$tmp/legacy.pid" || { echo "smoke-test: FAIL (legacy live pid must stay green)"; fail=1; }
  printf '%s\n' 4194303 > "$tmp/legacydead.pid"
  ! mesh_pidfile_alive "$tmp/legacydead.pid" || { echo "smoke-test: FAIL (legacy dead pid must be red)"; fail=1; }

  # (3) absent / empty / garbage
  ! mesh_pidfile_alive "$tmp/nope.pid" || { echo "smoke-test: FAIL (missing file must be red)"; fail=1; }
  : > "$tmp/empty.pid"
  ! mesh_pidfile_alive "$tmp/empty.pid" || { echo "smoke-test: FAIL (empty file must be red)"; fail=1; }
  printf 'notapid x\n' > "$tmp/junk.pid"
  ! mesh_pidfile_alive "$tmp/junk.pid" || { echo "smoke-test: FAIL (junk must be red)"; fail=1; }

  # (4) comm containing ") " must not shift field 22. Drive it with a real process, not a string.
  cp /bin/sleep "$tmp/we) ird"; "$tmp/we) ird" 30 >/dev/null 2>&1 & _w=$!
  sleep 0.2
  _wst="$(mesh_pid_starttime "$_w" || true)"
  case "$_wst" in ''|*[!0-9]*) echo "smoke-test: FAIL (comm with ') ' broke the field-22 read: '$_wst')"; fail=1 ;; esac
  kill "$_w" 2>/dev/null; wait "$_w" 2>/dev/null || true

  # (5) THE DRILL — a real recycled pid. Write a pidfile, kill the writer, then CLAIM ITS NUMBER with
  # an unrelated live process and assert `kill -0` stays GREEN (the fault reproduces) while
  # mesh_pidfile_alive goes RED (the fix catches it). The claim is made by rewinding
  # /proc/sys/kernel/ns_last_pid and forking immediately — bounded retries, because any other fork on
  # the node can take the number first. NOTE the mode bit lies: ns_last_pid is 0666 and an
  # unprivileged write still fails ([[a-mode-bit-is-not-the-write]]) — attempt it and judge the
  # RESULT, never `[ -w ]`.
  sleep 30 >/dev/null 2>&1 & victim=$!
  mesh_pidfile_write "$tmp/victim.pid" "$victim"
  vst="$(awk '{print $2}' "$tmp/victim.pid")"
  kill "$victim" 2>/dev/null; wait "$victim" 2>/dev/null || true
  claimed=0 tries=0
  while [ "$tries" -lt 300 ]; do
    tries=$((tries + 1))
    sudo -n sh -c "echo $((victim - 1)) > /proc/sys/kernel/ns_last_pid" 2>/dev/null || break
    sleep 60 >/dev/null 2>&1 & c=$!
    if [ "$c" = "$victim" ]; then claimed=1; claimant=$c; break; fi
    # kill-and-DISOWN, never kill-and-wait: `wait` on a discarded claimant was measured hanging the
    # whole suite (1 run in 5), and a bounded loop that can block forever is not a bounded loop. The
    # zombie holds only the number we already rejected, and dies with the shell a moment later.
    kill "$c" 2>/dev/null; disown "$c" 2>/dev/null || true
  done
  if [ "$claimed" = 1 ]; then
    kill -0 "$victim" 2>/dev/null \
      || { echo "smoke-test: FAIL (drill did not reproduce: kill -0 on the reclaimed pid is already red)"; fail=1; }
    ! mesh_pidfile_alive "$tmp/victim.pid" \
      || { echo "smoke-test: FAIL (RECYCLED pid $victim read as ALIVE — the predicate is the lottery it replaced)"; fail=1; }
    [ "$(mesh_pid_starttime "$victim")" != "$vst" ] \
      || { echo "smoke-test: FAIL (claimant shares the victim's starttime — the drill proved nothing)"; fail=1; }
    kill "$claimant" 2>/dev/null; wait "$claimant" 2>/dev/null || true
    echo "smoke-test: drill=LIVE (pid $victim reclaimed after $tries fork(s); kill -0 green, predicate red)"
  else
    # Never render a skipped arm as a pass. Fall back to the same STATE reached by hand — a live pid
    # carrying a starttime that is not its own — and SAY the live claim did not run.
    printf '%s %s\n' "$$" "$(( $(mesh_pid_starttime "$$") + 1 ))" > "$tmp/forged.pid"
    kill -0 "$$" 2>/dev/null || { echo "smoke-test: FAIL (control: own pid must be kill -0 green)"; fail=1; }
    ! mesh_pidfile_alive "$tmp/forged.pid" \
      || { echo "smoke-test: FAIL (live pid + wrong starttime read as ALIVE)"; fail=1; }
    echo "smoke-test: drill=DEGRADED (no ns_last_pid write available — pid reclaim NOT driven live; mismatch arm only)"
  fi

  [ "$fail" = 0 ] && { echo "smoke-test: ok"; exit 0; } || { echo "smoke-test: FAIL"; exit 1; }
fi
