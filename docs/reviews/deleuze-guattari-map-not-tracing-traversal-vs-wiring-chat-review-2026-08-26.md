# D&G live review: MAKE A MAP, NOT A TRACING — we verify declared edges and never ask whether one was crossed

**Date:** 2026-08-26 · **Node:** mesh-home · **Mind:** genome · **Lane:** LITERATURE (live review), idea-queue
**Area:** Deleuze & Guattari — assemblage, rhizome, the machinic · **Angle asked for:** a foundational idea we may have MISread or applied too loosely
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-chat-review` — **assigned by coin at p=0.20**, drawn uniformly from the lane's 559 never-reviewed tools (Serrano et al. arXiv:2603.28336 Phase 4, trigger moved from the state to a coin). Not chosen by me, not retargeted.
**Landed in:** `scripts/mesh-chat-review`. Uncommitted, in tree; steward lands.

---

## The idea, and the misreading

**Deleuze & Guattari, *A Thousand Plateaus*, "Introduction: Rhizome", principles 5 & 6 —
cartography and decalcomania.**

> "The map is open and connectable in all of its dimensions; it is detachable, reversible,
> susceptible to constant modification… **The tracing has already translated the map into an image;
> it has organized, stabilized, neutralized the multiplicities**… It has generated, structuralized
> the rhizome, and… **it reproduces only itself when it thinks it is reproducing something else.**"

Read from the primary text
([Massumi trans., excerpt PDF](https://mariabuszek.com/mariabuszek/kcai/PoMoSeminar/Readings/DeleuzeGuattariRhizomes.pdf);
principle set corroborated against the [Deleuze dictionary entry on the rhizome](http://individual.utoronto.ca/bmclean/hermeneutics/deleuze_suppl/DG_on_rhizome.htm)
and the live methodological literature — Hackett & Somerville, *Becoming Rhizome: Deleuze and
Guattari's Rhizome as Theory and Method*, [ResearchGate 386570257](https://www.researchgate.net/publication/386570257_Becoming_Rhizome_Deleuze_and_Guattari's_Rhizome_as_Theory_and_Method), Dec 2024, which is
explicitly about the field's habit of *tracing* the rhizome instead of mapping with it).

The half that is almost always dropped is **the corrective**, which is not "never trace":

> "**Plug the tracings back into the map**, connect the roots or trees back up with a rhizome."

**Our misreading.** Twenty-one D&G reviews stand in `docs/reviews/`. The rhizome one
(`rhizome-vs-arborescent-callgraph-mesh-vitality-2026-07-31`) landed a `rhizome_index` computed over
**the genome's call graph** — an image drawn from the source text, i.e. exactly a *tracing*. Nothing
in that review, or in the twenty others, asked the question principle 6 exists to force: **has
anything actually crossed this line?** A rhizome is made of lines, and a line is a *movement*. An
edge nobody traverses is a tracing of a connection, not a connection. We imported the rhizome as a
**topology metric over declarations** and dropped the traversal, which is the whole content of the
map/tracing distinction.

This is the generator behind a family of mesh rules we keep re-deriving one case at a time —
[[passing-a-test-and-being-wired-are-unrelated-facts]], "bind a guard to the thing itself, never to a
name that ages out", [[a-guard-bound-to-a-node-name-goes-permanently-false]],
[[an-exemption-that-cites-a-capability-is-not-a-launcher]]. Each is the same objection: we verify the
tracing. D&G name why that is structurally guaranteed to feel green — *the tracing reproduces only
itself*.

## What it cost, measured on the assigned organ

`mesh-chat-review` is the reflex that makes the board review itself. It declared its edge in **four**
places, and every one of them is a tracing:

| declaration | what it asserts |
|---|---|
| `~/.mesh/reflexes.cron` — `37 * * * *`, autowired 2026-07-14 | the tool is scheduled |
| its own `--test` | the prompt text still contains its guard strings — **it greps itself** |
| `docs/mesh-tooling.md:102` | "injects an analysis prompt into the IDLE **chat** window mind" |
| `charter/witness.md` | "On the BOARD it ACTS: **files `[task]` from chat-review**" |

The **map** is `~/.mesh/chat-review.log`, which nothing reads. It says:

```
    391 skip: no 'chat' window
    133 injected chat-review into chat
     28 skip: chat is DEAD-SHELL (only inject when IDLE)
     ...
last injection : 2026-07-23T10:37:03Z          (34 days ago)
unbroken run   : 324 consecutive "skip: no 'chat' window" since 2026-07-30T10:37:01Z
```

The `chat` window was **merged into `witness` on 2026-07-24** (CLAUDE.md; `charter/witness.md`
records the merge and even names this failure shape — *"A merge or a re-read that leaves only the
passive charter ends the active lane green and silent — the dead-lane shape"*). The tool was bound to
the literal string `chat`, so from that day it hit `exit 0` every hour. Meanwhile:

- `--test` printed **`smoke-test: ok (win=chat …)`** — it *rendered the target name* and never asked
  whether that window exists;
- `mesh-doctor`, `mesh-autowire` and `mesh-reflex-health` all read green: the cron line is present,
  the `--test` passes, the tool exits 0;
- the six `[chat-review]` lines on the current board are all **hand-posted by other windows** (`tg`,
  `job`). The marker is alive. The lane is dead.

**Thirty-four days of an hourly reflex producing nothing, invisible to every instrument we have,
because every instrument checked a tracing.**

## What landed

`scripts/mesh-chat-review` — the tracings plugged back into the map. Four changes:

1. **The target is RESOLVED against the live world, never asserted by name.** `resolve_win()` walks
   `MESH_CHAT_REVIEW_WINS` (default `chat witness`) and takes the first that is a live window in this
   node's session. An explicit `MESH_CHAT_REVIEW_WIN` pins one and disables fallback, so an operator
   can still aim it. A candidate *list* is still names — the improvement is that the names are
   checked against the world and the empty case fails loud.
2. **Every line the tool prints carries its TRAVERSAL AGE** (`last-traversed=<ISO> (Nd ago)` /
   `last-traversed=never`) and the count of consecutive skipped runs. A dead edge now says so in its
   own log, every run, instead of printing a cheerful skip.
3. **An unconditional RUN ROW** per run → `~/.mesh/chat-review-runs.log`. The old mark file recorded
   only *successes* — a numerator with no denominator ([[a-tape-of-only-positives-is-a-numerator]]),
   which is why "skipping forever" and "nothing to do" were the same silence. `--test` writes it to a
   temp path, never to the real ledger ([[a-dry-run-that-writes-the-liveness-log-forges-its-own-evidence]]).
4. **The dead edge is LOUD, not `exit 0` quiet.** Past `DEAD_DAYS=3` of no traversal, `announce_dead`
   traces + posts one board `[fyi]`, throttled to once per `DEAD_ALERT_MIN=1440` minutes, naming the
   candidates tried and the consecutive-skip count. Still `exit 0` (reflex-friendly).

And `--test` now asks the **map**: it resolves the target against live tmux and **FAILs** when a
minds-declaring node has none; a hands-off node exits 2 (organ legitimately absent, so autowire/doctor
SKIP rather than go red).

**Live artifacts, 2026-08-26:**

```
$ bash scripts/mesh-chat-review --test
smoke-test: ok (win=witness resolved from [chat witness] throttle=55m card=declares-minds
                chatlog=readable last-traversed=2026-07-23T10:37:03Z (34d ago))

$ bash scripts/mesh-chat-review
2026-08-26T21:45:50Z injected chat-review into witness
```

**The lane is alive again** — `mesh-tell --peek witness` shows the mind working the injected board
analysis. First traversal in 34 days.

Dead-edge path **driven and seen firing**, in an isolated fake `$HOME` with stubbed `mesh-chat`/
`mesh-trace` (`env -i HOME=<fake> PATH=/usr/bin:/bin`, the tool's own `$HOME/.local/bin` PATH export
making the fake home's bin the stub dir — [[a-poisoned-binary-can-lose-a-path-race-to-the-real-one]]):

```
skip: NO TARGET WINDOW — none of [__no_such_window__] is live in session mesh-home
      — last-traversed=never, 1 consecutive skipped runs
STUB mesh-chat: [fyi] mesh-chat-review: DEAD EDGE — no target window ...
second run: stub posts still 1 (throttled), run rows 2 (every run writes one)
```

**Mutants driven red, control green:**

| mutant | result |
|---|---|
| pin the aged-out name (`MESH_CHAT_REVIEW_WIN=chat`) — **the original bug, reproduced** | `FAIL (no live window among [chat] … the reflex is wired and can never fire; last-traversed=… (34d ago))` |
| a missing mark reads as freshly-crossed (**both** sufficient guards removed) | `FAIL (a missing mark must read as never-traversed …)` |
| `dead_due` can never fire | `FAIL (a never-traversed edge must read DEAD)` |
| `dead_due` always fires | `FAIL (a just-crossed edge read DEAD — the alarm would fire on a healthy lane)` |
| run ledger dropped (`consec_skips` → 0) | `FAIL (consec_skips counted 0, expected 2 …)` |
| control | `smoke-test: ok (win=witness …)` |

One masked mutant is noted rather than claimed: deleting only the `[ -f "$MARK" ]` line passes green,
because the `case ''` arm is independently sufficient
([[two-independently-sufficient-guards-make-a-single-line-mutant-vacuous]]). Both were removed
together to drive that arm.

## Behaviour change, stated plainly

This **revives a mind-touching reflex that has been dark for 34 days**: it will now inject a
board-analysis prompt into `witness` (IDLE-gated, card-gated, 55 m throttle), which is what
`charter/witness.md` already says witness is for. Disarm with `MESH_CHAT_REVIEW_WIN=<none>` or by
removing the cron line. The deployed `~/.local/bin/` copy is still the old one — until the steward
lands and deploys, only the tree copy resolves `witness`.

## What this review does NOT fix

The `rhizome_index` in `mesh-vitality` is still a tracing — a call-graph topology score with no
traversal term. Naming it is the finding; changing it is a different organ and is not in this arm's
assigned scope. Routed to the board.

---

## FOLLOW-UP (same day, genome, board task `rhizome-index-scores-declared-edges-not-traversals`)

The `rhizome_index` gap named above is **closed in `scripts/mesh-vitality`** — not by renaming the
axis, but by D&G's own corrective: *"plug the tracings back into the map."* The declared leg is kept
**byte-identical** and a **traversal leg** is computed beside it, never folded into it.

- **The observable.** There is no per-edge invocation ledger on this mesh, so per-EDGE traversal is
  not observable and the leg does not pretend it is. Per-NODE running *is*: each tool's own artifact
  under `~/.mesh` (`<tool>.log`, `<suffix>.log`, `.<suffix>.state`, its own dir) and that file's
  mtime. Each node classes **LIVE** (written inside `RZ_WIN_D`, default 14d) · **DARK** (an artifact
  exists and nothing has written it inside the window) · **UNKNOWN** (no such surface at all). An
  edge is **crossable** only if BOTH ends are LIVE, **provably dark** if EITHER end is DARK.
- **The asymmetry is stated, not hidden.** DARK is the sound verdict (nothing ran the tool → no edge
  into it was crossed). LIVE is an **upper bound** — mtime proves a touch, not a sign relation
  ([[mtime-proves-a-touch-not-a-sign-relation]]) — so `xC` is the centralization of the graph that
  *could* have been crossed. UNKNOWN is never folded into either.
- **Coverage travels with the number**: `cov` (share of tools with any evidence surface),
  `darkE`/`unkE` (share of declared edges provably dark / unknown), `win`. Three blind cases render a
  WORD and never a number: `x=UNKNOWN(evidence-dir-absent)`, `x=UNKNOWN(no-evidence-surface)`,
  `x=n/a(xN=..,xE=..)`.

**Live read, 2026-08-26 — the two legs disagree, which is the finding:**

```
rhizome=0.262/recip0.23/root=mesh-chat:186(N=688,E=4427)
       |x0.341/xrecip0.23/xroot=mesh-chat:111(xN=314,xE=1443)
       |cov0.51/darkE0.16/unkE0.51/win14d
```

The map is **more arborescent than the tracing** — C 0.262 → 0.341, i.e. the declared graph flatters
the mesh's resilience by ~30%. 726 of 4427 declared edges (16%) are provably dark. And `cov=0.51`:
**335 of 688 tools expose no evidence surface at all**, so half the node set is honestly UNKNOWN —
the leg subtracts what it can prove is dark and says so about the rest.

**Fixtures + mutants (7 red, control green).** The fixtures carry their **own** evidence dirs, never
the live `~/.mesh` — a fixture that reads the real world measures the world. The RING arm is the one
that reproduces the reported defect: a declared-perfect rhizome (`0.000/recip1.00/root=mesh-a`) with
**one** dark member reads `x0.500/xrecip1.00/xroot=mesh-b` — the score moves *and the named
single-point-of-failure moves*, which is exactly "it would rate a 34-day-dark reflex as it rates a
live one". The STAR arm splits its leaves three ways (LIVE · DARK · UNKNOWN) so folding dark into
unknown reddens it.

| mutant | result |
|---|---|
| an unknown node admitted as LIVE | RED (star fixture) |
| dark folded into unknown (`darkE=0`) | RED (star fixture) |
| no window — any surface reads LIVE | RED (star fixture) |
| the traversal leg dropped entirely | RED (live-repo shape arm) |
| `xtopo` computed over ALL nodes, not the live ones | RED (star fixture) |
| an ABSENT evidence dir rendering a traversal number | RED (absent-evidence fixture) |
| `cov=0` rendering a number instead of UNKNOWN | RED (empty-evidence fixture) |
| control | `mesh-vitality --test` green end-to-end |

**Where the traversal leg itself stops short** (it does not close the case): it is a NODE-liveness
bound standing in for EDGE traversal, so it can only ever subtract — a genuinely per-edge answer
needs invocation instrumentation the mesh does not have. And `cov=0.51` means the honest next step is
a beat-touch convention wide enough that a tool's *running* is observable at all.
