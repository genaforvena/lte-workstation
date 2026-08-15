# Scheduled appearance "wifi Keenetic-8813 @ 14:53 UTC" — DISCARDED (already), and why it was asked a THIRD time

**Date:** 2026-08-15 · **Window:** genome · **Tool:** `scripts/mesh-rhythm` · **Tapes:** `~/.mesh/wifi.log`, `~/.mesh/rhythm.log`

## The claim

> SCHEDULED APPEARANCE (auto, real data): wifi Keenetic-8813 tends to appear around 14:53 UTC
> (±1.6h, 5 appearances over 72h, clustered beyond scan cadence, sampling-corrected Rayleigh
> p=0.025 Bonferroni-corrected over 2 devices)

## The one-line answer

**Spurious — nothing recurs at 14:53.** Keenetic-8813 is a neighbour AP in the air on the large
majority of scans (the prior review measured 1828/2296 ≈ 80 % over 31 days; `wifiscan.log` is a live
append-only tape, so that ratio is its answer on that day, not a constant); it does not arrive and
leave, it crosses the detection threshold when its signal is weak, so
the "arrivals" are RF-marginality episodes, not a routine. Mechanism, measurements and the two
guards that now reject it: `scheduled-appearance-keenetic-8813-flicker-opportunity-null-2026-08-15.md`
(landed in `f52a50c`). This review is about the *second* defect — the one that made the mesh pay for
the same question three times.

## The finding is already dead at source — verified on live data

The two guards landed at 12:33Z are in both the genome and the deployed copy, and they work. Ablation
against the **live** tape, not a fixture:

| run | `mesh-rhythm --dry` on live data |
|---|---|
| all guards on (genome **and** deployed) | honest empty |
| `RHYTHM_SKIP_OPP_NULL=1` | Keenetic-8813 @ 14:55, p=0.0105 |
| `RHYTHM_SKIP_BLINDGAP_GUARD=1` | honest empty |
| both off (the pre-fix tool) | Keenetic-8813 @ 14:55, p=0.019, "over 2 devices" |

Two things this pins down that the fixture could not. The **opportunity-set null** is the guard that
actually kills this device — the blind-gap guard is aimed at the other shape and is not load-bearing
here, so "the fix works" was, before this, a claim about the wrong half. And the signature of the
both-off row (2 devices, ~14:55) is the signature of the queued claim, which dates it: **the idea was
minted by the pre-fix tool.**

## The real defect: the recent-emitted cache was owned by a different tool

`rhythm.log` shows the same key emitted twice, an hour apart:

```
2026-08-15T11:33:01Z mesh-rhythm: +1 finding -> ideas-queue (rhythm:wifi Keenetic-8813)
2026-08-15T12:33:01Z mesh-rhythm: +1 finding -> ideas-queue (rhythm:wifi Keenetic-8813)
```

`recent_has` exists precisely to stop that. It could not:

- `scripts/mesh-rhythm:96` → `STATE="$MESH/.rhythm-state"` (recent-emitted keys, written hourly)
- `scripts/mesh-rhythm-state:61` → `STATE="$HOME/.mesh/.rhythm-state"` (work-rhythm label)
- `scripts/mesh-rhythm-state:310` → `printf '%s|%s\n' … > "$STATE"` — a **full overwrite**, on
  `# reflex-cadence: 2-59/5 * * * *`

Two different tools, one path, one of them truncating it every five minutes. The live file holds
`DEGRADED|missing: body-motion (…)` — not one rhythm key has ever survived in it. An hourly tool
whose suppression cache is wiped every 5 minutes has a **dead gate, not a leaky one**.

Note the failure has no symptom of its own. Both writes succeed, neither errors, the file is always
present, always fresh, always well-formed — it simply never holds what this tool put there. And the
degraded behaviour of a *suppression* cache is silent by construction: **"nothing was suppressed" and
"there was nothing to suppress" print the same line** (`no fresh finding (none meet thresholds, or
all recently emitted)` — the message even enumerates both branches without distinguishing them). The
only visible trace was the mesh being asked the same dead question three times, and that trace
surfaces as *a paid mind turn*, which is the expensive place to discover it.

**A name is not an owner.** `.rhythm-state` reads as `mesh-rhythm`'s file by every naming convention
in the tree; it belongs to `mesh-rhythm-state`. The two tools are unrelated (one hunts schedules in
device tapes, the other labels the operator's work rhythm) and neither knows the other exists.

## Why the suite stayed green

The suite ran the tool a second time — but only after `printf '[ ] something open\n' > ideas-queue`,
so the **floor gate** answered first and returned "hold". The recent-key gate was never on the path
under test. A cache that matched nothing, ever, passed green. Same shape as the opportunity-set hole
this device already exposed once: a diagnosis with two halves where only one half got a guard.

## Fix (genome, uncommitted — steward lands)

`scripts/mesh-rhythm`:

1. **Own the path** — `STATE="$MESH/.rhythm-emitted.state"`. `.rhythm-state` is left alone; it is
   mesh-rhythm-state's. One-time effect: the cache starts empty, so at most one finding may repeat
   once (and for Keenetic it cannot — the guards reject it outright).
2. **`state_is_ours`** — every key this tool writes is `rhythm:<label>`, so a non-blank line that
   does not match is a foreign writer. Report it **loudly** (`FOREIGN-STATE …` naming the offending
   line) and fail toward **re-emitting**, never toward a silent hold; `recent_add` resets the cache
   rather than appending our keys under someone else's content. A collision arriving again under a
   new tool's name now announces itself instead of degrading to a repeat.
3. **`mesh-state-touch --create`** at the two liveness call sites — on the own path the file
   legitimately does not exist until the first emission, and the touch skips a missing file. An
   empty recent-emitted cache is an honest state ("nothing emitted yet"), not a fabricated reading.

Latent, not live, and stated as such: the old touch was aimed at a file another tool refreshes every
5 minutes. `.rhythm-emitted.state` is **not** in `mesh-reflex-health`'s `REFLEXES` table (checked), so
nothing currently misreads it — but had anyone added `.rhythm-state` there for `mesh-rhythm`, they
would have been watching mesh-rhythm-state's heartbeat and reading a dead mesh-rhythm as LIVE.

## Artifact — every new gate seen RED before green

`--test` green with all guards. Three mutants, run from a scratch copy, each red for its own reason:

| mutant | result |
|---|---|
| `recent_has` always false | `FAIL(GREEN): already-emitted key re-emitted on a CLEAR queue — suppression dead` |
| `state_is_ours` always true | `FAIL: foreign content … went unreported (silent, the whole bug)` + foreign line survived |
| `recent_add` reset removed | `FAIL: the foreign line survived into our cache` |

The suppression test carries its own RED half in-suite (`RHYTHM_SKIP_RECENT=1` must re-emit), so the
green assertion cannot be vacuous, and it runs on a **clear** queue so the floor gate cannot answer
for it.

## Loose end, not touched

The previous review flagged that `~/.mesh/wifiscan.log` holds far more `=== mesh-wifiscan` headers
than a `^===`-anchored parser can see. Chasing it this pass named the **mechanism**, which the
symptom alone did not: the file has **no writer in the genome at all** (`grep -rn 'wifiscan.log'
scripts/` → 0 hits). `mesh-wifiscan` writes `wifi.log`; `wifiscan.log` is a **cron stdout capture** —
`reflexes.cron:154`, `mesh-wifiscan --log >> $HOME/.mesh/wifiscan.log 2>&1`. The producer's output
does not end in a newline, so each run's header concatenates onto the previous run's last line. That
also means there is no pruner and no owner: nobody is responsible for its shape.

Still not fixed and still harmless *today* — it has no reader but the shell that appends to it. Any
future parser anchored `^===` would silently see a small fraction of the tape. Re-derive, never quote:

```sh
grep -o '=== mesh-wifiscan' ~/.mesh/wifiscan.log | wc -l   # all headers
grep -c '^=== mesh-wifiscan' ~/.mesh/wifiscan.log          # headers a ^-anchored parser would see
```

2406 vs 107 at 2026-08-15T13:05Z. The previous review reported 2401 vs 109 hours earlier; with an
append-only file and no pruner an anchored count should not fall, so one of the two measurements used
a slightly different pattern. Not chased — it does not change the claim, and the claim is the gate.
