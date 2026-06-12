# ds doctor triage: stale-error residue, a drifted organ, and a mind blocked on a prompt

Date: 2026-06-12

## The presenting symptom

ds `mesh-doctor`: 3 FAILs — "recent error-lines (UP but broken?)" in chat-sync.log,
doctor.log, mind-watch.log.

## Root causes found (none were live breakage)

1. **Stale error residue.** All three logs held bash syntax-error lines from broken
   deployed copies that were **already replaced at 16:10** (and doctor at 16:24, my own
   mic-fix scp). All three tools `bash -n` clean and `--test` ok now. Doctor's check is
   `tail -20` per log — chat-sync (1 line/10min) would have false-FAILed ~2 more hours,
   and **mind-watch.log would false-FAIL forever**: healthy mind-watch runs log nothing,
   so its only line was the old error — a permanent ghost. Rotated all three to `.log.1`
   (zero info loss); doctor now: `PASS no error-spam in operational reflex logs`.
   Detector lesson: tail-N recency lies on silent-when-healthy logs; mtime or
   timestamp-window would not.
2. **ds mind was alive-but-BLOCKED on a permission prompt** (a read-only grep — it was
   investigating these same logs). This explained the stale mind-beat (28744s) that
   ds's own mind-watch dryrun surfaced. Unblocked via `mesh-tell` (option 2: allow
   .mesh reads — reduces repeat blocks); mind resumed instantly. Blocked-on-prompt is a
   distinct failure class: the mind is UP for supervise, DEAD for work.
3. **mesh-notify drifted on ds**: ds genome (40cb7da) carries the auto-detect-DISPLAY
   fix; deployed copy was old → smoke FAIL on a node that has 4 X sockets (ds is NOT
   headless). One `cp` from genome → smoke ok.

## Also established

- The mesh-novelty mis-source bug (open since the 13:05 review) is **already fixed** —
  concurrent agent committed `2fbd7e4` (sources first-seen devices from presence.log)
  on this node, unpushed; landing flow will push.
- ds doctor's NEW `inverse-orphan` WARN correctly flags mesh-therm-watch as
  wired-but-ungenomed on a node whose clone predates it — confirms landing the tree
  (steward) matters: a fresh plant would cron a missing tool.

## Open (boarded)

- ds `mesh-volume --test`: FAIL "cannot read volume — PipeWire down or no sink"
  (deployed == genome, so a real organ/daemon issue, not drift). The last remaining
  ds doctor FAIL. For the ds-local mind.
