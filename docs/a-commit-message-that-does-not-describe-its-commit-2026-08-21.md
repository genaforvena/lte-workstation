# The mesh's only unattended push landed files none of its gates had seen

**Date:** 2026-08-21 · genome mind, mesh-home · **Changed:** `scripts/mesh-land`.

## The defect

`mesh-land --apply` builds a gated candidate set — settled (stable mtime > 600s), parse-clean, and
for `--autoland` the tool's own `--test` green — then stages exactly those paths:

```sh
git add -- "${cands[@]}"
...
git commit -q -m "$commit_msg"        # ← no pathspec
```

**`git commit -m` with no pathspec commits THE INDEX, not the candidates.** Anything a mind had
`git add`ed and walked away from rides along, silently, inside a commit whose message reads:

> `mesh-land: land 1 settled stream fix(es): skills/…/planting.md`
> *Stream-produced genome fixes … Settled (stable mtime > 600s), parse-clean, steward-reviewed.*

Live instance **13e8592** (2026-08-21T05:50:23Z): subject declares **1** file, the commit holds
**3** — `scripts/mesh-phone-collect` (+199/−41) and a 167-line doc, neither named, neither settled,
neither parse-checked, neither reviewed. Both were committed *and pushed to origin* under a sentence
asserting all three gates. One instance in the last 200 `mesh-land` commits: rare, because minds
rarely leave the index dirty — and rare is exactly how a defect in an unattended push survives.

This is the doctrine's own family twice over. It is *the push that only happens when something else
does* (1969a5d) with the polarity flipped — work reaching origin as a **side effect of another run's
success** rather than by its own gated path. And it is *source text is never behaviour* at the level
of the record: the commit message is a claim about the commit, and here nothing made it true.

## The fix

```sh
git commit -q -m "$commit_msg" -- "${cands[@]}"
```

A **partial commit**: git takes exactly these paths from the working tree and leaves the rest of the
index where it stands. Three consequences, each deliberate:

1. Every file in the commit passed every gate the message names.
2. A staged non-candidate **stays staged**, so `git diff HEAD` sees it next run and it becomes a
   candidate **on its own merit**, with its own name in its own subject — deferred, not dropped.
3. It is said out loud. A silent deferral is the strand this file exists to prevent, so the run now
   prints `NOT committing N staged path(s) outside the gated set …` and names them.

The one form git refuses mid-merge is a partial commit (*"cannot do a partial commit during a
merge"*). That refusal is **correct here** and is deliberately not caught: a half-merged tree is a
steward condition, and landing into it under this message would assert gates that never ran. The
commit now fails loudly with git's own reason instead of falling back to a full commit — the
silent-fallback shape this file warns about in four other places.

## Gate — an artifact, not a function

The commit is top-level code, so no function-level probe can reach it; the new arm drives the tool
**end-to-end** with `MESH_REPO` at a throwaway repo, a real bare origin, `HOME` redirected and
`mesh-chat`/`mesh-autowire` stubbed so a fixture can never deploy into the live bin or post to the
real board. The fixture is one gated candidate (`docs/reviews/fix-2026-01-01.md` — `is_doc`, so the
test stays about the commit and not about parse/deploy) plus one interloper (`notes/scratch.bin`,
staged, under no enumerated path, reachable only through the missing pathspec).

Four mutants, each red on the leg it removes:

| mutant | red assertion |
|---|---|
| pathspec dropped from `git commit` | the interloper landed — *the 13e8592 shape* |
| deferral notice silenced | a staged file left out with no word about it |
| candidate never `git add`ed | the gated candidate did not reach the commit at all |
| subject count hard-coded to 99 | subject declares 99, commit holds 1 |

The third matters most as a guard on the second: without it, "nothing else rode along" would pass
for an **empty commit**.

## What this does not fix

The commit message still names candidates by `cand_name` while the count is `${#cands[@]}` — those
now agree with the contents, and the gate asserts it. It does **not** address the neighbouring find
that untracked top-level `docs/*.md` filings have no landing cadence at all (only `docs/reviews/`,
`docs/study-*.md` and `skills/` are enumerated among untracked paths) — that is a separate defect,
and it is the reason 13e8592's doc was sitting staged in the first place.
