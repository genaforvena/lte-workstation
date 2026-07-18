# Spec: SMART / mind-defined wake diff in the reactor (data panes untouched)

**Operator 2026-07-18 (via tg), URGENT.** Owner: genome.
**CORRECTED 2026-07-18** after the first draft (WAKE-SIG emitted by dashes) was REJECTED.

## Hard constraint (operator, emphatic)
> "не меняем топ пейны ради починки миндов! … это НЕ проблема данных (НЕ ТРОГАЙТЕ), а того как
> диспатчить. и критично: не диспатч данных сырых, а призыв прочитать свой пейн."

- **DO NOT touch the top/data panes or any `mesh-dash` role.** The data is sacred and stays byte-for-byte.
- The fix lives ENTIRELY in the **dispatch/reactor** (`mesh-pane-consume`).
- The reactor already sends the mind **no raw data — only an invitation to read its own pane.** Keep that
  exactly; it is correct.

## Problem (unchanged, empirical)
`mesh-pane-consume` wakes a mind only when its top pane's `strip_volatile`'d content changes. But
`strip_volatile` removes only clocks/ages, NOT live numerics (latency `7.75→8.1ms`, byte counters), so
vpn/bruno minds wake on numeric JIGGLE every interval (log: vpn ~2h = its `--interval`, one honest
`droplet held` proves the gate works). The diff is too DUMB — it treats telemetry noise as a change.

## Fix — the diff becomes SMART and/or MIND-DEFINED, all inside the reactor
Two layers, both in `mesh-pane-consume`'s `pane_sig()` / comparison. The pane is captured as today; only
the reactor's INTERNAL copy (never shown to anyone) is filtered before hashing.

1. **SMART-BY-DEFAULT.** Extend the pre-hash normalization to also neutralize telemetry jiggle:
   unit-bearing numerics (`[0-9.]+ ?ms`, `[0-9.]+ ?[KMG]?B(/s)?`, bare floats in a `key=NN.N` telemetry
   position). A latency/byte change alone no longer changes the hash. Keep meaningful discrete changes
   (a verdict word UP↔DOWN, an integer count like `peers=16→15`) — those still wake. This is a smarter
   `strip_volatile`, NOT a change to pane content.

2. **MIND-DEFINED wake-rule (the mind OWNS what wakes it).** Optional per-channel rule file the MIND
   writes and tunes live: `~/.mesh/wake-rule/<channel>` (gitignored, mind-owned, node-local).
   - Format: one `grep -E` pattern per line = the SIGNIFICANT lines this mind watches. When the file
     exists, the reactor keeps ONLY matching lines from its internal capture, then hashes those.
     (A leading `-` on a line = an EXCLUDE pattern: drop matching lines. Include + exclude compose.)
   - No file → the SMART-BY-DEFAULT normalization above applies to the whole pane.
   - The mind changes its own rule at any time (self-tuning): e.g. vpn writes
     `echo 'vpn=|peers=|egress=|DOWN|UP' > ~/.mesh/wake-rule/vpn` so only a real verdict/peer change wakes
     it; latency lines are simply never in the hashed set.
   - The reactor logs which mode it used per wake (`rule` vs `smart-default`) to `pane-consume.log`.

## Gate (RED-first, in `mesh-pane-consume --test`)
- Two frames differing ONLY in a latency value → SAME sig under smart-default → NO wake. (RED against
  today's whole-pane hash.)
- Two frames differing in a verdict word (UP→DOWN) → DIFFERENT sig → WAKE.
- With a `wake-rule` present: a change on a NON-matching line → NO wake; a change on a matching line →
  WAKE. Prove the rule file is actually consulted (drive a temp `MESH_WAKE_RULE_DIR`).
- Keep the existing strip_volatile timestamp-quiet + real-change tests green.

## Scope & order (max fast)
1. `mesh-pane-consume`: smart-default numeric normalization + `~/.mesh/wake-rule/<channel>` support in
   `pane_sig()` + `--test` gate. Deploy to `~/.local/bin`, keep `scripts/` in sync.
2. Verify vpn+bruno stop waking on jiggle via `~/.mesh/pane-consume.log` (they should now hold droplets
   through numeric-only frames). Optionally seed their `wake-rule` files.
3. NO dash changes. NO sensor/producer cron changes. Data panes untouched — verify by diffing a pane
   capture before/after (must be identical).
