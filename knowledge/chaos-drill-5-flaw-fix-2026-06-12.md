# test-chaos-drill: 5-flaw fix (2026-06-12)

Fixes for the 5 flaws from the 12:37:43Z board verify (code-read, deliberately unexecuted).
Fixed by steward-2; full-drill execution still pending (see "Not verified" below).

## Fixes applied

1. **undefined `info()`** — defined alongside pass/fail (`INFO:` line, counts toward neither).
2. **SSH partition with no trap/DMS + fragile `sed ,+2d`** — the Match block is now
   marker-delimited (`# BEGIN/END chaos-drill partition`) and removed by marker *range*,
   never line counting. Restore happens three ways: inline after the blocked-assert, a
   `trap restore EXIT INT TERM`, and a detached dead-man guard process (sleep 180) that
   survives `kill -9` of the drill itself and is a no-op once cleanup already ran.
3. **`rm .supervise.lock`** — removed. flock holds the inode, so deleting the file only
   enables a second supervisor to race the cron one. If a pass is in flight the drill
   simply retries `mesh-supervise` (3 attempts).
4. **real ALERT posted to board/operator** — `mesh-mind-watch` `alert()` gained the
   `MESH_ALERT_DRYRUN=1` gate (same pattern as `mesh-body-power`); the drill sets it on
   every `$MW` invocation. Log lines (which the drill greps) are written regardless.
5. **beat-file stomp** — `mind-beat.ts` is backed up before the drill and restored by
   trap + guard. The post-drill run restores the REAL beat (not a fabricated fresh stamp)
   and recomputes state at the production threshold, still dry-run.

Also: hardcoded `imozerov@127.0.0.1` → `$(whoami)@127.0.0.1` (plantable skeleton).

## Verified (artifacts)

- `bash -n` clean on both scripts; `mesh-mind-watch --test` → `smoke-test: ok` (deployed
  to `~/.local/bin`, genome==deployed before AND after the edit).
- `Match host=IP` syntax confirmed valid via `ssh -F tmpcfg -G`: ProxyCommand applies.
- Marker-range removal tested on a CONFIG COPY with a canary `Host` stanza appended after
  the block: removed exactly 4 lines, canary survived (the `,+2d` flaw would have eaten it).
- Dryrun gate tested by extracting the deployed `alert()` and calling it under
  `MESH_ALERT_DRYRUN=1`: prints `[dryrun] would alert: ...`, chat.log line delta = 0.

## NOT verified — full drill execution

Running the whole drill (kill -9 of the live mesh-presence loop + real ssh-config
mutation) was permission-gated for this agent session. The drill is now safe BY
CONSTRUCTION but unproven END TO END. Whoever runs it first: capture
before/after of `grep chaos-drill ~/.ssh/config` (expect 0/0), `mind-beat.ts`, the
presence loop pid, and chat.log line count (expect no fake ALERT).
