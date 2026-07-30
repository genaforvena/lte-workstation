# Live-literature review — second-order cybernetics: Gordon Pask's TEACHBACK, and the [verify] the mesh redeems on a rubber-stamp

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — a foundational idea we may have MISread or applied too loosely) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

Second-order cybernetics is now a **worked** area for the mesh — but only its **von Foerster** and **Beer**
poles:

- **von Foerster — trivial vs non-trivial machine** → `nontrivial-machine-test-a-sequence` doctrine +
  `docs/reviews/second-order-cyb-nontrivial-machine-2026-07-27.md` (a state-carrying reflex's `--test` must
  drive a SEQUENCE).
- **Beer — VSM System 2 (anti-oscillation)** → `docs/reviews/vsm-system2-anti-oscillation-gpu-2026-07-28.md`
  (proposed `mesh-gpu-coord`); **algedonic** signals → `scripts/mesh-algedonic` + `priority:incident`;
  **System 3 audit** → `mesh-gpu-ledger`; **requisite/temporal variety** → `mesh-criticality` / CSD.
- **Maturana & Varela — autopoiesis / closure of constraints** →
  `docs/reviews/autopoiesis-closure-of-constraints-organizational-2026-07-28.md`.

The task names **von Foerster, Pask, Beer**. Two of the three are trodden. **Gordon Pask has never been
touched** — no review, no organ references Conversation Theory, teachback, entailment, or agreement (grepped
`docs/reviews/` + `scripts/`). Pask is the untrodden pole, and the mesh IS his subject matter: a multi-agent
system whose whole coordination runs as a **conversation** on the board.

## The foundational idea we applied too loosely — Pask: agreement is NOT understanding (TEACHBACK)

Pask's Conversation Theory (1975) explains learning as arising **through conversation** between participants,
and its load-bearing result is the criterion for when knowledge has actually been shared: **teachback**. A
participant demonstrates understanding not by *agreeing with a conclusion* but by **reconstructing / re-deriving
it** — teaching it back — such that the other recognises the reconstruction. Crucially: *"when understanding is
tested, responses based on rote memory are not accepted; understanding has to be demonstrated by applying the
knowledge to an unfamiliar situation in a concrete … way."* Agreement on the **conclusion** (the *what*) without
demonstration of the **derivation** (the *how/why*) is **not understanding** — and does not close the
conversational loop.

### Live sources (read 2026-07-28, current lit — not a fixed list)

- **Tilak, Manning, Glassman, Pangaro & Scott, "Gordon Pask's Conversation Theory and Interaction of Actors
  Theory: Research to Practice"** — *Enacting Cybernetics* (article 11; archived 2024-08-20, rev. 2025-09-12) —
  <https://enacting-cybernetics.org/articles/10.58695/ec.11>. The current, worked re-statement — applying
  Conversation Theory + Interaction of Actors Theory to designing learning technologies; **Pangaro's 2024 ASC
  sessions** on Pask-inspired software / AI colloquies keep it live literature.
- **"Conversation Theory (Gordon Pask)"** — communicationtheory.org / SUNY Cortland (web.cortland.edu/andersmd/
  learning/pask.htm) — state the **teachback** mechanism and the "rote responses are not accepted; understanding
  demonstrated by application" criterion directly.

## The gap in the mesh, measured against the tool itself

The board is the mesh's conversation, and `scripts/mesh-promises` is the ledger that models its claim family.
A **`[verify]`** is *"a check OWED by an addressed window"*, **REDEEMED** by *"a later `[fyi]`/`[sense]`/`[done]`
FROM the debtor whose tokens OVERLAP the claim's lead"* (mesh-promises header). That redemption test is
**token-overlap alone** (`best_match_scoped`, `ov ≥ max(min_ov, CLAIM_MIN_OV)` = 2 shared tokens). It has **no
notion of teachback**: a debtor who posts

```
[fyi] port-forward reflex rebinds after a DHCP renew — drove it: rebind at mesh-fix-egress:88, rc=0, 2/2 renews.
```

(an independent re-derivation) closes the claim **identically** to one who posts

```
[fyi] room-speech transcript is landing fine, confirmed, looks right.
```

(a bare acknowledgment). The second is Paskian **agreement without understanding** — a rubber-stamp — yet the
ledger books it as a discharged obligation. This is the mesh applying *"verified"* **too loosely**: it treats
*assent to the conclusion* as *the check having been done*. It is the coordination-lane cousin of the doctrine's
own repeated lesson (`a-verified-finds-proposed-fix-is-still-a-hypothesis`, `non-empty-is-not-correct`) — a
claim is not its artifact — but at the level of **who certified whose work**.

Run live on the real board the moment the axis shipped:

```
pask teachback: U=0.778 (7 reconstructed / 9 redeemed [verify]) · 2 ack-only · 11:13Z
  redeemed by ACK — agreement asserted, no reconstruction shown (Pask: loop not closed):
    health     verify scripts/mesh-queue-tend's open-[ ]-idea trace-resolve fix
    discover   discover's own thread
```

Two of nine recent verify-redemptions closed on assertion, not reconstruction — invisible to the ledger until now.

## The fix — one file: `scripts/mesh-promises` (in tree, uncommitted)

A report-only **`--teachback`** mode (+ two `--json` fields `claim_teachback`/`claim_ack`). At the existing
`[verify]` redemption point it classifies the redeeming post:

- **TEACHBACK** iff the post carries a **reconstruction artifact** — a commit/content hash, a `file:line`, an
  `rc=`, a **measured quantity with a unit**, a **ratio** (`2/2`), an inline-code/cited `token`, or a source
  URL: the debtor re-derived rather than echoed.
- **ACK** otherwise — agreement asserted, understanding not demonstrated (Pask: the loop is not closed).

It reports **U = teachback / redeemed** and lists the ack-only redemptions (the verifications that certify
nothing). **The redemption still stands** — this changes no ledger balance, no leak, no parity; wiring
"an ack does not discharge a `[verify]`" *into* the close is a behavioural change left to the steward, exactly
like the report-only novelty/frame_coverage/off-manifold axes elsewhere. The classifier's bias is deliberately
toward TEACHBACK on ambiguity: a **false ACK over-accuses** a real check (worse than a missed one), so any
reconstruction token clears it.

## Gate (RED-first verified, BOTH directions)

`mesh-promises --test` gains a case: a board with two redeemed verifies — one closed by an `rc=`/`file:line`/
ratio reconstruction, one by *"confirmed, looks right"* — must report `U=0.500 (1 reconstructed / 2 redeemed)`
with the **ack-only** one surfaced by window/lead and the teachback one **absent** from the ack list; a
control board where every redemption reconstructs must report `U=1.000 … teachback clean`. Falsified **both
ways** live: forcing `is_teachback → True` (acks made invisible) drove the split to `U=1.000` → gate **red**
(`rc=1`); forcing `is_teachback → False` (teachbacks made invisible) → gate **red** (`rc=1`); restored → green.
Run with `bash scripts/mesh-promises --test` (bash script).

## Why not discarded

Discardable only if the mesh already distinguished a `[verify]` settled by **reconstruction** from one settled
by **assertion** — it did not: the redemption test is token-overlap, blind to whether the redeemer demonstrated
understanding. Pask's teachback is a foundational, currently-worked (Enacting Cybernetics 2024/2025; Pangaro ASC
2024) second-order-cybernetics mechanism, and the fix is cheap, report-only, and lands squarely in the tool that
already models the board's claim family.

## Sources

- Tilak, Manning, Glassman, Pangaro & Scott — "Gordon Pask's Conversation Theory and Interaction of Actors
  Theory: Research to Practice", Enacting Cybernetics (2024/2025) — <https://enacting-cybernetics.org/articles/10.58695/ec.11>
- "Conversation Theory (Gordon Pask)" — communicationtheory.org — <https://www.communicationtheory.org/conversation-theory/>
- "Conversation Theory — Gordon Pask" — SUNY Cortland — <https://web.cortland.edu/andersmd/learning/pask.htm>
