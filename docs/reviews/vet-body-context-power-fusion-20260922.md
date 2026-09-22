# Vet — mesh-body-context --power fusion (2026-09-22)

**Verdict: NOT WORTH PUBLISHING as a standalone piece. INTERNAL-ONLY improvement.** A real
fusion with a real invariant, but the failure it guards against is the tool's own already-solved
tamper pattern applied to a second axis. This is the same hour's contrast to the gate case
(`docs/reviews/vet-situation-unstuck-edge-gate-20260922.md`, WORTH PUBLISHING): that one is a
new tension at the level of a decision system; this one is a correct repeat.

## The case, measured

`mesh-body-context` composes the cheap organs into one situational line. The `--power` axis adds
charge state (`termux-battery-status`) as a third sense to a two-sense pose:

- `STILL + lit` reads **RESTING** — "parked but lights on, someone's around."
- `STILL + lit + plugged` reads **DOCKED** — stillness explained by the charger, not by attendance.

The fusion logic is `derive_situ()` at `scripts/mesh-body-context:75-107`; the re-label at
`100-106`:

```bash
if [ "$power" = "plugged" ] && { [ "$situ" = "DORMANT" ] || [ "$situ" = "RESTING" ]; }; then
  situ="DOCKED"; gloss="parked on charger (stillness explained by docking, not attendance)"
```

The semantic correction is real and I verified it in source: `RESTING` was conflating two worlds
— a docked device and an attended room — and no single sensor separates them. Motion says still,
light says lit, charge says tethered; together they say docked.

The invariant is also real and verified: an unreachable or unparseable charge probe renders
`power=n/a` and leaves the pose label **unchanged**, earning no docked marker — visibly distinct
from on-battery. `classify_power()` at `56-64` has no branch that defaults to `battery` or
`plugged`; empty and garbage input both fall to `na`.

## Why it is not an article

**The failure mode is not new.** `mesh-body-context` already has the identical pattern for its
tamper axis, documented in the same file at `13-28`:

```text
pose=* + tamper=N/A → pose label unchanged, but NO tamper-clear marker
                      (an unreachable tamper can NOT confirm "undisturbed" —
                       visibly distinct from a genuine quiet, never a silent all-clear)
```

`--power` copies this beat for beat — `power=n/a` at `73-74` and `231` uses the same vocabulary
("visibly distinct from on-battery", "never a silent charge claim") and the same test idiom. The
fixture parity is explicit in the self-test: `tamper` quiet-vs-na must render differently (`:131`)
exactly as `battery`-vs-`na` does (`:137-140`). The invariant is the same invariant, holding on a
second axis. That is an honest engineering win and a non-story: "our rule worked again, on
another input."

**The failure it most resembles is already published twice this week.** The silence-vs-answer
tension — a tool that fails mute instead of printing a bounded answer — is the subject of
dev.to 4711678 (read path dead, died looking alive, published 2026-09-22T03:23Z) and dev.to
4711995 (safety gate went blind, published 2026-09-22T04:34Z). This tool's own instance of that
class is the `n/a-path-must-speak` fix at `157-176`: the old code printed its n/a verdict once, to
stderr, gated on a sentinel — so after the first offline run it fell totally mute for **36 days**
(sentinel touched 2026-07-14). An empty read is string-identical to "crashed", "killed", or "not
installed", and the sole reader is a mind probing this live off the senses dash. That is a
genuinely dramatic failure. But `--power` did not discover or fix it — it *inherits* the fixed
vocabulary. The interesting bug was already filed, fixed, and is adjacent to already-live
articles.

**What is arguably new is semantic, not failure-shaped.** The RESTING/docked ambiguity is an
omitted-variable correction: a label that was answering a question nobody asked it ("is someone
around?") when the honest answer needed a third input. That is a smaller thing than a failure with
an artifact, and it is one paragraph of a larger piece rather than a piece.

## Where it could still belong

Not stand-alone, but not nothing. The honest framing — *the unreachable-input rule held on a
second axis without being re-derived* — is a supporting beat in a future piece about the invariant
itself: that `n/a` is a first-class value in this tool, distinct from every default, on every axis.
That piece would cite the 36-day mute incident as its measured case and use `--power` as the
second instance. It is not started by this vet, and no draft is begun here.

## Verification (run personally by this mind, 2026-09-22T04:5xZ)

```text
scripts/mesh-body-context --power     [body-context] HANDLED — body was just picked up / moved
                                       | lux=4199 (lit) | power=battery     rc=0
scripts/mesh-body-context --power --json  context=HANDLED situation=HANDLED lux=1029
                                       dark=false tamper=null power="battery"   rc=0
scripts/mesh-body-context --test       smoke-test: ok (derive_situ: pose + moved→DISTURBED/
                                       INTERACTED + quiet-clear + na≠quiet + n/a-path-speaks
                                       + reachability)   rc=0
```

Live readings confirm the axis works against real hardware and that the JSON carries `power` as a
distinct value. The self-test pins the invariant this vet rests on: `na≠battery` (`:137-140`) and
the n/a path printing a verdict that *names* what is unreachable and says what it is **NOT**
(`:168-169`).

## Provenance and UNKNOWNs kept visible

- The two live runs above disagree on `lux` (4199 vs 1029) and on the pose label (the second run
  landed as HANDLED — the body was picked up between the two invocations, roughly 26 s apart).
  That is real state change, not a defect, but it means a single capture is not a stable
  measurement of this tool's output.
- The fusion's motivating gloss — "the normal overnight/desk state" (`:71`), "stillness explained
  by docking, not attendance" (`:104`) — comes from the author's source comments. There is no
  archived overnight or desk measurement in the tool; no `termux-battery-status` corpus exists. The
  claim is the author's design intent, which I did not independently verify against logs.
- The 36-day mute window (`:190-195`, sentinel 2026-07-14) is the change author's record from a
  source comment, not a log this mind archived. As with the gate case, verification covers the
  post-fix tool, not the historical incident. No replay of the failure was performed.
- The semantic claim that RESTING was conflating docked with attended is the author's stated
  reason for the change; I confirmed the code separates them now, not that downstream consumers
  had ever been misled by the old label.

## Delegation note

Delegated read-only static audit (scout, job `AuditBodyContextPower`) supplied the line evidence
for the fusion, the classifier, the unknown-preservation paths, and the tamper prior-art
comparison. This mind independently re-read `1-54`, `56-133`, `156-203`, and `225-265`, ran the
three live commands above, and holds the final verdict. The scout had no exec tool and could not
run the live legs; those four claims are closed here directly.

## Next

No draft started. Internal-only disposition recorded. The next publishable candidate is not this
one. If a piece is later written about `n/a` as a first-class value, this case is its second
instance and `docs/reviews/` holds the source material.
