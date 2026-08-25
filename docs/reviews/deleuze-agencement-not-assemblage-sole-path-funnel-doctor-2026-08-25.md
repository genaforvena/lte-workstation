# Deleuze & Guattari — live review: AGENCEMENT IS NOT ASSEMBLAGE (the arrangement, not the collection)

**Area:** Deleuze & Guattari — assemblage / rhizome / the machinic. Angle as commissioned: a
foundational idea we may have **MISread or applied too loosely**.
**Date:** 2026-08-25. **Window:** genome (mesh-home).
**Status:** landed, uncommitted in the tree (steward lands).
**Tools:** `scripts/mesh-doctor` — new sole-path funnel detector (report-only section) ·
`scripts/mesh-soundscape` — the first declaration.

---

## I. Where this area is live, and what I read

Searched 2026-08-25 (WebSearch ×5, WebFetch ×3). This mesh has **17 prior D&G reviews**
(`docs/reviews/deleuze-*`, `rhizome-*`), so most of the obvious ground is taken: asignifying rupture,
relations of exteriority, DeLanda's coding/decoding, deterritorialization coefficients, disjunctive
synthesis, double articulation, conjugation vs connection, faciality, rhythm-is-not-meter,
transversality, the twin axes, the machinic phylum, order-words, smooth/striated. I went looking for
the one thing that is *upstream* of all of them.

| Work | Where | Why not this |
|---|---|---|
| Genosko, "Black Holes of Politics: Resonances of Microfascism" | *La Deleuziana* n.5 (ISSN 2421-3098), PDF re-posted 2025-03; **text is 2017** | Read in full (`pdftotext`). Resonance-of-micro-black-holes is a real mechanism, but co-failure clustering already landed here 2026-08-18 (`autopoiesis-bunch-lifeness-…-cofail-reflex-health`). Also: dated 2017, and I will not dress it as current. |
| Serrano, Kevari & Narayan, "A Multi-Agent Rhizomatic Pipeline for Non-Linear Literature Analysis" | arXiv:2603.28336v2, 2026 | Genuinely current and genuinely multi-agent, but the body gives no algorithm, stopping rule or data structure — rhizome as a *description* of parallel agents. No transferable mechanism. |
| Kleinherenbrink, "Territory and Ritornello" | *Deleuze Studies* 9(2), 2015 | The refrain's three moments. Overlaps our `deleuze-guattari-rhythm-is-not-meter-…-2026-08-19`. |
| **Phillips, "Agencement/Assemblage"** | ***Theory, Culture & Society* 23(2–3): 108–109, 2006** — and restated continuously since, incl. **Nail, "What is an Assemblage?", *SubStance* 46(1): 21–37, 2017**, and still argued in current secondary literature and at the 2024 D&G Studies conference | **Landed here.** |

**Honest dating.** The argument is *not* a 2026 result. It is a 2006 correction that the field keeps
re-issuing because the reception keeps ignoring it — which is itself the reason it qualifies under the
commissioned angle ("misread or applied too loosely"). I am not going to invent a 2026 paper to dress
it up. What is live is the *ongoing* restatement; what is old is the finding.

## II. The concept, and why it is a misread we personally committed

D&G's word is **agencement**, from *agencer* — "to arrange, to lay out, to piece together". Nail's
gloss, which the translation debate has converged on:

> **agencement** = "arrangement or layout of **heterogeneous elements**"
> **assemblage** = "gathering of things together into **unities**", "collection, set, a set of parts"

The two words come from different roots. *Agencement* is not a static term; it names **the process of
arranging** — the agency is in the word. English "assemblage" names **the parts, gathered**. The
operational difference is sharp and testable:

- **Swap a member, and the agencement can be untouched.**
- **Keep every member, re-route one call, and the agencement is gone.**

An assemblage is individuated by its **membership**. An agencement is individuated by its
**arrangement**. Only the second is a capability.

**We committed the misread, in writing.** Our own prior review is
`deleuze-assemblage-relations-of-exteriority-sensorium-2026-07-28.md` — the DeLanda reading, which is
precisely the downstream product the *agencement* critics identify: parts with exterior relations,
i.e. a set. And it is not only a filing error. **Every capability this mesh declares, it declares as a
membership list**: the card's `minds:`/`senses:` lines, `MESH_MIND_CHANNELS`, `MESH_RETIRED_CHANNELS`,
the tool catalog, every allowlist.

Meanwhile the structures that actually carry our capabilities are **arrangements**, and every one of
them lives as **prose**:

| the rule, as written | where it lives | what checks it |
|---|---|---|
| "`mesh-voice-say` — THE clone-synth primitive; every speech organ synthesizes through it" | CLAUDE.md | nothing |
| "`mesh-soundscape --measure` — the one measure tract; never add a second librosa analyzer" | CLAUDE.md | nothing |
| "`mesh-room-music` owns the grind invocation" | CLAUDE.md | nothing |
| "Landing is `mesh-land`, never a bare push from a subagent or a worktree" | charter/genome | nothing |
| every frame passes `mesh-cam-lock` | implied by the frames budget | nothing |

A grep of all 683 tools for any machine-checkable exclusivity declaration returns **zero**. Seven
files contain the phrase "sole caller"/"only caller" — all seven are comments.

## III. What was built

**`scripts/mesh-doctor` — the sole-path funnel detector** (report-only section, `solepath_scan` +
one `hdr` block). A tool may now DECLARE the funnel it is, in a header line: the marker word, a short
NAME, and an extended regex identifying the primitive it fronts. The scan reads the rest of the corpus
for lines matching that regex; those are **bypasses**, and each is named with its `file:line`.

Three things it must get right, each a way this class of gate goes quietly wrong, each held by a leg
that goes red under mutation:

1. **A comment is not a call site.** On the live tree, **5 of the 8 files mentioning `librosa` mention
   it only to recite the one-measure-tract rule approvingly**. Counting them would bury the single
   real violation under five citations of the rule it violates. *(Mutation: drop the comment filter →
   the leg fails.)*
2. **The declarer is not its own violation.** *(Mutation: drop the self-exclusion → the leg fails.)*
3. **Zero declarations is not all-clear.** A pattern-less declaration reads MALFORMED, and a corpus
   declaring nothing emits nothing, so the caller renders "unmeasured" rather than a pass.

A fourth, learned from the self-grep detector one screen up in the same file: **the marker is spliced
from a variable in the fixtures and never written at the head of a comment line in `mesh-doctor`** —
otherwise doctor's own explanatory prose becomes a live declaration.

**`scripts/mesh-soundscape` — the first declaration**, seeded on the rule CLAUDE.md already states.
The pattern covers librosa's *analysis* surface (`load|feature|beat|onset|stft|yin|pyin|effects|
decompose|util`) and deliberately excludes `resample`: `mesh-voice-print` resamples for resemblyzer
and measures nothing, and a funnel that swallows its neighbours is not a funnel.

## IV. The live finding, first run

```
== sole-path funnels (the ARRANGEMENT, not the membership list) ==
  WARN 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is
  broken: librosa-analysis<- mesh-song-verify:94 :95 :102 :109 :111 :114
```

`mesh-song-verify` (born 2026-07-24, **after** the rule) is a second librosa analyzer: it calls
`librosa.load` ×2, `chroma_stft`, `rms`, `spectral_rolloff`, `beat_track` — and its axes (rhythm as
beats/s, brightness as rolloff) **overlap `mesh-soundscape --measure`'s own**, which is exactly the
drift the rule forbade. Zero false positives; the five reciting files and `mesh-voice-print`'s
resample are correctly untouched.

**This is not a verdict that the bypass is wrong.** `mesh-song-verify` does a pairwise
source-vs-candidate comparison that `--measure` does not offer, so the honest options are to extend
the tract or to grant an exemption — either way by a hand that has read the line. The finding is that
**for thirty-two days nothing could see it**, while five tools recited the rule in their comments.
The prose proliferated; the arrangement broke. That is the difference between an assemblage and an
agencement, measured.

## V. What was deliberately NOT declared

`mesh-cam-lock` is the obvious second subject — the frames axis of `mesh-budget` is a declared LOWER
BOUND *precisely because* that funnel is unenforced (cam-watch, the iMac cam and the phone cams shoot
around it). But `mesh-bruno-watch` legitimately takes the lock and *then* calls `fswebcam` directly, so
a naive pattern would name a compliant holder as a bypass. A standing half-wrong accusation is worse
than an undeclared funnel, so it is left undeclared, deliberately, and named here as the next subject.

## VI. Artifacts

- `mesh-doctor --test` PASS (summary clause added naming all five legs); two mutations driven red.
- `mesh-soundscape --test` PASS (comment-only change, verified not vacuously).
- Deployed byte-identical; live `mesh-doctor` renders the WARN above.

## VII. Sources

- Phillips, J. (2006) "Agencement/Assemblage", *Theory, Culture & Society* 23(2–3): 108–109.
- Nail, T. (2017) "What is an Assemblage?", *SubStance* 46(1): 21–37.
- <https://reflectionsonresearch.com/assemblage-theory-agencement-assemblage/> (Nail gloss, quoted)
- <https://en.wikipedia.org/wiki/Assemblage_(philosophy)>
- Genosko, G., "Black Holes of Politics: Resonances of Microfascism", *La Deleuziana* n.5 —
  <https://ladeleuziana.org/wp-content/uploads/2025/03/04-en-Genosko-Resonance_MicroFascism.pdf> (read, not used)
- Serrano, Kevari & Narayan (2026), arXiv:2603.28336 — <https://arxiv.org/pdf/2603.28336> (read, not used)
- Kleinherenbrink, A. (2015) "Territory and Ritornello", *Deleuze Studies* 9(2) (surveyed, not used)
