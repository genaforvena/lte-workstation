# Live literature review — swarm intelligence & stigmergy

**Area:** swarm intelligence / social-insect recruitment · **Angle:** a foundational idea we applied too
loosely — recruitment read as ONE mechanism when the literature has split it into two
**Date:** 2026-08-19 · **Channel:** genome · **Organ:** `scripts/mesh-handoff` (new report-only mode `--audit`)
**Status:** uncommitted in tree, steward lands

---

## What I went looking for and what I actually found

The mesh has landed sixteen reviews on this area (evaporation, repellent pheromone, trail entropy,
quorum, cross-inhibition, response thresholds, collective gradient, interaction rate, trace design,
ant mill, structural bias, zealots, the fundamental diagram, differential latency, directed
information, sematectonic vs sign-based). All of them are about the MASS-recruitment side of the
literature: a trace in a shared medium, read by many. Nothing in `docs/` or `scripts/` mentions
**tandem running** — the one-to-one branch — and that is where the misread turned out to be.

### The concept: a tandem run's PRODUCT, not its completion

Franks & Richardson, *Teaching in tandem-running ants*, **Nature 439:153 (2006)** — the founding
claim, and the one the mesh's own handoff doctrine unknowingly echoes: a tandem run is *teaching*
because it has **bidirectional feedback** between leader and follower. The leader sets the course;
the **follower sets the pace**, tapping the leader to say "still here, go on", and the leader waits
when contact breaks. That backchannel is what makes the run a transfer of a ROUTE rather than a
transfer of a BODY.

The correction — and this is the part we do not embody — is **Mizumoto, Tanaka, Valentini,
Richardson, Annagiri, Pratt & Shimoji, "Functional and mechanistic diversity in ant tandem
communication", *iScience* 26:106418 (2023)** (preprint: *Cryptic functional diversity in ant tandem
runs*, bioRxiv 2022.08.28.505613). They ran a combined network + information-theoretic analysis over
leader/follower trajectories in two genera and found that **the same named behaviour is two different
channels**:

- ***Temnothorax*** — "leaders and followers alternately influence their partner's behavior… the
  leader determin[es] the course… while the follower controls the leader's speed to effectively
  gather spatial information." The run's product is **a new recruiter**: an ant that goes on to LEAD
  the same route. *Temnothorax* "uses tandem running to recruit additional recruiters."
- ***Diacamma*** — "Diacamma tandem runs **lack bidirectional information flow, the signature of
  route-learning** in Temnothorax tandem runs." Followers do not regulate the leader; they only keep
  consistent close contact, which the authors read as *Diacamma* "prioritiz[ing] avoiding lost
  followers over providing opportunities for followers to collect spatial information." *Diacamma*
  "uses tandem runs not to share information, but to **transport nestmates**" — it "uses it
  principally to move the passive majority of their colony."

The word the authors use is **cryptic**: the two are indistinguishable in the aggregate. Same
behaviour, same completion statistics. Only the *product* — did the transfer create something that
can now lead the route, or did it move a body — separates them.

The thread is live, not a 2006 artefact: Mizumoto's 2024 review (*Ecological Research* 39,
10.1111/1440-1703.12510) develops the group-level-similarity-from-individual-diversity framing, and
the contact channel itself keeps being probed — Chakraborti, Mukhopadhyay & Annagiri, **"Restriction
of pedicel-flagellum joint in the antennae negatively impacts recruitment but not exploration in
ants", *Movement Ecology* 14:39 (2026)** (and the same group's *BMC Ecol Evol* 2024,
10.1186/s12862-024-02267-6): immobilise the follower's antennal joint and **tandem recruitment
degrades while solo exploration is untouched**. Break the backchannel and the transfer breaks while
the solo lane stays perfectly green — a shape this codebase has a name for.

## Where we applied it too loosely

`mesh-handoff` is DOCUMENTED as a teaching channel — CLAUDE.md says the SessionStart restore means
"the mind wakes holding its own thread" — and every guard in it is a *transport* guard:

- `--snapshot` on a `*/5` cadence, so a crash never loses the state → **do not lose the follower**;
- the hollow-guard and the no-clobber-a-fresh-manual rule → **do not lose the follower**;
- `mesh-clear`'s only hard gate is that the handoff WRITE succeeded → **do not lose the follower**;
- `refs/wip/<window>` beside it → **do not lose the follower**.

Every one of those is *Diacamma*: keep close contact, never drop the body. Not one of them asks
whether the receiver picked up the ROUTE. And structurally the channel has no backchannel at all —
the writer clears regardless of whether any reader could follow, so the follower cannot set the pace.
We built the transport channel and wrote the teaching claim on it.

Note what this is NOT: it is not the directed-information/coupling question that
`swarm-directed-information-net-asymmetry-leadlag-2026-08-19` already landed in `mesh-leadlag`.
Mizumoto et al. *measure* who-regulates-whom with transfer entropy over trajectories; we have no
trajectory pair to run it on. The transferable idea is the **product test**, which needs no coupling
analysis at all: after the transfer, does the receiver work the route that was handed to it?

## What landed: `mesh-handoff --audit` (report-only)

```
mesh-handoff --audit [--window <w>] [--horizon-h N] [--json]
```

Replays the board's `[handoff]` trail (`~/.mesh/chat-overflow.log` + `~/.mesh/chat.log`) and scores
each transfer by its product. For each handoff it rebuilds the **route set** the handoff named (repo
paths, `~/.mesh` artifacts, `mesh-*` tool names, ≥3-word kebab slugs, commit hashes), then looks at
that same window's later board lines within the **stint** — from the handoff until the window's NEXT
handoff, capped at `--horizon-h` (default 12h) — and emits:

- **route** — a later line touches the route that was named (teaching-shaped);
- **transport** — the window worked, and touched **none** of it (transport-shaped);
- **na** — unevaluable: the window posted nothing in the stint, or the handoff **named no route at
  all**. Missing evidence is never counted as transport.

Two things it publishes rather than hides:

1. **The bound direction.** The route set is rebuilt from the ≤240-char BOARD body, because
   `_write_handoff` overwrites the durable per-window file — the full text of a past handoff no
   longer exists anywhere on the node. Truncation can only LOSE route tokens, so **`route` is a lower
   bound and `transport` an upper bound**, and the output says so on every run.
2. **The stopwords it used.** The transfer machinery names itself in nearly every handoff
   (`mesh-handoff`, `mesh-clear`, `pre-clear`…); counting those as route overlap would make every
   transfer read as teaching by construction. There is an explicit machinery list plus a
   corpus-frequency guard (a token in ≥50% of the trail carries no routing information), calibrated
   on the live trail rather than frozen in the source, and the count is printed.

### The live reading (n=46, 2026-08-16 → 2026-08-19)

```
handoff-audit: n=46 route=23 transport=23 na=0 horizon=12h stopwords=2
  genome route=11 transport=13 · senses route=5 transport=6 · tg route=1 transport=3
  discover route=2 transport=1 · job route=2 · wake route=2
```

Read with the bound: **at most half** of this node's handoffs were followed by work on the route
they named; at least half were. The corpus stopword guard picked exactly the two boilerplate tokens
(`/.mesh/handoff/genome.md`, `mesh-home`) and nothing else. `na=0` across the live corpus, so the
missing-evidence branch is exercised only by fixtures — stated here rather than left to look like
coverage. This is a measurement, not an accusation: a mind legitimately gets re-tasked between
stints, and a transport-shaped transfer is not a fault. The point is that **until now nothing could
tell the two apart**, exactly as the paper says of the aggregate.

### Gates (each seen RED under its own mutant, from a scratch copy)

| leg | asserts | mutant that turned it red |
|---|---|---|
| P4a | route overlap is detected | — (positive control) |
| P4b | a receiver who worked on nothing named is `transport` | any-later-line counts as overlap → 5 red |
| P4c | no later line ⇒ `na`, never transport | fold the no-later branch into transport |
| P4d | a handoff naming no route ⇒ `na` | score the empty-route case anyway |
| P4e | the machinery's own name is not route overlap | `MACHINERY = set()` |
| P4f | an out-of-horizon touch is not credited | horizon widened to 240h |
| P4g | the stint ends at the window's next handoff | next-handoff clamp removed |
| P4h | the aggregate is the fixture's arithmetic | (fails under every mutant above) |
| P4i | an empty trail renders `na`, not `0 route / all transport` | empty-trail branch removed |

`mesh-handoff --test` green, rc=0, full suite.

## Deliberately NOT done

- **No gate on `/clear`.** The obvious next step — refuse a clear whose last handoff scored
  `transport` — is wrong twice over: it grades the previous stint to block the current one, and it
  re-introduces exactly the judgement that the operator removed from `mesh-clear` in 2026-07-24
  ("никаких llm-проверок"). Report-only.
- **No cron.** `mesh-handoff`'s `# reflex-cadence:` is `--snapshot`'s and stays that way; an audit
  that nobody reads is an unseen reflex. It is on-demand, like `mesh-forage`.
- **No backchannel invented.** The real *Temnothorax* fix would be a follower-paced transfer — the
  reader acknowledging, the writer waiting. That is a change to the clear/restore protocol and wants
  the operator; this review measures the gap rather than legislating it.

## Sources

- Franks NR & Richardson T. *Teaching in tandem-running ants.* Nature **439**:153 (2006).
  https://www.nature.com/nature/journal/v439/n7073/abs/439153a.html
- Mizumoto N, Tanaka Y, Valentini G, Richardson TO, Annagiri S, Pratt SC, Shimoji H. *Functional and
  mechanistic diversity in ant tandem communication.* iScience **26**:106418 (2023).
  https://www.cell.com/iscience/fulltext/S2589-0042(23)00495-9 · preprint
  https://www.biorxiv.org/content/10.1101/2022.08.28.505613v1.full
- Mizumoto N. *Ant and termite collective behavior: group-level similarity arising from
  individual-level diversity.* Ecological Research **39** (2024).
  https://esj-journals.onlinelibrary.wiley.com/doi/10.1111/1440-1703.12510
- Chakraborti U, Mukhopadhyay S, Annagiri S. *Restriction of pedicel-flagellum joint in the antennae
  negatively impacts recruitment but not exploration in ants.* Movement Ecology **14**:39 (2026).
  https://link.springer.com/article/10.1186/s40462-026-00663-9 · and *Restricted antennal movement
  impacts the tandem running dynamics in a ponerine ant*, BMC Ecol Evol (2024).
  https://link.springer.com/article/10.1186/s12862-024-02267-6
- Social learning of navigational routes in tandem running acorn ants (*Temnothorax nylanderi*),
  bioRxiv 2024.06.05.597530. https://www.biorxiv.org/content/10.1101/2024.06.05.597530.full.pdf
