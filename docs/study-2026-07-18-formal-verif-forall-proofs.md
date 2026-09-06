# Study finding — "parse GitHub repository links for potential Forall proofs" (formal verification)

**Source:** auto idea-queue task from the `study 'formal verification'` brief (2026-07-16T08:23:01Z).
**Verdict:** Historically declined as a build; reopened by the 2026-09-06 idea-queue task and
implemented as a small, non-networking parser in `scripts/mesh-study-bridge`.
**Date:** 2026-07-18 · owner: genome

## Reopened implementation (2026-09-06)

The study bridge now extracts canonical, deduplicated `https://github.com/OWNER/REPO` identities
from harvested item links. Issue/tree/commit suffixes and `.git` are removed, malformed profile-like
links are ignored, and the resulting candidates are supplied to the worker prompt as potential
Forall (∀) proof repositories. The worker is told to seek actual Lean/Coq/Agda/Dafny/Isabelle/TLA+
artifacts rather than infer a proof from a link alone. This keeps the feature small and read-only;
it does not clone or claim to verify external repositories.

## The ask, read literally

"Update worker code to parse GitHub repository links for potential *Forall* proofs." *Forall* = ∀ =
formal verification / theorem proving (Coq, Lean, Agda, Dafny, Isabelle, TLA+). The literal task: a
worker that ingests GitHub repo links and scans them for formal-proof artifacts.

## Why it does not map to this codebase (checked, not assumed)

Three preconditions for a non-orphan implementation, all ABSENT:

1. **No worker parses GitHub/repo links as a feature.** `grep -rlE 'github\.com|\.git|clone'` over
   `scripts/` hits only git remotes in comments and the word "clone" — no worker consumes a repo link.
2. **No formal-verification substrate.** No Coq/Lean/Agda/Dafny/Isabelle/TLA+ anywhere (the `lean`/`dafny`
   word matches are the adjective "a lean node" and unrelated tokens). The mesh does no theorem proving.
3. **No consumer.** Nothing downstream would read a "this repo contains ∀-proofs" signal. A tool with no
   consumer is precisely the speculative orphan the operator doctrine forbids ("no speculative wrapper,
   wire-on-demand"; "invoked-by is not ever-runs"; the verification principle's "declare an organ only
   after arming it").

Building it would produce a script that runs green in isolation, is wired to nothing, and manufactures
false capability — the exact failure class CLAUDE.md is built to prevent. That is a worse outcome than
no change.

## The honest reframe (for a future, real formal-verification task)

Our `--test` gates ARE the mesh's proofs, and their live integrity problem is documented and real: the
**vacuous self-grep gate** (`grep -q '<literal>' "$0"` always matches its own grep line — "33 of 52
self-grep gates are self-matching", CLAUDE.md 2026-07-15/1969a5d). A genuinely formal-verification-flavored,
non-orphan contribution would be a checker that flags gates asserting their own source text rather than a
runtime artifact. That is a real property to verify — but it is a *different task* with a real consumer, not
"parse GitHub links," and inventing it here would just be relabelling. Filed as the honest direction; not
built under this brief.

## Disposition

Negative finding — closes the idea so the queue does not re-dispatch a cargo-cult build. Sibling of the
study lane's earlier `finding-study-lane-hollow-20260705`. The artifact of a study is allowed to be "this
does not apply, and here is the evidence."
