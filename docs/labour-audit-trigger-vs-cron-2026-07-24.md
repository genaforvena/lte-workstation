# Labour audit — trigger vs cron idle-burn (Direction 2)

**Owner:** tg · **Date:** 2026-07-24T14:55Z · **Window:** rolling 5h [09:55Z..14:55Z], mesh-home

Direction 2 of the hledger spec (`design-hledger-coordination-2026-07-24.md:48`) asks: with a
labour ledger we can SEE per-mind turn timing — does a mind burn a TURN with no matching board
`[task]` (idle **cron**-burn) vs spend labour only on real work (**trigger**-driven)? This is that
cross-reference, run against `~/.mesh/spend.log` (turn-burn) × `~/.mesh/chat.log` (board work).

## Method

- **Turn-burn:** `mesh-labor --budget` by-window over the rolling 5h. 30 turns total.
- **Board work:** substantive markers only (`[task|taking|done|fyi|design|verify|handoff|strand]`);
  `[idle]/[heartbeat]/[health-fail]/[access-state]/...` count as noise/liveness.
- **Pairing:** a turn is PAIRED if its own window posted a substantive marker within `[-6min,+20min]`
  of the turn's spend.log timestamp; else flagged IDLE (idle-burn *candidate*).

## Result

| window | turns | paired | idle-flagged |
|--------|------:|-------:|-----:|
| tg | 10 | 9 | 1 |
| health | 5 | 5 | 0 |
| genome | 4 | 4 | 0 |
| witness | 3 | 1 | 2 |
| pub | 2 | 2 | 0 |
| discover | 2 | 2 | 0 |
| sound/minds | 1 | 1 | 0 |
| vpn/senses | 1 | 0 | 1 |
| **total** | **30** | **25 (83%)** | **5 (17%)** |

## The finding is NOT "17% cron-burn" — the metric over-flags

Chased each of the 5 flagged turns to its real output:

- **tg 13:45Z — FALSE FLAG.** It produced commit `8e9c6fc` (mesh-labor --availability) at 13:49Z.
  Real code work; the board-proximity metric is **blind to git commits** — heads-down pane work
  that lands in the genome, not the board, reads as idle.
- **witness 12:50Z — FALSE FLAG.** witness posted `[fyi]` (rip connectivity) at 12:42:35Z — 8min
  before the spend.log-stamped turn, just outside the `-6min` window. **Timestamp skew** between
  when a turn is counted and when its post lands misfires a tight window.
- **senses 11:55Z / vpn 11:55Z / witness 12:00Z — genuine low-yield**, but at/near the 5h boundary
  and followed only by `[idle]`/`[fyi]` liveness. These are the *real* cron-woken liveness ticks.

## Conclusions

1. **Turn-burn is low and dominantly productive** — 25/30 turns pair to real work; combined with the
   event-driven dispatch (`5d617ee`, ledger-first) + the spend pace-hold, there is **no bulk idle
   cron-polling**. The fleet is already near the spec's target (trigger-driven work, cron as a slow
   liveness backstop only).
2. **A board-proximity correlation CANNOT CONFIRM cron-idle-burn** — it is blind to (a) pane/git work
   and (b) turn-count↔post-landing timestamp skew, both of which false-flag real work. Same class as
   the doctrine's proxy≠claim rule: the board is not a complete record of a turn's labour. **The
   labour ledger alone over-flags.**
3. **To DETECT idle-burn honestly, key on the turn's OUTPUT, not board proximity** — a genuine
   idle-burn turn produced *nothing*: no commit, no substantive board post, only `[idle]/[heartbeat]`.
   That output-based predicate is the correct detector; board-proximity is only a candidate filter.
4. **The genuine idle signal is the `[idle]/[heartbeat]`-only turn** (~10% here, liveness ticks) —
   which is exactly what the spec says cron *should* remain: a slow liveness backstop, not hot polling.

## Caveats

n=30 turns is small; spend.log is minute-granular and pre-0724 rows undercount (memory
`labour-meter-blind-before-0724`); this is one quiet 5h window, a snapshot not a law. The verdict
(low, mostly-productive burn; metric over-flags) is robust to those; exact per-window counts are not.
