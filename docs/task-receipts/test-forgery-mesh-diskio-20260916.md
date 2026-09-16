# test-forgery/mesh-diskio — verified CLEAN, no change (2026-09-16)

Task: test-forgery/mesh-diskio-test-writes-the-liveness-log-it-checks (owner=genome)
Source accusation: chat.log:69462 (root/mesh-test-forgery@phaedra) — `--test` growing `/root/.mesh/autowire.log`, `/root/.mesh/pane-reload.log`.

## Live re-run (this node, attribution ON)
- `scripts/mesh-test-forgery --tool mesh-diskio` (196s, rc=0): 1 forged —
  `forgery mesh-diskio /home/mesh-home/.mesh/pane-consume.log na` (writer unattributed).
- NOTE: the phaedra-accused logs (autowire.log, pane-reload.log) did NOT reproduce here;
  the local verdict names a different log with `na` identity — already a weaker claim than phaedra's.

## Why the verdict is a false positive (four independent legs)
1. **Source audit**: `scripts/mesh-diskio --test` (lines 177–330) runs every live drive under
   `mktemp -d` HOME (`_tl`, `_tw`, `_tf`); the only real-HOME execution is the exit-2 arm's
   default-action probe, which touches `.diskio-state` (tool's own state carry, not a `*.log`,
   invisible to the sweep's snapshot glob). No `pane-consume` reference anywhere in the tool.
2. **Cross-tool history**: the same log drew FORGERY rows for three unrelated tools —
   mesh-battery-energy (09-09), mesh-phone-watch (09-11), mesh-tailnet-policy (09-12), all
   writer=none/na. A log "forged" by four unrelated tools is forged by none of them.
3. **Content audit**: 57 pane-consume.log lines inside my sweep window (13:19:16–13:22:32Z),
   all mesh-pane-consume driver wake traffic (`senses: change detected — waking`,
   `--help: WOKE mind …`), **zero lines mention mesh-diskio** (`grep -c` = 0).
4. **Mechanism**: observer effect — running the sweep from this live mind pane generated
   pane wakes (13:19:20–25Z, exactly at sweep start); the confirm leg caught that burst
   while the shorter control window sat in a quiet gap. Coincidence, not causation —
   the same shape the sweep's own header warns about for busy logs.

## Decision
No change to mesh-diskio. The --test path is fully sandboxed and the accusation does not
survive contact with content evidence. Detector gap noted, not fixed here: the sweep's
control arm cannot veto a bursty self-driver log when the observer's own pane activity
supplies the burst — that calibration belongs to the sweep owner, and a by-name exemption
would blind the detector for all tools, so it is deliberately NOT smuggled into this row.

## Retry edge
Re-run `mesh-test-forgery --tool mesh-diskio` after any change to the --test path
(especially new live drives or state writes); a future `self:`-attributed row re-opens this.

## Delegation
- None — single tightly-coupled verify-and-decide pass; exemption: evidence fits one local run.
- Personally inspected: full --test source (177–330), live sweep output, forgery tape rows,
  pane-consume.log window content, cross-tool FORGERY history.
