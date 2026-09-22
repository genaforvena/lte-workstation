# Vet — mesh-note3-connectivity MCC annotation links (2026-09-22)

**Verdict: WORTH PUBLISHING, but not next in queue.** The tension is real and measured, but this
case is a verified design restraint rather than a failure found and repaired, so it ranks below
the failure-recovery pieces already queued. Recommendation: hold it until the queue clears, then
publish it as a short piece, not a full article.

## What was claimed

Two MCC ("mind-consumer-consumer") producer↔consumer links, both feeding one consumer,
`scripts/mesh-note3-connectivity`:

- `mesh-note3-cellsignal` → the connectivity verdict, annotated as `cell=`
- `mesh-note3-touchidle`  → the connectivity verdict, annotated as `idle_s=`

Both are declared **additive annotation only** — the annotation must never change the verdict or
the exit code, and a dark producer must render `UNKNOWN`, never a faked level or age.

## The measurement, run personally at 2026-09-22T15:37:46Z

Consumer, one read:

```
ONLINE|active_default=1|connected=1|interface=1|validated=1|transport=REACHED|cell=POOR|idle_s=60576|reason=validated-default|ts=2026-09-22T15:37:46Z   (rc=0)
```

Both producers, run directly and independently:

```
mesh-note3-cellsignal:  status=OK radio=gsm asu=6 dbm=-101 level=POOR           (rc=0)
mesh-note3-touchidle:   status=OK idle_s=60576 band=IDLE wakefulness=Awake interactive=true  (rc=0)
```

Transport axis, read from its own state file (a separate writer, not self-asserted):

```
REACHED 2026-09-22T15:35:01Z serial=4d00553d61ab90b7 device_uptime_s=310042.60 node=local
```

`idle_s=60576` is **16 hours 49 minutes** since the last touch. The verdict is `ONLINE` by a
validated default route over a **POOR** cellular radio on a body nobody has touched all day.

## The tension worth the piece

A green verdict that carries its own contradiction — and is still correct.

The route is validated; `ONLINE` is the truthful answer to "does this phone have a current default
network?" The radio is marginal and the phone is untouched, and both facts ride along in the same
line. The tool refused to let a bad radio flip a correct verdict, and refused to hide the bad radio
either.

This is the inverse of the closest published piece. "My pose sensor said someone was home. The
phone was just on the charger" (dev.to 4716071) is a green verdict fooled by a confound. Here the
conflound is present and the contract is the correction: the confound is surfaced as an annotation
and explicitly forbidden from touching the decision. The publishable sentence is not *my green
light lied* but *my green light told the truth and still warned me.*

## The contract, verified against source

Additive-only is wired correctly, and the wiring is provable, not asserted (`scripts/mesh-note3-connectivity`):

- `cell_quality()` (lines 64–71) and `touch_idle()` (lines 78–84) return a bare token; they cannot
  reach the verdict. A failed producer call yields `UNKNOWN` — lines 68 and 81 fall through on
  non-zero and emit it, never a fabricated value.
- `probe()` (lines 93–98) interpolates the two tokens into a format string after the verdict is
  already decided. The verdict and the exit code are computed from the connectivity dump alone.
- The `UNKNOWN` arms are real and exercised, not stubs that pass trivially: `--test` (lines
  113–142) forces a dark radio (`level=unknown`, rc 2) and a dark touchidle (`idle_s=unknown`,
  rc 2) and asserts the verdict's exit code is unchanged while the annotation renders `UNKNOWN`.
  Both arms passed here.
- The restraint is load-bearing in both directions: line 125 asserts a dark radio **must not**
  change the verdict rc, and line 126 asserts it **must** still render `cell=UNKNOWN`. A tool that
  silently dropped the annotation on failure would pass the first and fail the second.

The transport axis is genuinely independent: `transport_live()` (line 48) greps a state file
written by a separate adb probe, and line 88 returns `UNKNOWN … transport=UNREACHABLE` with rc 2
when that file lacks this serial. `transport=REACHED` is read, not assumed.

## Two honest findings

**The cell radio drifts, and the pane line is stale.** Within this vet window the serving cell
moved between three readings 8 minutes apart:

```
15:29Z  asu=8  dbm=-97   WEAK
15:33Z  asu=4  dbm=-105  POOR
15:37Z  asu=6  dbm=-101  POOR
```

The pane novelty line reports this link as "live ONLINE cell=**STRONG**". That was true when the
line was written; it is not true now. This is not a tool defect — the radio is genuinely mobile —
but any article drafted from the pane line instead of a live read would carry a wrong number. The
pane's own NEXT line is right: vet one measured case before drafting.

**`--json` is a false promise.** `scripts/mesh-note3-connectivity` accepts `--json` and `-j` and
silently ignores both — the only argument handled is `--test` (line 101); everything else falls
through to `probe()`, which takes no arguments. A machine consumer requesting JSON receives the
pipe-delimited verdict line and has no way to detect that it did not get what it asked for. No
current consumer is broken: `scripts/mesh-dash:2469-2471` reads `.note3-connectivity.state` with
`head -1` and renders it as text. Flagged as `[chat-review]`, not fixed from this window — the
charter forbids repairing another window's tool here.

## Why this ranks below the queue

The published and queued pieces each have a failure that was found and repaired: a dead read path
that died looking alive, a safety gate stronger than the verdict it guarded, a pose sensor fooled
by a charger. Each is an arc. This case has no failure — the design was correct and the vet proves
it held under live load. That is a weaker shape for a piece, and publishing it ahead of a
failure-recovery arc would spend the reader's attention on restraint when the stronger material is
ready.

The measured claims above are unaffected by that ranking. They were run personally and they hold.

## Verification

- Ran all three tools live at 2026-09-22T15:37:46Z; consumer rc 0, both producers rc 0, transport
  state read from its own file.
- Ran `scripts/mesh-note3-connectivity --test`: offline fusion arms pass, cell and idle annotation
  arms pass (stub-annotated and dark-UNKNOWN both asserted), live ADB read green.
- Read `scripts/mesh-note3-connectivity` in full (152 lines) to confirm the additive contract at
  the source level rather than from the comment alone.
- Compared against the nine live dev.to articles to check the angle is not already published;
  closest is 4716071, and this case is its inverse.
- Searched `docs/` for prior coverage of these two links: `note3-connectivity` returns no existing
  vet or pub artifact; `cellsignal` and `touchidle` appear only as passing mentions.

## Decision

Land the vet. Do not draft or publish from here this wake: the case is publishable but ranks below
the queued failure-recovery pieces, and the charter forbids publishing without naming the artifact
afterward. Next pub action on this case is a short draft once the queue clears — written from the
live readings above, not from the pane line, whose `cell=STRONG` is already wrong.
