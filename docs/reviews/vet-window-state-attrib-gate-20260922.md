# Vet — mesh-window-state attribution gate: who is allowed to lower an alarm (2026-09-22)

## Verdict — WORTH PUBLISHING (conditional), and the condition is not yet met

**Re-checked 2026-09-22T12:2xZ (claim `pub-vet-window-state-attrib-gate-20260922/vet-write`). The
hold stands, and the blocking condition is unchanged.** The event log still holds exactly one entry,
still `UNKNOWN`, and the ALERT→MOTION downgrade branch has still never fired in production:

```text
$HOME/.mesh/.tamper-events     1788402319|UNKNOWN        (1 line; same 2026-09-03 entry, ~19d)
scripts/mesh-tamper --status   tamper: quiet (133s ago, window=8, recency=COLD,
                               events_24h=0, last_attrib=UNKNOWN, burst=NONE, cadence=NA)
scripts/mesh-window-state      [window-degraded] DEGRADED — missing: tamper,body-motion
scripts/mesh-window-state --test   rc 0 — 47 assertions (identical suite, re-run this wake)
```

The one thing that moved since the original vet is the *producer*: at vet time `mesh-tamper` read
`OFFLINE` (825s state age); now it reads **`quiet`** with a 133s state age and a live presence input
(`FAMILIAR`) beside it. That is the *`cur_attrib` arm's exact precondition*: a live, fresh
familiar-now reading available to consult when the tamper side records its next event. The gate's
second rule has a live producer to be tested against — it simply has not been tested by an event
yet. This is recorded because it is the half of the condition that *has* improved: the missing
instrument is no longer missing, only the observation is.

**Decision unchanged: hold the publish.** The two satisfaction conditions below remain the gate.
The re-check narrows what is being waited on — not "the sensor is down" but "the sensor is up and
has not yet been moved while someone familiar is nearby".

The case is **not** already published. A delegated read-only audit (scout `AttribGateDedupeAudit`)
read all 57 of the author's dev.to articles via the API and found **zero** that cover the
attribution-downgrade tension: the three closest are all a different direction.

- `4524740` "I fixed the sensor and silently broke the alarm above it" — a sensor fix broke the
  alarm *above* it (the opposite direction: a repair that caused silence, not a benign annotation
  that silences).
- `4487371` "Your backlog alarm is an accumulation statistic" — alarm statistics, no attribution.
- `4711995` "The sensor was fine. My safety gate was the thing that went blind." — a readiness gate
  producing silence; no tamper/presence/attribution vocabulary at all.

Nor is it in the repo: no in-repo published-article index lists it, `docs/attribution.md` describes
the ATTRIBUTED-vs-UNATTRIBUTED *cluster* but not this gate's event-time/current-state asymmetry, and
the review that produced the gate exists only as a source comment (`chat-review/window-state-alert-attrib-gate
2026-07-07`), never as an artifact. **Dedupe: clear.**

**The condition that is not met.** The publishable claim here is a *measured non-event*: the gate
has never been observed lowering an alarm. The event log contains **one** event ever, and it is
`UNKNOWN`:

```text
$HOME/.mesh/.tamper-events     1788402319|UNKNOWN        (1 line; 2026-09-03, ~19 days ago)
```

No `ATTRIBUTED` event has been recorded, so the downgrade branch has never fired in production. The
charter's rule — *write from a measured case, never from a summary of one* — means the honest
publishable framing is "the alarm that was designed to be silenceable, and the one event it saw was
the case it refused to be silent on", which is a weaker and more honest piece than the design reads.

**Decision: hold the publish.** Write the draft only when one of these is satisfied:
1. a real `ATTRIBUTED` disturbance event lands in `.tamper-events` and the ALERT→MOTION downgrade is
   observed in `.window-state`, or
2. a real `SUSPECT`/`AMBIGUOUS` event lands beside a fresh `cur_attrib=ATTRIBUTED` and the ALERT
   holds — the *more* publishable of the two, because it is the case where the annotation refused to
   quiet an alarm it could have quieted.

This vet is the artifact. Nothing has been posted.

---

## The case

`mesh-window-state` fuses four security senses (tamper disturbance, BLE presence churn, Wi-Fi
multipath motion, phone body motion) into one room verdict: `ALERT` / `CO-MOTION` / `MOTION` /
`QUIET` / `DEGRADED`. The `ALERT` branch is driven by `mesh-tamper` — the phone's
`SIGNIFICANT_MOTION` hardware trigger, which fires only on real physical motion. For a phone that is
supposed to sit parked, a fire means someone moved or picked it up.

An annotation can lower that alarm. `mesh-tamper-attrib` fuses the disturbance with `mesh-presence`
(BLE personal presence and *familiarity* — a settled known device nearby) and returns one of
`ATTRIBUTED` (moved, familiar person nearby — expected) · `SUSPECT` (moved, but nobody familiar, or
only an appliance, or a stranger) · `AMBIGUOUS` (inconclusive) · `UNKNOWN` (a sensor is stale or
missing) · `NONE` (nothing to attribute).

The design question is not whether to trust that annotation. It is **which annotation is allowed to
lower an alarm, and on whose evidence.**

## The asymmetry, in code

`classify_window` takes two attribution sources, and the precedence between them is the whole point
(`scripts/mesh-window-state:178-215`):

```bash
if [ "$tamper" = "ACTIVE" ] || [ "$tamper" = "RECENT" ]; then
  if [ "$attrib" = "ATTRIBUTED" ]; then
    echo "MOTION|tamper=$tamper attrib=ATTRIBUTED (familiar handling)"
    return
  fi
  if { [ "$attrib" = "UNKNOWN" ] || [ -z "$attrib" ]; } && [ "$cur_attrib" = "ATTRIBUTED" ]; then
    echo "MOTION|tamper=$tamper cur_attrib=ATTRIBUTED (familiar person nearby now)"
    return
  fi
  echo "ALERT|tamper=$tamper (event in last 30min — security concern)"
  return
fi
```

Two rules, and the second is the interesting one.

**Rule 1 — event-time attribution is primary.** `attrib` is field 6 of `mesh-tamper`'s state,
recorded *at the moment the disturbance fired* (freshness-gated presence, classified with
`mesh-tamper-attrib`'s exact vocabulary). A familiar pickup is not a security concern, and
`ATTRIBUTED` downgrades it. Every other value — `SUSPECT`, `AMBIGUOUS`, `UNKNOWN`, `OFFLINE`, and
the empty field of a legacy 5-byte state — keeps `ALERT` unchanged. *Fail-suspicious, never
fail-quiet on an unrecognized or absent attribution.*

**Rule 2 — a current reading can only fill an absence, never overrule a verdict.** `cur_attrib` is
`mesh-tamper-attrib`'s own */10* cached read: *who is nearby now*, distinct from *who was nearby at
the event*. It is consulted **only** when the event-time attribution is genuinely absent
(`UNKNOWN`/missing). A recorded `SUSPECT` or `AMBIGUOUS` event verdict **stands** even beside a
fresh familiar-now.

That second rule is the case. The obvious implementation — "someone familiar is home right now, so
lower the alarm" — would erase a genuine unattributed disturbance. The operator could be home, and
the disturbance could still be someone else. The annotation is allowed to speak only where the event
itself left a gap.

## Why this generalizes

The pattern is a security-relevant instance of a shape that appears everywhere an interpretation
layer is allowed to soften an alarm: a liveness probe, a "known good" baseline, a canary that
silences a rollback, an allowlist entry, a maintenance window. Each is a *silencer*, and each one is
correctly trusted only on evidence about **the event**, not evidence about **the present**.

The two rules above answer the two questions a silencer has to answer:

1. **What is the annotation evidence for?** Event-time. A presence reading taken minutes after a
   disturbance is a different claim than one taken at the fire, and `mesh-tamper` captures
   it at the fire precisely because the */10* fusion cron would otherwise miss a moved verdict that
   a quiet overwrite before the next run.
2. **May a present-state reading overrule an event verdict?** No — it may only *fill a gap*. The
   asymmetry is one-directional by construction: absence degrades toward the alarm, never away from
   it.

The diagnostic worth stealing: for any alarm you own, find the component allowed to lower it, and
ask whether its evidence is about the event or about the present. If the answer is "the present", the
alarm can be quieted by whoever happens to be standing near it.

## Verification (run personally, 2026-09-22T10:5xZ)

```text
scripts/mesh-window-state --test        rc 0 — 47 assertions (18 fusion + 10 tamper-attrib +
                                          5 wifi reader + 9 body reader + 5 cadence-staleness)
scripts/mesh-tamper-attrib --test       rc 0 — 14 classify assertions + 1 distinctness + real read
scripts/mesh-tamper-attrib              UNKNOWN — tamper=UNREADABLE, presence=ACTIVE_NEAR/FAMILIAR
scripts/mesh-tamper-attrib --live        UNKNOWN — tamper=unreachable (real read attempted, rc 0)
scripts/mesh-tamper --status            OFFLINE (825s ago, recency=COLD, events_24h=0,
                                          last_attrib=UNKNOWN, burst=NONE, cadence=NA)
scripts/mesh-presence                   rc 0 — personal_presence=ACTIVE_NEAR familiarity=FAMILIAR
```

The classification contract, exercised directly through `classify_window` (the pure, offline-testable
core), covering both rules and every fail-suspicious branch:

```text
classify_window ACTIVE 3 STILL STILL ATTRIBUTED   → MOTION|tamper=ACTIVE attrib=ATTRIBUTED (familiar handling)
classify_window ACTIVE 3 STILL STILL UNKNOWN/ATTRIBUTED
                                          → MOTION|tamper=ACTIVE cur_attrib=ATTRIBUTED (familiar nearby now)
classify_window ACTIVE 3 STILL STILL SUSPECT ATTRIBUTED
                                          → ALERT|tamper=ACTIVE (event in last 30min — security concern)
classify_window RECENT 3 STILL STILL AMBIGUOUS NONE
                                          → ALERT|tamper=RECENT (event in last 30min — security concern)
classify_window ACTIVE 3 STILL STILL ""  ATTRIBUTED
                                          → MOTION|tamper=ACTIVE cur_attrib=ATTRIBUTED (legacy 5-field)
classify_window NEVER 3 STILL STILL "" NONE       → MOTION|churn=3 (BLE devices came/went recently)
```

The third line is the publishable sentence: **a `SUSPECT` event verdict standing beside a fresh
`ATTRIBUTED` now-still-alarm.** The annotation had the power and refused to use it.

## Provenance and UNKNOWNs kept visible

- **No live event.** The tamper producer is `OFFLINE` at vet time (state age 825s, `events_24h=0`),
  and the event log holds exactly one entry, `1788402319|UNKNOWN` (2026-09-03, ~19 days ago). The
  entire `ALERT`→`MOTION` branch has never fired in production on this node. Every verification line
  above is a unit test and a direct call to the pure classifier; **not one is an observed production
  downgrade.** This is the reason the publish is held, and it is stated rather than smoothed over.
- **Origin.** The gate landed in `8b109e66` "mesh-window-state: gate the tamper ALERT on
  mesh-tamper's field-6 last_attrib" (2026-07-07, genaforvena). `26f3677` — the commit the source
  comments cite — is `mesh-tamper`'s *event-time attribution + ambient-gated severity*, the producer
  that writes field 6. Two commits, one contract; the reader comment names the producer, the gate
  names the consumer, and neither is wrong, but the vet names the gate's own commit.
- **The originating review is not an artifact.** `chat-review/window-state-alert-attrib-gate
  2026-07-07` exists only as a source comment (`scripts/mesh-window-state:78-82, 197-213, 318-322`);
  grep for it across `docs/` and `~/.mesh/` returns no case record. The design intent is therefore
  only as durable as the comment.
- **`a9e5bebf` was investigated and dropped.** The most recent `mesh-window-state` commit's message
  reads "vv2 originally used 'BROKEN', which is not in the alarm alphabet at all, so it went quiet
  for…" — an adjacent and genuinely publishable case (a label outside the alarm vocabulary silently
  disabling the alarm path), but it is a landing stub with no artifact, no file, and no discoverable
  `vv2` tool. It is **not** used as evidence here and should not be written up until it has one.
- **The live tamper read was attempted, not assumed.** `mesh-tamper-attrib --live` and
  `mesh-tamper --status` both ran and both returned the honest `UNKNOWN`/`OFFLINE`; the presence
  input beside them is live and `FAMILIAR`, so the `cur_attrib` branch's freshness gate has a live
  producer to consult when the tamper side recovers.
- The r/homelab and r/selfhosted lanes remain gated (see pane) and are out of scope for this vet.
- This is a **vet, not a publish**. The dev.to draft and URL are a separate decision and a separate
  task; nothing here has been posted.
