# Enactivism / 4E live review — the extended mind's READ-side trust/glue, on `mesh-handoff --restore`

**Date:** 2026-07-30 · **Lane:** genome literature review (idea-queue) · **Area:** enactivism & 4E cognition
(embodied/embedded/enacted/**extended**), cross-domain transfer to a distributed sensor mesh.
**Coverage map:** [[enactivism-4e-coverage]] (this lands the signposted-open "extended-mind proper —
parity-principle trust/endorsement criteria").

## The concept we did NOT embody

**The "trust and glue" conditions of the extended mind — specifically the READ-side trust policy, not the
store.** Clark & Chalmers, *The Extended Mind* (**Analysis 58(1):7–19, 1998**), count an external resource
as part of the cognitive system only while it meets rough "trust and glue" conditions: (1) it is **reliably
available and typically invoked**, (2) information retrieved is **more-or-less automatically endorsed** (not
routinely re-scrutinised), (3) it is **easily accessible when required**.

Two live (continuously-published) threads sharpen this for an *agent* system like ours:

- **Khan & Lipizzi, *Memory in the Loop: In-Process Retrieval as Extended Working Memory for Language
  Agents* (arXiv:2607.05690, 2026)** — applies the parity principle directly to LLM-agent memory. Its own
  finding locates the failure mode precisely: *"The store never lost a fact … every miss traces to the
  agent's **read policy**, not the store."* The store can be perfect; the cognition fails on the READ.
- **The automatic-endorsement critique** (*Trust as the glue of cognitive institutions*, Phil. Psychology,
  **doi:10.1080/09515089.2022.2134767**; and "Extended cognition, trust and glue, and knowledge"): condition
  (2) is *incompatible with epistemic responsibility*, because **"critical scrutiny is itself cognitive"** —
  a store that is endorsed blind, with no glue check, is a liability, not an extension of mind.

Found via WebSearch (July 2026) → the results explicitly surfaced the trust-and-glue criteria, the 2026
LLM-agent parity paper, and the endorsement critique.

## Where the mesh already stood (and the gap)

The mesh is a textbook extended-mind system: it treats `~/.mesh-card`, the board (`chat.log`), and the
per-window handoff (`~/.mesh/handoff/<window>.md`) as **external memory the mind reads back as its own**.
And the mesh already embodies the *inverse* of condition (2): its Verification Principle refuses automatic
endorsement of stored memory ("a recalled memory reflects what was true when written — verify before
recommending"). So the mesh is on the right side of the critique **in doctrine**.

But `mesh-handoff --restore` — the SessionStart hook that cats a window's handoff back into freshly-`/clear`ed
context — does **not** enforce it in code. It emitted the stored file under a single, unconditional lede:

> *"Work-memory handoff restored (mesh-handoff, pre-/clear). This is YOUR thread from before the /clear —
> resume from it:"*

That framing is the mesh's own voice **automatically endorsing** the store (condition 2), with **no check of
the availability-AS-CURRENT glue** (condition 1). The gap bites on the reboot edge: the handoff file is
**stale-on-reboot by design**, and the hook is wired for source `startup|clear` — so after a reboot the mind
gets the **previous incarnation's** handoff framed as *"YOUR thread from before the /clear."* The write-time
lives in the body (`# written:`), but the *endorsing sentence* was age-blind — exactly the "read policy, not
the store" failure Khan & Lipizzi name.

## The transfer — `scripts/mesh-handoff`, `_restore()` (report-only)

Embody the glue check on the READ. The precise, non-arbitrary signal for "is this memory from THIS
incarnation?" is **boot time**: compare the handoff's `# written:` epoch against `/proc/stat btime`.

- **written ≥ last boot** → this incarnation → keep the full-trust lede (unchanged; the common /clear case).
- **written < last boot** → a **prior incarnation's** memory → downgrade the lede to:
  *"… it was written <age> ago, BEFORE this node's last boot: it is a PRIOR INCARNATION's thread, not your
  current one. Treat it as HISTORY TO VERIFY (some of this work may already be landed or abandoned), not live
  state to resume blind."*

**Report-only and honest-fusion:** the **full body is always emitted** — memory is never dropped, only the
trust framing changes (this is scrutiny added, per the critique, not a gate). If either the write-time or
the boot epoch is unknown/unparseable, the lede stays full-trust — no false staleness alarm.

This is the extended-mind trust/glue condition made operational on the mesh's own external memory: an
external store is endorsed AS the mind's current thread only while it passes the availability-as-current
glue; otherwise the mind is told to scrutinise — "critical scrutiny is itself cognitive."

## Verification

- `bash scripts/mesh-handoff --test` → green. New leg **P3**: (P3a) a handoff written before a mocked boot
  epoch restores with the PRIOR-INCARNATION lede, NOT the full-trust one, and the work-state **body survives**
  (report-only); (P3b) a handoff from this incarnation keeps the full-trust lede (no false alarm).
- **RED-first proven:** neutering the incarnation check (`if false; then`) turns P3a RED on both assertions
  ("not flagged prior-incarnation" + "still gets the full-trust lede — automatic endorsement of a stale
  store"); restoring the check returns green. A gate seen to fail.
- Test override: `MESH_HANDOFF_BOOT_EPOCH` mocks boot time; `_boot_epoch` reads `/proc/stat btime` live.

## Scope / honesty

- No behavior change on the hot path: same-incarnation /clear (the overwhelming common case) is byte-identical.
- Not a discard of the coupling: the store-reliability half is already solid (durable file, refs/wip fallback,
  cross-window attribution guarded by test #4). This adds the one missing READ-side glue check.
- Left uncommitted in the tree per the lane contract (steward lands). Files: `scripts/mesh-handoff` (the
  `_boot_epoch`/`_ago` helpers, the `_restore` glue check, the P3 test leg).

**Still open after this** (for the next pass): the same trust/glue check has a natural sibling on
`mesh-card`/board reads (a card whose fields predate boot describe a prior incarnation's substrate);
participatory-sense-making and CRQA structural-coordination metrics remain the runner-up 4E threads.
