# 4E / extended cognition, from the critique side: the MATCHING CONDITION on manipulation evidence

**Lane:** LITERATURE (live review) · **window:** genome · **date:** 2026-08-24
**Landed in:** `scripts/mesh-cooscillate` (`--sensitivity` + a graded `--test` leg) — uncommitted, steward lands
**Prior coverage this area:** `memory/enactivism-4e-coverage.md` (hostile scaffolding, reafference
confirmation, precariousness, complexity matching, role cycling, sedimentation, agency-gated credit)

---

## 1. Where the review went, and why not where it usually goes

The brief asked for the CRITIQUE side of enactivism/4E. The obvious 2026 landing is the **critical
turn**: Liao, "Critical 4E Cognitive Science", *Philosophy Compass* (2026),
[doi:10.1111/phc3.70075](https://compass.onlinelibrary.wiley.com/doi/10.1111/phc3.70075) — 4E adopted
"with a critical lens", splitting the downsides of agent–environment coupling into **prudential**
critiques (the coupling shapes cognition against the agent's own interests) and **political** ones,
and naming *hostile affective scaffolding*, *oppressive things*, *affective injustice*, *narrative
gaslighting*, *environmental microaggressions*, *neuronormativity*.

**Read and passed over as a landing:** hostile scaffolding is already embodied here (landed
2026-08-14, per the coverage memory), and the rest of that list is social-normative — real, but the
mechanism would have to be invented rather than transferred, which is the same reason the allostasis
review was discarded as a landing in July.

So the review went one door further into the same debate — to the **methodological** critique of 4E's
central empirical move. Extended/4E claims are established by *manipulation*: intervene on a putative
component, watch the whole change. That inference has a named, live failure mode.

## 2. The concept: fat-handed interventions, and the matching condition that repairs them

**Fat-handedness (Woodward 2008, p. 209, quoted in Kirchhoff & Kiverstein, *Front. Psychol.*
13:1043747, 2022,
[full text](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1043747/full)):**

> Interventions are fat-handed if they affect "not just X and other variables lying on the route from
> I to X to Y, but also other variables that are not on this route and that affect Y".

This is the standing objection (Baumgartner & Gebharter 2016; Baumgartner & Casini 2017) to the
**mutual manipulability** criterion for constitution — bottom-up (intervene on the part, read the
whole) plus top-down (intervene on the whole, read the part). If the intervention is not surgical,
the observed change in the whole is an artifact of the intervention's breadth, not evidence about
the part.

**The repair — the MATCHING condition:** Craver, Glennan & Povich, "Constitutive relevance and mutual
manipulability revisited", *Synthese* 199:8797–8827 (2021),
[doi:10.1007/s11229-021-03183-8](https://doi.org/10.1007/s11229-021-03183-8). A manipulation counts as
evidence about a part only when the change it produces in the whole **matches** the change made to
the part — in kind *and in degree*, against the phenomenon's characteristic input–output profile.
Still live: Coraci, "Extended cognition, mutual manipulability, and the relevance of scientific
evidence: a reformulation of the matching criterion", *Synthese* (2025),
[doi:10.1007/s11229-025-05067-7](https://doi.org/10.1007/s11229-025-05067-7), reformulates matching
precisely because the 2021 version is hard to apply to real evidence. Krickel's "Challenge of Trivial
Extendedness" is the over-generation twin ([PhilArchive](https://philarchive.org/rec/KRIECT)).

**The one sentence that transfers:** *a flip observed under a maximal intervention licenses no claim
about any smaller one.*

## 3. What the mesh does not embody

Mesh doctrine already carries the *kind* half of matching, twice:

- "A gate you have not seen FAIL is not a gate" (CLAUDE.md) — the manipulation requirement itself.
- `a-mutant-can-go-red-for-the-wrong-reason` — read the failure MESSAGE; the red must be the defect.
- `a-two-arm-gate-against-a-live-world-measures-the-world` — this *is* fat-handedness, named
  independently: "The arms differed in TWO things: the variable under test AND the world."

The **degree** half is absent. Mesh gates manipulate at the ENDS — delete the line, comment the call,
poison the binary, empty the fixture — and assert a boolean flip. Nothing anywhere asks the matching
question in the other direction: **of the changes in the subject that the detector does NOT register,
how large are they?** No mesh detector publishes the smallest effect it can detect. Grep across
`scripts/` for effect-size/power/detection-threshold language returns two files
(`mesh-algedonic`, `mesh-criticality`) and neither publishes a floor.

## 4. The application (one file): `scripts/mesh-cooscillate`

`mesh-cooscillate` is the right subject because its detection floor is not a matter of opinion — it is
fully determined by the tool's own gate, and it is **not the floor the file declares**.

The file declares `MIN_R=0.6  # |Pearson r| on deltas must exceed this` and then imposes a
Bonferroni-corrected significance gate, `fisher_p(r,nd) * ntests <= ALPHA`. Inverting the second for
the smallest clearable |r| at the tool's own `MIN_OVERLAP=8`, against the family sizes this file's own
header records from real runs (19 / 37 / 104 / 231 / 331 pairs):

| nd | m=1 | m=19 | m=37 | m=104 | m=231 | m=331 |
|---:|----:|-----:|-----:|------:|------:|------:|
|  8 |0.705|0.873 |0.892 |0.916  |0.929  |0.935  |
| 14 |0.531|0.720 |0.747 |0.783  |0.806  |0.815  |
| 30 |0.360|0.522 |0.549 |0.586  |0.612  |0.623  |

**`MIN_R = 0.6` is decorative for every window this tool actually runs on.** The significance gate
binds at |r| ≈ 0.81–0.93 for the 14–19 Δ-step windows the header quotes from live findings; the
declared floor only becomes the operative one at nd ≳ 30. Every genuine coupling between the declared
floor and the real one is invisible, and no line anywhere said so. Same family as the mesh's own
*a declared pref is not the FIB*, one ring out into statistics.

**Honest limit on the critique.** This harness is not a two-point curve — it already plants r = 1.0
(must emit), "Coincid" at r ≈ 0.70 (must be dropped as winner's-curse), and empty (nothing). Three
points, each a real leg. What none of them does is convert that into a **published threshold**: the
0.70 leg treats the blind band as correct behaviour and never names its width.

### What was added (report-only; the detection path is untouched)

**`mesh-cooscillate --sensitivity`** — publishes the OPERATIVE floor for the live window, computed by
bisecting **this file's own `fisher_p`**, not by quoting a constant, so if the p-model changes the
published floor follows it (the mesh's "the CLAIM is the gate, re-derived, never quoted" rule). It
never reaches PASS B, writes no state, emits no idea, and renders `unmeasured` + exit 2 on a window
with nothing tested — never a plausible constant.

Live artifact, this node, 2026-08-24T20:0xZ:

```
[coosc-sensitivity] ntests=9 alpha=0.0500 declared MIN_R=0.600 window=48h min-overlap=8
  nd=8    r_min=0.845   binding=ALPHA  pairs=6
  nd=12   r_min=0.728   binding=ALPHA  pairs=3
operative-floor: |r| >= 0.845 at the median tested nd=8 (declared 0.600) — blind band 0.600..0.845
blind-band pairs this window: 0/9 measured |r| inside the band — real co-movement this gate can never emit
binding-gate: ALPHA on 9/9 tested pairs, MIN_R on 0/9
```

**A graded `--test` leg** — the matching condition operationalized. Three fixtures on ONE pair at
nd = 8, ntests = 1, read by the tool's own Pearson at 0.66 / 0.80 / 0.95, straddling the floor
`--sensitivity` publishes for exactly that (nd, ntests): r_min = 0.705, so ALPHA binds and **0.66 sits
inside the blind band while clearing the declared MIN_R = 0.6**. The assertion is the match itself:
emit **iff** |r| ≥ the published floor. Plus a vacuity guard (the band must be non-empty), a
falsifiability arm (with ALPHA disabled the 0.66 fixture must resurface, proving it is the
significance gate that silences it and not some other filter), and the honest-empty arm.

### Seen RED, then green

| mutant | result |
|---|---|
| `_rmin` returns `MIN_R` (publish the declared floor as operative) | RED — *"published floor 0.600 is not inside (MIN_R,1) — the graded fixtures cannot straddle it"* |
| `_rmin` returns `hi*1.15` (floor above the real flip) | RED — *"\|r\|=0.80 is below the published floor 0.810 yet a finding was emitted — the published floor under-states the gate"* |
| empty corpus exits 0 instead of 2 | RED — *"an unmeasurable floor must not render as a number"* |

Full `--test` green on HEAD (rc 0).

**One mutant is masked, stated rather than hidden:** dropping the Bonferroni gate from PASS B
(`if pcorr>ALPHA: continue`) is caught by the pre-existing winner's-curse leg first, so the new
blind-band leg never gets to speak (`a-red-gate-hides-every-gate-after-it`). Driven separately
against the 0.66 fixture, the new leg's subject does separate them: HEAD emits 0 findings, the mutant
emits 1.

### Not done

Deployment. The change is uncommitted in `scripts/` per the task; deploying to `~/.local/bin` ahead of
a commit would put the node ahead of the genome and read as drift to `mesh-sync-tools`.
`--sensitivity` is on-demand and deliberately unwired — no cadence, no reflex.

## Sources

- [Liao, *Critical 4E Cognitive Science*, Philosophy Compass 2026](https://compass.onlinelibrary.wiley.com/doi/10.1111/phc3.70075?af=R)
- [Kirchhoff & Kiverstein, *Defending the use of the mutual manipulability criterion in the extended cognition debate*, Front. Psychol. 13:1043747, 2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1043747/full)
- [Craver, Glennan & Povich, *Constitutive relevance and mutual manipulability revisited*, Synthese 199:8797–8827, 2021](https://doi.org/10.1007/s11229-021-03183-8)
- [Coraci, *Extended cognition, mutual manipulability, and the relevance of scientific evidence: a reformulation of the matching criterion*, Synthese 2025](https://link.springer.com/article/10.1007/s11229-025-05067-7)
- [Krickel, *Extended Cognition, The New Mechanists' Mutual Manipulability Criterion, and The Challenge of Trivial Extendedness*](https://philarchive.org/rec/KRIECT)
- [Ward, *What Is Enactivism?*, Adaptive Behavior 2026](https://journals.sagepub.com/doi/10.1177/10597123261450094) — read; the organicism/informationalism axis and its "lumping" critique did not yield a transferable mechanism this pass.
