# Live-literature review — biosemiotics: index vs icon (mode of reference) and the perimeter's camera-only ALERT

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task) · status: **proposal, uncommitted** (security-path change — steward/operator weighs the trade-off before landing)

## Area & angle

Biosemiotics — sign and meaning in living systems — approached, as the task asks, through **a
foundational idea we have applied too loosely**: Peirce's trichotomy of the **sign–object
relation** — *icon* (references by resemblance), *index* (references by an existential/causal
connection), *symbol* (references by arbitrary convention). This trichotomy is the load-bearing
distinction of the whole field, and it is *live* literature, not a fixed classic — it is still being
worked operationally in the current journal (see cites). Searched the 2025–2026 *Biosemiotics*
(Springer) volume and the Peirce-in-biology literature.

**Where we'd been (biosemiotics, this mesh):** the *functional cycle* / Umwelt return-leg on
actuators (`biosemiotics-functional-cycle-closure-2026-07-24.md`) and the *information-balance*
metric R_sequence≈R_frequency for the wake recognizer (`biosemiotics-information-balance-wake-recognizer-2026-07-27.md`).
Neither touches the sign–object **mode of reference**. **Not embodied:** the index/icon distinction
as a *fusion rule*.

## The concept

Peirce, *Collected Papers* 2.247–249, restated in the current literature:

> "the symbol is linked to its object based on arbitrary convention; the icon is based on a
> relationship of resemblance; and in the case of the index, the relationship is an **existential
> connection** such as the causal link between a footprint and the person that left it."

The operational teeth, for a sensor mesh: **the three modes have different guarantees about the
existence of the object.**

- An **index** *cannot occur without its object*. A footprint entails a foot; a bang entails an
  acoustic event; a radiating BLE MAC entails a radio; a chassis IRQ entails a press. You cannot
  forge the index without producing (a token of) the cause.
- An **icon** references by *resemblance*, and resemblance is cheap to counterfeit. A photograph, a
  poster, a phone/TV screen, a reflection, a mannequin, a face on a video call — each is a perfect,
  high-confidence icon of a person **with no existential connection to a body being present**. An
  icon answers *what does this resemble* (identity), never *is it here* (existence).

That the distinction is **live, not archival** literature: *Biosemiotics* 2025 carries "Icon, Index,
Symbol: Deepening Histological Understanding Through Semiotics and Embodiment"
(doi:10.1007/s12304-025-09636-8), and the same journal uses index-vs-icon to *classify real
biological sign relations by mode* in "In the Case of Protosemiosis: Indexicality vs. Iconicity of
Proteins" (*Biosemiotics* 13, doi:10.1007/s12304-020-09396-7) — a molecular recognition that binds
by causal fit is indexical; one that binds by shape-resemblance is iconic. That paper does *exactly*
the transfer proposed here: tag a sign channel by its **mode of reference**, then reason about what
the channel can and cannot license.

*(Honesty note: the two Springer papers are paywalled; I read the search-surfaced titles/abstracts,
not the full texts. The definitional quote above is from the standard Peirce sources — media-studies.com's
Peirce summary and de Gruyter's "Biosemiotics and Peirce", lass-2023-0011. No quotes are invented from
the paywalled bodies.)*

## Where we applied it too loosely — `scripts/mesh-perimeter`, the PHYSICAL axis

`mesh-perimeter` fuses OUTSIDE/NETWORK/PHYSICAL into one CALM/NOTICE/ALERT verdict. Its PHYSICAL axis
already fuses **five** channels — and the tool's *own comments* rank them in the **exact inverse** of
Peirce's mode logic, without the vocabulary:

| channel (`_phy_sev` fold) | Peirce mode | current ceiling | the tool's stated reason |
|---|---|---|---|
| BLE presence (`mesh-presence`) | **index** (radio radiating) | CALM/NOTICE | — |
| device-free motion (`mesh-motion-attribution`) | **index** (displaced air/RF) | NOTICE | "can't say WHO" |
| **camera stranger** (`mesh-stranger-watch`/face-recognize) | **ICON** (resemblance) | **ALERT** (straight) | "a visual, identity-bearing confirmation is the **strongest** PHYSICAL signal available" |
| power-button IRQ (`mesh-powerbtn`) | **index** (a real press) | NOTICE | "a press is touch evidence, **not identity**" |
| room-ear impulse (`mesh-soundscape`) | **index** (a real acoustic event) | NOTICE | "a bang is an event, **not an identity**" |

Every **index** is capped at NOTICE and explicitly demoted as "an event/touch, not an identity." The
single **icon** is promoted to the top severity and fired **alone** — `stranger_phy_sev()`
(`mesh-perimeter:218`) returns `ALERT` on a fresh `ANNOUNCED|STRANGER-HELD` with no other axis
consulted.

The mistake is that the perimeter's question is **presence** ("is a body in the room?"), which is an
**existence** question — and for existence the **index is the strong sign and the icon is the weak
one**. The tool imported the icon's strength on the *identity* question ("who?") and spent it on the
*existence* question ("here?"), where the icon carries no existential guarantee at all.

The "2-of-2 frame confirmation" makes it **worse**, not better, in Peircean terms: two frames from
the *same camera* are **two icons sharing one failure mode** — both see the same photo/screen/
reflection. Iconic redundancy raises confidence in the *resemblance*, never in the *existence*. Only
an **independent index** (a channel whose connection to the object is causal, not resemblance) can
upgrade "resembles a stranger" to "a body is here." (Cf. memory `a-weak-surface-hit-suppresses-the-strong-surface`
— same shape: correlated confirmations that share a blind spot.)

Note the tool is scrupulous about the *other* honest-fusion axis — **reachability** (a dead sense →
UNREACHABLE/UNKNOWN, never a faked all-clear). But reachability is orthogonal to **mode of
reference**: a camera can be perfectly *live, fresh, and 2-of-2-confirmed* and still be imaging a
poster. Honest-fusion guards the dead-input failure; it does not guard the live-icon-of-an-absent-object
failure. That second failure is precisely what the index/icon distinction names.

## The concrete fix (implementable spec — for the steward)

Make the camera an **iconic identity** channel, not a standalone presence oracle:

- **A fresh confirmed camera stranger caps PHYSICAL at NOTICE** (never silenced — the operator still
  sees "camera: confirmed stranger, no corroborating physical sign"), **unless** an **independent
  indexical** channel is concurrently non-CALM — device-free motion, unknown BLE, a recent
  power-button press, or a room-ear impulse — in which case it escalates to **ALERT**. An index is
  the existential corroborant a photo/screen cannot produce; a real intruder is a body and *will*
  trip one.

Minimal change, `scripts/mesh-perimeter`:

1. **Reorder the folds** so the camera is folded **last** (currently it is fold #3 of 5, so at call
   time `phy_sev` has not yet seen powerbtn/ear). Move `stranger_phy_sev` after `scape_phy_sev`
   (perimeter:722), **or** thread an `any_index_hot` flag (1 if any of BLE/motion/powerbtn/ear
   raised `phy_sev` to NOTICE+) into the call.
2. `stranger_phy_sev(label, fresh, any_index_hot, cur)`:
   - fresh `ANNOUNCED|STRANGER-HELD` + `any_index_hot=1` → `ALERT`
   - fresh `ANNOUNCED|STRANGER-HELD` + `any_index_hot=0` → `max(cur, NOTICE)` (surfaced, not top)
   - else → `cur` (unchanged: stale/known/DARK/absent never escalate — keep the existing asymmetry)

Test deltas (perimeter `--test`, red-then-green per "a gate you have not seen FAIL is not a gate"):

```sh
# was: stranger_phy_sev ANNOUNCED 1 CALM  = ALERT   → now needs the index arg:
[ "$(stranger_phy_sev ANNOUNCED     1 0 CALM)"  = NOTICE ] || fail "icon-alone caps at NOTICE, never standalone ALERT"
[ "$(stranger_phy_sev ANNOUNCED     1 1 CALM)"  = ALERT  ] || fail "icon + a live index → ALERT (existential corroborant)"
[ "$(stranger_phy_sev STRANGER-HELD 1 0 NOTICE)"= NOTICE ] || fail "cooldown-held icon-alone stays NOTICE"
[ "$(stranger_phy_sev SILENT        1 1 CALM)"  = CALM   ] || fail "known/unconfirmed still never escalates, even with an index hot"
[ "$(stranger_phy_sev ANNOUNCED     0 1 CALM)"  = CALM   ] || fail "stale icon never escalates regardless of index"
```

**Trade-off, stated plainly (why this is a proposal, not a unilateral edit):** this *downgrades* the
one case of a perfectly still, silent, device-less stranger visible **only** to the camera from ALERT
to NOTICE. That case is real but narrow — and it is exactly the case device-free-motion and the room
ear are *also* blind to; the NOTICE still surfaces it. In exchange it removes the whole
photo/poster/screen/reflection/video-call false-ALERT class, which an identity-icon fired alone
cannot distinguish from a body. The operator should decide whether that trade is right for this node
before it lands; the mode-of-reference *observation* stands either way.

## If discarded in one line

Not discarded — it lands on a real, named security-fusion function (`mesh-perimeter:218
stranger_phy_sev`) whose own comments document the inverted ranking, and the index/icon distinction is
the biosemiotics literature's most operational and most-currently-worked handle on exactly this
"resemblance is not presence" gap.

## Sources

- [Icon, Index, Symbol: Deepening Histological Understanding Through Semiotics and Embodiment — *Biosemiotics* 2025](https://link.springer.com/article/10.1007/s12304-025-09636-8) (doi:10.1007/s12304-025-09636-8)
- [In the Case of Protosemiosis: Indexicality vs. Iconicity of Proteins — *Biosemiotics* 13 (2020)](https://link.springer.com/article/10.1007/s12304-020-09396-7) (doi:10.1007/s12304-020-09396-7)
- [Biosemiotics and Peirce — de Gruyter, *Language and Semiotic Studies* 2023](https://www.degruyterbrill.com/document/doi/10.1515/lass-2023-0011/html)
- [Peirce's ten classes of signs (Queiroz) — modeling biosemiotic processes](https://cspeirce.com/menu/library/aboutcsp/queiroz/10-biosem-jq.pdf)
- [Charles Peirce — Icon, Index, Symbol: Definition and Examples (media-studies.com)](https://media-studies.com/peirce-sign-categories/)
