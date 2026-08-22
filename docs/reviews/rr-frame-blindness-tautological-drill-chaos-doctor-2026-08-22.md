# The chaos suite that verifies a copy of the detector: frame coverage, and a drill that cannot be wrong

**Live review, 2026-08-22 — relevance realization & the frame problem (Vervaeke), from the angle the
task asked for: a CROSS-DOMAIN transfer into a distributed sensor mesh.**
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-chaos-doctor` — assigned by coin at p=0.20, drawn uniformly from the
lane's 567 never-reviewed tools. Not chosen by me and not chosen by the lane.
Landed in `scripts/mesh-chaos-doctor` (`--frame`, read-only; uncommitted — steward lands from the tree).

## What was already ours

Eleven prior RR landings: cognitive scope · cognitive tempering · diametric autism/psychosis ·
ecological rationality (footholds) · efficiency↔resiliency · **the ramification problem**
(`mesh-doctor`, 2026-08-17) · insight/reframe-at-impasse · opponent processing · the prior dilemma ·
**the qualification problem** (`mesh-organ`) · routines/orientation worlds.

Both frame-problem landings are about the *subject's* frame: what a change ramifies into
(ramification), what preconditions an action silently assumes (qualification). Neither asks the
reflexive question, and nothing in the corpus does: **what is the frame of the tool doing the
checking, and can that frame be wrong?**

## The find

**Andersen, B. P., Miller, M. & Vervaeke, J., "Predictive processing and relevance realization:
exploring convergent solutions to the frame problem," *Phenomenology and the Cognitive Sciences*,
doi:[10.1007/s11097-022-09850-6](https://link.springer.com/article/10.1007/s11097-022-09850-6)**
([PhilPapers](https://philpapers.org/rec/ANDPPA-11), [Monash](https://research.monash.edu/en/publications/predictive-processing-and-relevance-realization-exploring-converg/)),
found by live search 2026-08-22 alongside the [Utrecht thesis on RR as a solution to the frame
problem](https://studenttheses.uu.nl/bitstream/handle/20.500.12932/42973/Thesis%20final.pdf?sequence=1)
and Irving, Vervaeke & Ferraro on self-organising criticality as RR's implementation.

The load-bearing claim, and the one that transfers: **relevance realization cannot be an algorithm
over a fixed feature set, because selecting the features IS the problem being solved.** An agent that
"zeroes in on relevant aspects and intelligently ignores the vast majority of the world" has to do so
through a self-organising, opponent-processed dynamics that **can be wrong and re-tune** — any frame
fixed in advance is, by construction, blind to what it excluded, and its blindness is invisible from
inside it.

## The transfer: a chaos suite IS a frame

`mesh-chaos-doctor`'s whole purpose is the doctrine "a detector you have not seen fail is faith, not
verification". It injects failures and proves `mesh-doctor` catches them. But the suite is itself
six hand-picked failure classes standing in for everything the subject claims to catch — a fixed
frame — and it had neither of the two things a frame needs to be able to be wrong:

**1. It never measured its coverage.** `mesh-doctor` declares **19** check classes (its own `hdr`
sections). The suite drills **5**. Nobody had counted, and the 14 undrilled classes were not merely
uncovered — they were *unnamed*, and an unnamed gap reads as no gap.

**2. Five of six drills re-implement the detector and then test their own copy.** The suite says so
in its own comments — *"Run the same topology-clean check logic from mesh-doctor inline"*, *"Inline
inverse-orphan logic"* — and DRILL 4 defines a local `load_offset()` that is a copy of
`mesh-textin`'s. DRILL 1 runs `bash -n` directly; DRILL 3 runs the injected tool's own `--test`. Only
DRILL 2 actually invokes `mesh-doctor`, and on this node it SKIPs. **The real detector could be
deleted and this suite would print DETECTED six times.** A drill that cannot be wrong is not evidence
— it is the frame confirming itself, which is precisely the failure RR names.

## What landed

`mesh-chaos-doctor --frame` — read-only, no injections of its own beyond the suite it re-runs:

```
mesh-chaos-doctor --frame — the suite's own frame, measured
  subject: /home/mesh-home/lte-workstation/scripts/mesh-doctor
  coverage: 5/19 declared check class(es) drilled (26%)
  ✓ every declared drill target is still a live class in the subject
  uncovered classes (NAMED — an unnamed gap reads as no gap):
    · egress integrity (clean router-LAN, no SPOF)
    · reflexes RUNNING CLEAN (UP-but-broken: errors in logs)
    · hang risks (mesh-* SSH a peer with NO ConnectTimeout)
    · self-asserting gates (a self-grep whose pattern matches its own line)
    · absence rendered as a NEGATIVE READING
    · interpretant check (state producers with no reader…)
    … 14 in total
  tautology drive (suite re-run against a mesh-doctor that detects nothing):
    SUBJECT-FREE broken-tool → parse-check
    SUBJECT-FREE broken-smoke → smoke-check
    SUBJECT-FREE textin-replay → missing offset returns file size (no replay)
    SUBJECT-FREE textin-replay → stale offset clamped (no stale-tail replay)
    SUBJECT-FREE topology-leak → IP 100.64.0.1 detected
    SUBJECT-FREE inverse-orphan → … wired but ungenomed
  tautological=6 of the drills that fired
```

- **Tautology is established by DRIVING, never by reading the source.** The suite is re-run with a
  `mesh-doctor` that detects nothing; every drill still reporting DETECTED proved something about a
  copy living in this file. 6 of 6 firing drills.
- **Each drill DECLARES the subject class it stands for**, and `--frame` checks that class still
  exists — a drill aimed at a renamed or deleted check is a reflex tending a target that is gone.
- **The stub is prepended AFTER the script's own `export PATH`**, because a stub dir handed in by a
  caller would otherwise lose the PATH race to the real `~/.local/bin` — the documented
  poisoned-binary trap. `MESH_CHAOS_SUBJECT_STUB` is set only by `--frame`'s own re-invocation and
  can only ever make the subject *weaker*, so a production run that never sets it cannot be made
  falsely green by it.

## Verification

`--test` drives four legs: `--frame` must report a coverage fraction over the subject's real class
list; it must NAME the uncovered classes; it must run a tautology drive that reports a count; and —
the leg that matters most — a hidden `--which-subject` probe must show the child resolving
`mesh-doctor` **inside the stub dir**. That last one exists because the tautology COUNT cannot detect
a broken stub here: these drills never call the subject at all, so they print DETECTED either way.

Driven red four ways, restored green each time:

| mutation | result |
|---|---|
| remove the stub prepend (stub loses the PATH race) | `FAIL (the stubbed subject LOST the PATH race — resolved '/home/mesh-home/.local/bin/mesh-doctor' … the tautology drive would be silently measuring the REAL mesh-doctor)` |
| stop naming the uncovered classes | `FAIL (--frame does not name its uncovered classes)` |
| drop the coverage fraction | `FAIL (--frame reports no coverage fraction over the subject's classes)` |
| drop the tautology count | `FAIL (--frame ran no tautology drive — a drill that tests its own copy stays invisible)` |

`--frame` **reports; it does not fix.** The 14 uncovered classes and the 6 subject-free drills are now
visible and countable, which is the whole content of the transfer: a frame that publishes its own
coverage can be wrong, and one that does not cannot.

## Sources

- [Andersen, Miller & Vervaeke, *Phenomenology and the Cognitive Sciences*, doi:10.1007/s11097-022-09850-6](https://link.springer.com/article/10.1007/s11097-022-09850-6) · [PhilPapers](https://philpapers.org/rec/ANDPPA-11)
- [Relevance Realization as a Solution to the Frame Problem (Utrecht thesis)](https://studenttheses.uu.nl/bitstream/handle/20.500.12932/42973/Thesis%20final.pdf?sequence=1)
- [Relevance Realization and the Neurodynamics and Neuroconnectivity of General Intelligence](https://www.researchgate.net/publication/299812171_Relevance_Realization_and_the_Neurodynamics_and_Neuroconnectivity_of_General_Intelligence)
