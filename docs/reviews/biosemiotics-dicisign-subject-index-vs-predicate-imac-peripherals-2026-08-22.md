# The dicisign: a measured predicate hung on a nickname, and the address that was parsed and thrown away

**Live review, 2026-08-22 — biosemiotics (sign and meaning in living systems), from the angle the task
asked for: a CROSS-DOMAIN transfer into a distributed sensor mesh.**
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-imac-peripherals` — assigned by coin at p=0.20, drawn uniformly from
the lane's 568 never-reviewed tools. Not chosen by me and not chosen by the lane.
Landed in `scripts/mesh-imac-peripherals` (uncommitted — steward lands from the tree).

## What was already ours

Thirteen prior biosemiotics landings: code duality · code-vs-interpretant · dialogue of constraints ·
ecoacoustics/ACI · efficiency sensing · functional-cycle closure · incentive salience · **index vs
icon** (`mesh-perimeter`) · information balance · the interactive sign · the interpretant · the
senome's analog continuum · Umwelt degeneracy.

The closest is `biosemiotics-index-vs-icon-perimeter-stranger-2026-07-28`, which asks *what MODE of
reference a sign has*. It does not ask the next question, and no review in the corpus contains the
word **dicisign**: given that a reading is a whole PROPOSITION, are its two parts — the part that says
which object, and the part that says what is the case — separately identifiable at all?

## The find

**Nielsen, H., Vitti-Rodrigues, M. & Emmeche, C. (2026). "Measuring Meaning of Molecular Motifs."
*Biosemiotics*. doi:[10.1007/s12304-026-09637-1](https://link.springer.com/article/10.1007/s12304-026-09637-1)**
— found by live search of the journal's 2026 volume on 2026-08-22. Springer full text is paywalled
from this vantage; **this review is written from the landing page's abstract, not the full paper**,
and the sign-structure below is Stjernfelt's standard dicisign theory (*Natural Propositions*, MIT
Press 2014), which the paper applies. The paper's move: bioinformatics meets biosemiotics and **signal
peptides emerge as dicisigns**, showing "the perceived tension between Shannon's quantitative/
statistical theory of information and the biosemiotic approach to semantic and interpretational
aspects of living systems need not be as big as previously conceived."

A **dicisign** is Peirce's class for the simplest sign that can be TRUE or FALSE — a "natural
proposition". It is **composite by necessity**, and both parts must be separately identifiable:

| part | mode | job |
|---|---|---|
| **subject** | INDEX | picks out *which object* the sign is about |
| **predicate** | ICON | says *what is the case* of it |

Drop the indexical half and you still have a sign — but not one that can be false *about a particular
thing*. That is the transferable claim, and it is exactly a sensor-mesh problem: **a reading is a
proposition, and a mesh that measures its predicate carefully while leaving its subject as a nickname
has built a sign that cannot be wrong in any locatable way.**

## The organ, read as a proposition

`mesh-imac-peripherals` emitted:

```
[imac-peripheral] name="Apple Wireless Keyboard" battery=62 low=no
```

- **predicate** — `battery=62 low=no`. Measured, parsed carefully, thresholded against `LOW_BATT_PCT`.
- **subject** — `name="Apple Wireless Keyboard"`. A string the operator types into macOS System
  Settings and can change at any time.

And the actual index was *right there in the input and discarded*: the parser reads each device block,
sees `Address: 7C-C3-A1-8C-26-6B`, and never captures it. Three consequences, none of which any test
could have caught, because every fixture asserted the name:

1. **A rename reads as a new device.** Nothing ties two readings of the same keyboard together, so
   there is no drain rate, no history, no "this one has been falling for a week".
2. **Two peripherals sharing a name collapse onto one utterance.** Entirely plausible on a household
   iMac (the tool's own fixture already carries a device named in Russian by its owner).
3. **The subject vanishes exactly when the predicate matters.** The parser emitted only devices with
   `Connected: Yes` AND a `Battery Level`. A peripheral whose battery dies **disconnects** — so the
   sense went silent precisely at the event it exists to predict, and that silence was byte-identical
   to "never paired". The shipped test asserted this defect as correct: *"FAIL: disconnected/
   battery-less device must not appear"*.

## What landed

```
[imac-peripheral] addr=7C-C3-A1-8C-26-6B name="Apple Wireless Keyboard" battery=62 low=no
[imac-peripheral] addr=28-11-A5-B8-9E-A2 name="Bose Revolve SoundLink" battery=na low=na reason=disconnected
[imac-peripheral] unindexable=1 (paired device(s) with no Address — no subject, so no reading can be about them)
```

- **The Address is the subject; the name is demoted to a label.** Both are emitted (text and JSON) —
  the label is for humans, the index is the identity.
- **The predicate may be absent without the subject vanishing.** `battery=na` plus a `reason=`
  (`disconnected` / `no-battery-profile`), never 0 and never omitted — the mesh's standing rule that
  an `na` names its own cause.
- **A device with no index is not folded in.** It cannot be a subject, so nothing true or false can be
  said of it; it is counted and named as `unindexable=N` rather than dropped in silence.

## Verification

`--test` drives the contract rather than asserting the old strings: the keyboard and the low-battery
mouse are asserted **by address**, a disconnected device must survive with `battery=na reason=disconnected`,
a **rename fixture** (`Apple Wireless Keyboard` → `Клавиатура Ильи`) must keep the same subject and the
same population of subjects, and a device with no `Address:` must produce `unindexable=1` and **no**
predicate. The honest-exit contract is unchanged (rc 2 on an unreachable iMac; it is unreachable now,
so the live-read leg reports n/a rather than fake-green).

Driven red three ways, restored green each time:

| mutation | result |
|---|---|
| stop parsing `Address:` (subject reverts to the name) | `FAIL: keyboard fixture (got: … unindexable=3 …)` |
| re-drop disconnected/battery-less devices (the shipped behaviour) | `FAIL: a disconnected subject must survive with an na predicate + reason` |
| emit `addr=?` for an unindexable device instead of counting it | `FAIL: zero-peripheral fixture (… addr=? name="Some Phone" …)` |

## Sources

- [Nielsen, Vitti-Rodrigues & Emmeche 2026, *Biosemiotics*, doi:10.1007/s12304-026-09637-1](https://link.springer.com/article/10.1007/s12304-026-09637-1) (abstract only from this vantage — paywalled)
- [Interactive Signs and Digital Umwelts: Rethinking Meaning in the Age of Platfospheres, *Biosemiotics* 2025](https://link.springer.com/article/10.1007/s12304-025-09607-z)
- [Umwelt-based Analysis of Multispecies Places: Guidelines for Application, *Biosemiotics* 2026](https://link.springer.com/article/10.1007/s12304-026-09644-2)
- [Introduction: Semiotic Scaffolding, *Biosemiotics*](https://link.springer.com/article/10.1007/s12304-015-9236-1)
