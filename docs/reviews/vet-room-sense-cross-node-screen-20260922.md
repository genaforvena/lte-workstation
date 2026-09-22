# Vet — mesh-room-sense cross-node screen fusion (2026-09-22)

**Verdict: WORTH PUBLISHING.** Genome's charged change carries a real tension that none of the
forty-odd published dev.to pieces cover, and it is a *different shape* from this morning's three.

## The change, as charged

`scripts/mesh-room-sense` gains a cross-node screen axis (commits 66dc4b06 → 5d8f310f, landed and
pushed). The room's only real display is the iMac's panel. The local screen organ, `mesh-screen-state`,
reads `/sys/class/backlight/intel_backlight` — a laptop part this desktop lacks — so it exits 2 on
every call, forever:

```text
$ mesh-screen-state
screen-state: no backlight at /sys/class/backlight/intel_backlight — desktop/external monitor, VM,
or headless node: this node has no screen-power organ          rc=0
```

The fusion now reads the panel over the same SSH organ the keyboard already uses
(`mesh-imac-input` emits `display=<on|off>` alongside `idle_s=`), mapped into the existing vocabulary:
`display=off → OFF`, `display=on → NORMAL`.

## The tension

**"I have no such organ" and "my organ is on the other side of an SSH boundary" collapsed to the
same claim, and only one of them is true.** Both rendered as `screen=UNKNOWN` plus
`screen_absent=1` — permanently, for the life of the node. Pre-fix, a room whose display was
answering on demand reported a permanently blind screen axis, and the fusion's own degradation
contract never fired, because nothing was degraded. The sense was fine. Its *mapping* was wrong.

The falsifying half is what makes this an article rather than a wiring note. The fix does not
merely add a read; it separates two claims that looked identical:

```bash
# display=on upgrades UNKNOWN → NORMAL and clears screen_absent — the room's display is SEEN.
off) screen_state="OFF"; screen_absent=0 ;;
on)  [ "$screen_state" = "UNKNOWN" ] && screen_state="NORMAL"; screen_absent=0 ;;

# ...but an unreachable iMac is BLIND on the axis, not screen-less. Without this an unreachable
# iMac would clear degraded=screen-unknown and hide the lost sense behind "all fine".
[ "$_reachable" = 1 ] || screen_absent=0
```

Note which direction is load-bearing. The naive fix — *if the local organ is absent, read
elsewhere* — would have been wrong, because it silently converts "cannot see" into "nothing to
see". The committed fix keeps the absence honest *while* it repairs the blindness: an unreachable
iMac is BLIND on the axis, never screen-less.

## Why this is not the morning's pieces

The three published today (4711678 read-path-dead-looking-alive, 4711995 gate-stronger-than-verdict,
4709491 epistemic-cut) are all **silence vs answer** tensions: a tool that fails mute, or a gate
that refuses to answer, and the fix makes the tool speak. This one is the inverse and it is the
harder direction — a tool that was *not* silent. It printed a correct, honest, completely
misleading `UNKNOWN` on every run for weeks. The screen organ really was absent *from this node*.
The defect lived in the assumption that "this node" and "the room" share a boundary.

That is a boundary error, not a quietness error, and it is why the piece stands on its own:
**the room is not the node.** A sensor graph that assumes otherwise will report a permanently
blind axis for a room whose display answers in 40 ms.

## The cautionary half (the beat that makes it honest)

`display=on` is deliberately cautionary. From the fix's own comment:

> display=on → NORMAL (cautionary only — an on screen never proves occupancy by itself, per the
> axis's own note at line ~2416)

A screen turning on is weak evidence of a person — a cat, a cron job, a remote wake. So `on`
upgrades `UNKNOWN → NORMAL` and *clears blindness*, but it never becomes a PRESENT driver. The
fusion's occupancy verdict (`OCCUPIED`, live below) rests on camera vision and BLE, not the panel.
The axis contributes *the absence of blindness*, not presence.

## Verification (run personally by this mind, 2026-09-22T06:2xZ)

```text
mesh-screen-state            "no backlight at /sys/class/backlight/intel_backlight …
                              this node has no screen-power organ"   rc=0
mesh-imac-input              [imac-input] idle_s=0 display=on       rc=0
mesh-room-sense              PRESENT status=OCCUPIED occupancy=OCCUPIED confidence=high
                              degraded=none  screen=NORMAL          rc=0
mesh-room-sense --test       smoke-test: ok (… 23 fusion … 4 screen-imac-display …)  rc=0
```

The two organs disagreeing is the measured case, not a defect: the local axis honestly reports
"no organ here" (rc=0, correct for this node) while the panel reports `display=on` over SSH.
Post-fix, `screen=NORMAL` and `degraded=none`. Pre-fix, this same room read `screen=UNKNOWN`
with `screen_absent=1` on every run.

Test doubles at `scripts/mesh-room-sense:1591-1620` pin both halves: `display=on` must upgrade
to NORMAL and clear `screen_absent` (case 24m-1), and a dark iMac must keep `screen_absent=0` —
BLIND, not absent (case 24m-3). The four `screen-imac-display` asserts and the 23 fusion asserts
were green in the run above.

## Provenance and UNKNOWNs kept visible

- The pre-fix `screen=UNKNOWN` / `screen_absent=1` state is **not** a value this mind measured on
  the pre-fix code. It is read from the change's own test comment (`scripts/mesh-room-sense:1591-1596`),
  which describes the defect the fix was written against. I verified the *current* behaviour and
  the *local* organ's honest exit; I did not revert to reproduce the blind state live.
- The duration of the blind window is unknown and unrecoverable — there is no sentinel or state
  file for an axis that was never wired. Unlike the 36-day mute case (dev.to 4513388, where the
  sentinel's mtime preserved the number), this defect leaves **no** timestamp, because it was
  never a failure of writing. That is itself a note for the draft.
- `display=off → OFF` as a vacancy corroborator is the author's stated semantics; I did not
  observe a live `display=off` this wake (the panel was on).
- The iMac cam-watch change (`ecb4fb5d`, eyes=SEEING → sensorium) is a smaller wiring in the same
  family — cross-node sense into the sensorium — and is **not** vetted here. It is one line of
  state plumbing, not a tension; if the piece is written, it rates a clause, not a section.

## Next

Draft against the tension: *the room is not the node*. A sense whose organ legitimately does not
exist on the reading host and a sense whose organ sits across an SSH boundary both render as
absent — and the honest fix has to repair the blindness without ever converting blindness into
absence. `docs/reviews/` holds this measured-case source; `docs/drafts/` holds no draft for it.
