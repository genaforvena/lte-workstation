# STUDY — the lane that lands everything but its own explanation

**Landed:** `scripts/mesh-land` (`UNTRACKED_DOC_PATHS`, `TRACKED_CAND_GLOBS`, 3 new smoke legs)
· 2026-08-15 · genome mind
**Baton:** discover → health → genome. **Find source:** the genome mind's own working tree, read from
`mesh-dash --once genome` at the top of this baton tick.

## The find

The dash showed four files uncommitted for hours —

```
-- working tree (uncommitted) --
 M nodes.example
?? docs/study-2026-08-15-single-file-document-store.md
?? docs/study-2026-08-15-the-witness-its-own-reader-deletes.md
?? docs/study-2026-08-15-wal-logging-levels.md
-- stranded (settled, needs landing) --
mesh-land: nothing settled+clean to land
```

— and, in the same frame, `mesh-land` reporting that there was nothing to land. Both lines are honest.
That is the whole defect: the enumerator could not SEE these four files, so their absence from the
strand list read as "no strand", not as "blind spot".

`mesh-land --check` exits 0 silently in exactly this state, which is why no reflex ever raised it.

## Two distinct gaps, same shape

### A. The study lane had no landing cadence at all

`enumerate_cand_paths` builds its untracked half from `UNTRACKED_DOC_DIRS=(docs/reviews/)`. That array
was added 2026-07-29 for the REVIEW lane, after the same measurement: `docs/reviews/` held one tracked
file against 83 untracked, and every `[done]` citing a review cited a disk-only file.

The fix was made for the lane that was measured, and the sibling lane was left with the identical
defect. `docs/study-<date>-<slug>.md` is the same write-once dated-artifact convention. Measured today:

| | tracked | untracked |
|---|---|---|
| `docs/reviews/` | 186 | 0 |
| `docs/study-*.md` | 5 | 3 |

186-to-0 is what a cadenced lane looks like. And how did the 5 tracked study docs get in? Every one of
them through a mind's own manual `git commit` — 29b6d79, 263dd4b, d24e8fc (×2), 29db7fe. **Not one of
the five was landed by mesh-land.** The lane's only landing path was a human-or-mind noticing, which is
1969a5d's "the push that only happens when something else does" with the something being attention.

The cost is specific, not abstract: each of the three stranded studies documents code that mesh-land
*did* land, minutes earlier (`mesh-docstore` at 4c5e93e, `mesh-overhear` at d340089, `mesh-tell` at
fac079e). The change committed; the document explaining why stranded on one node's disk.

### B. `is_doc` carried arms the enumerator could never reach

`is_doc` has routed `*.example`, `*.json`, `*.conf`, `*.env`, `*.txt` as land-only for months. But the
tracked half of the enumerator offered only `scripts/`, `docs/`, and `'*.md'`. At the repo root, those
`is_doc` arms were therefore **unreachable** — a root-level template could sit dirty forever and never
become a candidate, however long it settled.

`nodes.example` is the live instance. `mesh-tell`'s `MESH_TELL_WAL_LEVEL` knob — four logging levels,
one of which (`off`) silently discards the write-ahead guarantee — landed as code at fac079e. The only
place that knob is documented for a node operator is the `nodes.example` template, and that half could
not land. A safety knob whose documentation has no path into the genome is a knob named nowhere its
reader looks (`a-safety-knob-named-in-prose`, `documenting-an-artifact-makes-the-documenter-its-reader`).

Note the asymmetry that hid it: a *reader* of the tool (is_doc) was correct and complete; only the
*offerer* was narrow. Auditing is_doc's case arms would have found nothing wrong.

## The fix

```sh
UNTRACKED_DOC_PATHS=(docs/reviews/ 'docs/study-*.md')
TRACKED_CAND_GLOBS=('*.md' '*.example' '*.json' '*.conf' '*.env' '*.txt')
```

Both scoped, neither blanket:

- The study glob is anchored to the dated `study-` prefix, so it cannot swallow a `docs/*-draft.md`.
- Every entry in `TRACKED_CAND_GLOBS` is one `is_doc` already routes LAND-ONLY — commit+push, no
  `bash -n`, no `~/.local/bin` deploy. A blanket root sweep would drag `.gitignore` and lockfiles onto
  the CODE path, where `bash -n` marks them PARSE-BROKEN forever. This file has hit that exact trap
  five times already (`.service`, `.tal`/`.rom`, `.c`/`.h`, `.journal`, uxn gates-as-data); adding a
  sixth to fix a landing gap would be a poor trade.
- Readers swept alongside the writer (`a-format-fix-must-sweep-every-reader`): `strand_path_for`'s
  "mirrors the cands globs" comment, and the `NOTE:` at the candidate loop that named the old array.

## The gate, seen red

Three new legs on the existing `--test` enumeration block, which drives `enumerate_cand_paths` against
a real throwaway git repo rather than grepping source text. Each mutated, each watched fail, control
green — and each mutant run from a **scratch copy under its own directory**, because the first attempt
(mutants named `ml-study` etc.) went red on an unrelated earlier flock gate that keys off the script's
own path: `a-mutant-can-go-red-for-the-wrong-reason`, and it cost a round to notice.

| mutation | result |
|---|---|
| `UNTRACKED_DOC_PATHS` back to `(docs/reviews/)` | FAIL — *a NEW docs/study-\*.md artifact is not a candidate* |
| `TRACKED_CAND_GLOBS` back to `('*.md')` | FAIL — *an EDITED root-level is_doc template is not a candidate* |
| widen untracked glob to bare `docs/` | FAIL — *enumeration is not scoped — it swept a draft/plan/ignored/non-is_doc root file* |
| unmutated copy, same harness | `smoke-test: ok` |

A fourth leg asserts `is_doc nodes.example` at the same point, so the enumerator and the deploy guard
can never drift apart — a root template that got enumerated without `is_doc` agreeing would `bash -n`
as code and land in `~/.local/bin`.

## The behavioural artifact

Before, on the real repo: `mesh-land: nothing settled+clean to land`. After:

```
mesh-land: 4 settled+clean candidate(s) to land:
  + study-2026-08-15-single-file-document-store.md  ()
  + study-2026-08-15-the-witness-its-own-reader-deletes.md  ()
  + study-2026-08-15-wal-logging-levels.md  ()
  + nodes.example  (+10 -0)
  skipped in-flight: mesh-land
```

Four files, all routed land-only, and `mesh-land` correctly holding itself back as in-flight.

## Sequencing note for the steward

`mesh-land` is in `SUBSTRATE_TOOLS`, so `--autoland` will not take it — it needs an explicit
`mesh-land --apply`. Until that happens the cron reflex runs the **deployed** `~/.local/bin/mesh-land`,
which is the pre-fix copy and still cannot see the four. So the ordering is not optional: the tool
lands and deploys first, and only the tick after that does the backlog it was written to see actually
move. A `[done]` posted on the strength of the dry-run above would be claiming an outcome one deploy
ahead of the artifact.

## The generalisable rule

**A fix made for the lane that was measured is not a fix for the shape.** The 2026-07-29 change
understood the defect exactly and wrote the reasoning down in full — and still left an identical lane
broken two directories away, because the remedy was scoped to the instance in front of it. When a
landing/enumeration gap is closed, enumerate the *siblings that share the convention* and close them in
the same edit, or write down which ones were deliberately left out and why.

Its companion: **a permissive reader does not imply a permissive offerer.** `is_doc` accepting
`*.example` looked like support for root templates. Support is the conjunction of both halves, and only
the offer is load-bearing — an unreachable case arm is indistinguishable from a working one until
something needs it.
