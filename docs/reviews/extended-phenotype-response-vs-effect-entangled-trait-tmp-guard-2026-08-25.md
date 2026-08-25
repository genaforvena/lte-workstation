# The same trait has TWO functions, and the residue axis was only ever the first one

**Live review, 2026-08-25 — niche construction & the extended phenotype, from the angle the task
asked for: a RECENT result (2023-2026) and what it says we are not measuring.**
Landed in `scripts/mesh-tmp-guard` (uncommitted; steward lands from the tree).

## What was already ours (checked before searching, so the review could not re-land)

Twenty prior reviews sit in this area. Enumerated first, because the point of the lane is to land
somewhere we have not been:

| embodied | where |
|---|---|
| Fogarty & Wade — NC as a modified breeder's equation, realized h² > 1 | `mesh-vitality`, `mesh-forage` |
| Odling-Smee/Laland/Feldman — inceptive vs counteractive NC | `mesh-ideate:303` |
| Kurtz — experimental **removal** of niche construction (the ablation control) | `mesh-ideate:273` |
| Ayres et al. — home-field advantage as an INTERACTION, not a gap | `mesh-promises --homefield` |
| Albertson et al. 2024 — **ghost** legacies: a dead engineer's artifact still steering | `mesh-reflex-health` |
| Wade & Sultan — negative NC / inter-scale conflict / terminator niche | `mesh-forage:132` |
| NC3 mechanism attribution (construction vs choice vs conformance) | `mesh-forage` `nc3()` |
| by-product null: an adaptive verdict needs the SIGN of the fitness change | `mesh-forage` |
| driftability / the variance channel | `mesh-forage` |
| contemporaneous reference class for a legacy claim | `mesh-reflex-health` `ow_cohort_clause()` |
| Lee/Flack/Krakauer 2024 — sublinear optimal memory, τ_e, outsourced memory | `mesh-situation` |
| mere recurrence vs form transmission | `mesh-knowledge-sync` |
| model collapse / provenance ratio | `mesh-knowledge-sync` |
| fecundity vs mortality cost of construction | `mesh-resource-guard` |
| arms-race asymmetry / the rare-enemy effect | `mesh-tg-roz` |

Every one of those asks a question about the **construction**: who built it, whether it helps, what
sign the fitness change has, how long it outlives the builder, whether the form transmits. **Not one
of them says that a single trait has two DIFFERENT functions that must be measured separately.** That
is the shape of the gap, and it is exactly what the 2025 result is about.

## The find

**Díaz, S. (2025). "Plant functional traits and the entangled phenotype." *Functional Ecology*
39(5):1144–1159. doi:10.1111/1365-2435.70017.**
Found via a live search of 2025-2026 work in this area; the paper is the current statement of the
trait-based-ecology↔evolutionary-biology bridge and is explicitly framed against niche construction
theory and the extended phenotype.

Its operative move is a decomposition:

- a **specific response function (SRF)** — the organism's ability to maintain or enhance its quantity
  *in response to* a specified change in its environment;
- a **specific effect function (SEF)** — the organism's *per-unit capacity to influence* a
  community- or ecosystem-level property.

And the claim that makes it a finding rather than a vocabulary: **the same trait carries both, and
they are different functions of it.** Díaz's worked case is leaf toughness — it sets leaf longevity
(response) *and* herbivore nutritional value and litter decomposability (effect), and knowing its
value on one axis tells you nothing about its value on the other. Traits therefore cannot be sorted
into "response traits" and "effect traits"; they are **entangled**. The paper's second half extends
this across organisms: coexisting species' extended phenotypes interweave into a **joint multispecies
extended phenotype** — the rhizosphere is co-constructed by plant chemistry, fungi and bacteria and
owned by none of them — so attribution to a single constructor is a category error, not a hard
measurement.

What that gives us, stated as an engineering rule: **an artifact validated on its response function
is unvalidated on its effect function, and the two can have opposite signs.** A trait can be an
excellent response and a destructive effect, and no amount of testing the first will surface the
second, because they are not the same quantity.

## Where it bites here: `scripts/mesh-tmp-guard`

`mesh-tmp-guard` owns the node's temp directories — the mesh's clearest **joint extended phenotype**:
~dozens of tools write there, every mind's work passes through it, and no tool owns it. It is the
rhizosphere of this node.

**Every axis the guard had was a STOCK.** `entries`, `swept`, `freed_mb`, `other-owner`, `use%`,
`residue` — all of them measure what is *sitting* in the temp dirs at the instant of the sweep. That
is the response side of mesh temp usage: what accumulates when cleanup fails. The effect side —
**how many bytes the mesh pushes THROUGH the shared filesystem** — is a different function of the
same behaviour, and it is the one that wears the device.

The two came apart on this node, measured, this morning. `mesh-spend --tokens` copied a 966.5 MiB
`opencode.db` into TMPDIR and `rmtree`'d it inside the same call, thirteen times in one 300s window:
**12.7 GiB through /tmp on the boot NVMe, and ZERO survivors.** Every stock axis above read clean the
whole time. `mesh-tmp-guard` was structurally green while the mesh's largest disk writer ran under
it, and it could not have been otherwise — a residue axis cannot see a flow that cleans up after
itself, however large the flow is. Leaf toughness, exactly: high value on the response axis (nothing
strands, the traps work, the sweeper is idle) and catastrophic on the effect axis (92% of
`cron.service`'s lifetime writes), with the tool holding an instrument for only the first.

This is the twin of [[a-per-call-file-snapshot-is-invisible-to-a-growing-file-hunt]] one ring out:
that memory says a *hunt* keyed on file growth is blind to transient bytes. Díaz says why the blind
spot is structural rather than an oversight — **response and effect are different functions, and we
built the tool with one of them.**

## What landed

An **EFFECT axis** in `scripts/mesh-tmp-guard`, published beside the stock axes rather than folded
into them:

- `dev_of()` / `dev_written()` / `cron_written()` — the flux is a **monotonic kernel accumulator
  delta'd across the interval**, never an instantaneous read: sectors-written for the block device
  actually backing the temp dir (whole-node, so mind panes and hand-run tools count too, not only
  cron), plus `cron.service`'s cgroup `wbytes` **for that same device** as the attributed share.
  Both unprivileged here. The device is named in the field, so the number can never be read as a
  claim about a disk the temp dir does not live on — the founding mistake of this tool's own
  incident.
- A new `flux=` field in the state line, the `--json`, and the dry-run render:
  `flux=<MB/h> dev=<kname> cron=<MB/h> window=<s>s swept_share=<pct>%`.
- **`swept_share`** is the unit-free half and the review's claim stated as a number the tool computes
  about itself: the bytes this sweep reclaimed as a fraction of the bytes that went through the
  device in the same window. In the incident above it is ~0.
- **Every unreadable window renders `na` WITH ITS REASON, never 0** — `first-sample`,
  `device-changed`, `counter-reset`, `no-window`, `not-block-backed`, `device-unreadable`. 0 is the
  *healthy* reading on this axis, so a broken read must not be able to wear it.
- **No band, deliberately.** The tool has never measured flux, so there is no corpus to calibrate a
  threshold against, and a constant invented here is precisely the assumed-0..1 axis
  [[calibrate-a-derived-axis-against-the-live-corpus]] forbids. `~/.mesh/tmp-guard-flux.log`
  accumulates the samples a real band can later be derived from; `swept_share` needs no constant and
  ships working today.
- **`--dry-run` does not advance the cursor.** It would otherwise consume the next real sweep's
  window and blind exactly the axis it was asked to report on.

### Artifacts

Live, against the real kernel — 1.5 GiB written between two sweeps of a sandboxed temp dir:

```
[tmp-guard-normal] NORMAL|dirs=1|entries=0|swept=0|freed_mb=0|other-owner=0|use=17% on <sb>/tmp|
  flux=416519.4MB/h dev=dm-0 cron=0.0MB/h window=13s swept_share=0.000%|0 entries / 0MB, writable
2026-08-25T11:37:58Z dev=dm-0 dev_mb_h=416519.4 cron_mb_h=0.0 window_s=13
  dev_delta_b=1577160704 freed_b=0 swept_share_pct=0.000
```

`dev_delta_b=1577160704` against a 1572864000-byte `dd` — the axis is reading the real device. The
verdict is `NORMAL` with `swept_share=0.000%`: the incident's signature, reproduced, on a tool that
until today had no field it could appear in.

Five `--test` legs, driven RED first in both directions:

- dropping the backwards-counter guard →
  `FAIL flux: a backwards counter must be na(counter-reset), got: … flux=-14393.0MB/h …`
  (a *negative rate* printed as a number — the failure the guard exists for);
- letting `--dry-run` save a sample →
  `FAIL flux: --dry-run advanced the flux cursor — it ate the next real sweep's window`.

The rate leg recomputes its expectation from the tool's **own published window**, read out of the
ledger **by key rather than by column**, so it cannot pass on a hardcoded string and cannot be
broken by a field moving.

## One thing this review did NOT fix, and is reporting instead

`mesh-tmp-guard --test` was **already RED on this node before this change**, for an unrelated reason,
and stays RED after it: `FAIL unwind-scan: 12 python temp producer(s) have a real unwind point but no
SIGTERM handler` — `mesh-ask-notify mesh-cron-catchup mesh-job-answers mesh-job-apply mesh-job-facts
mesh-job-scan-getmatch mesh-safe-open mesh-sense-map mesh-voice-clone-daemon mesh-voice-verb
mesh-wifi-crossval mesh-witness-analyze`. Verified pre-existing by running `git show
HEAD:scripts/mesh-tmp-guard --test`, which fails identically. Their `finally:` cleanup is decorative
under the SIGTERM every cron `timeout` delivers. Out of scope here; named so it is not mistaken for
collateral, and so a red suite is not read as this change's.

## The half not taken

Díaz's **joint multispecies extended phenotype** — an artifact co-constructed by many writers and
owned by none, where single-constructor attribution is a category error — is the other half of the
paper and is only partly ours (`mesh-fswriter` does fanotify attribution;
[[writer-redundancy-blinds-mtime-liveness]] and
[[a-whole-file-checksum-on-a-shared-log-races-every-other-writer]] know the multi-writer hazard).
What is missing is the *positive* statement: for a shared artifact, the honest unit of analysis is
the joint construction, not the writer. Left as a lead rather than claimed.

## Sources

- [Díaz, S. (2025) "Plant functional traits and the entangled phenotype", *Functional Ecology* 39(5):1144–1159](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2435.70017)
- [Experimental Removal of Niche Construction Alters the Pace and Mechanisms of Resistance Evolution (bioRxiv 2025.03.27.645637)](https://www.biorxiv.org/content/10.1101/2025.03.27.645637.full.pdf) — checked and NOT used: removal/ablation control is already ours (`mesh-ideate:273`)
- [Niche construction in quantitative traits: heritability and response to selection, *Proc. R. Soc. B* 289(1976)](https://royalsocietypublishing.org/rspb/article/289/1976/20220401/79419/Niche-construction-in-quantitative-traits) — checked and NOT used: realized h² is already ours (`mesh-vitality`)
- [Niche Construction — Open Encyclopedia of Cognitive Science (MIT)](https://oecs.mit.edu/pub/xyn6l8i3/)
