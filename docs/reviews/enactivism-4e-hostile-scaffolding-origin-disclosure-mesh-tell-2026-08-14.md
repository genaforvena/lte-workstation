# 4E critique: hostile scaffolding — the mesh discloses provenance to the auditor, not to the mind

**Area:** enactivism & 4E cognition, entered from a **known failure mode of the area itself**.
**Date:** 2026-08-14 · **Organ:** `scripts/mesh-tell` · **Status:** landed, opt-in, uncommitted for the steward.

## The critique (this is the angle, not decoration)

The situated/extended-cognition literature has a named blind spot, and its own editors name it:

> "Treatments of situated and extended cognition and affect tend to be **optimistic and apolitical**,
> focusing mostly on the **benefits** of external cognitive resources for an individual user."
> — Spurrett, Colombetti & Sutton, *Introduction: Scaffolding Bad — Varieties of Situated Cognitive
> Harm*, **Topoi 44(2):345–351 (2025)**, doi:10.1007/s11245-025-10167-7

The counter-concept is **hostile scaffolding** (Timms & Spurrett, *Philosophical Papers* 52(1), 2023,
doi:10.1080/05568641.2023.2231652): scaffolding that

> "depends on the **same capacities** of an agent to make cognitive use of external structure as in
> benign cases, but that **undermines or exploits the user while serving the interests of another
> agent**" — environmental and social structures shaping cognition "**in the interest of others, not
> of the scaffolded person**".

Two load-bearing details. First, the harm is not a malfunction: it rides the *working* mechanism, so
nothing looks broken. Second, **depth of offload is the risk multiplier** — "in cases where the
scaffolding is deep and permits the offloading of significant cognitive work, hostile scaffolding
exploitatively manipulates cognitive processing itself." The collection extends this past deliberate
hostility to structural and negligent harm (Mossner & Walter, *Scaffolded Affective Harm*, Topoi
44(2):627–641, 2025). Live and continuing: Liao, *Critical 4E Cognitive Science*, **Philosophy Compass
(2026)**, doi:10.1111/phc3.70075 — "critical turns focus on the **downsides** of agent-environment
interactions".

**Why this area and not another:** every prior 4E landing here (see the coverage memory) asks whether a
coupling is *live, influential, or well-timed*. None asks **whom the coupling serves**. That is the
literature's own blind spot reproduced in the genome.

## The gap: `mesh-tell` captures `who`, then files it where the addressee cannot read it

`mesh-tell` is the mesh's deepest offload by the literature's own criterion — CLAUDE.md mandates it as
the self-continuation, keepalive and dispatch primitive, and a mind acts on what appears at its prompt.

The WAL already records the sender. `wal_append` (`scripts/mesh-tell:181`) writes
`ts · pid · phase · who · node · win · b64(prompt)` with `who="${MESH_WHO:-$(id -un)}"`. But the pane
receives the payload **verbatim** (`:684`, `load-buffer` → `paste-buffer -p`). So the one field that
would let a mind weigh an instruction is captured and then routed **to the auditor, away from the
addressee**.

Consequence, and it is not hypothetical. CLAUDE.md ranks operator instruction above skills and above
default behaviour. A live WAL line from tonight:

```
2026-08-14T23:10:47Z  1424647  intent  job@mesh-home  local  sound  <b64>
  decoded: "оператор просил дважды (22:26 и 22:43 в TG, до сих пор без ответа): сдела…"
```

`job@mesh-home` injected into `sound` a prompt that **invokes the operator's authority**. It may well
be a faithful relay — that is exactly the point: the receiving mind **cannot tell**, and the field that
would settle it was written to a log it never reads. A mind cannot distinguish its own
self-continuation, another mind's nudge, a cron reflex, and the operator. That is the hostile-scaffolding
structure precisely: it exploits the capacity that makes the channel work at all (a mind treats what
appears at its prompt as addressed to it and acts on it).

**Live scale** (`~/.mesh/tell-wal.log`, 2026-07-27 → 2026-08-14): **1997 injections, 7 distinct senders.**

## Landed: `mesh-tell --origin` (opt-in, default OFF)

A one-line, same-line stamp applied **before** `b64`, so the WAL still journals the exact bytes the pane
receives: `[via <MESH_WHO>@<host>] <prompt>`.

Disclosure does not weaken the capacity the channel rides — it **prices** it.

Three deliberate constraints, each of which is a leg:

- **Default OFF.** This is the keepalive/dispatch/self-continuation path; a default-on rewrite of what
  every mind reads is not a change to make without the steward.
- **Same line, never a leading newline.** This file's own documented stall class is the multi-line paste
  stranding at `paste again to expand`. A disclosure that added a line would buy provenance with lost
  prompts.
- **Two hard skips** — a payload whose first non-space char is `/` (a slash-command must reach the engine
  as the first token or it is prose), and `MESH_TELL_ALLOW_SHELL=1` (the deliberate bare-shell send,
  where a prefix is a syntax error, not a sentence).

### Gate

5 legs, all driving the real script and asserting on the WAL payload — never on `origin_stamp` in
isolation, because a pure-function leg passes while the stamp is unwired (the `mesh-load-gate` E9
lesson). Mutants, each red on a **distinct** leg:

| mutant | change | red on |
|---|---|---|
| 1 | disclosure always-on | o1 (proven directly: emits `[via TESTWHO@mesh-home] hello world` where o1 demands byte-identity) |
| 2 | hardcode the stamp to `operator@` | o2 **and** o5 |
| 3 | drop the slash-command skip | o3 (`[via TESTWHO@mesh-home] /clear`) |
| 4b | drop the ALLOW_SHELL skip *from `origin_stamp` only* | o4 (`[via TESTWHO@mesh-home] git pull && echo x`) |

Mutant 1 aborts at an earlier `--fresh` leg before reaching o1, so o1 was proven **separately** by
driving the mutant and reading the WAL — a mutant caught by someone else's leg does not prove yours.
Mutant 4's first form edited `dead_shell_guard`, which shares that exact line; it reddened the
dead-shell gate instead, so it was retargeted (4b). Both are the "a mutant can go red for the wrong
reason" trap, met twice in one gate.

## Honest limits

- **The disclosure is only as good as `MESH_WHO`, and today it mostly is not set.** Of 1997 intents,
  **1938 (97%) carry the bare host identity** `mesh-home` (the `id -un` fallback); only 59 are
  window-qualified (`genome@` 30, `tg@` 13, `health@` 12, `pub@` 2, `senses@` 1, `job@` 1). Enabled
  today, most sends would stamp `[via mesh-home@mesh-home]` — "something on this node", not who. The
  field rotted **because nothing ever read it**; this change creates the reader, and the callers
  (dispatch, keepalive, cron reflexes) must now set `MESH_WHO` for the stamp to carry information.
  That sequencing is the steward's, and it is the real remaining work.
- **Not wired.** No reflex or dispatch path sets `--origin`. Per the mesh's own rule, a mechanism you
  have not seen fire is absent — this is landed and gated, not in service.
- **This is disclosure, not authentication.** Any sender can set `MESH_WHO` to anything. It defeats
  *undisclosed* provenance, not a deliberate impersonator. Claiming otherwise would be the "a mode bit
  is not the write" error in a new costume.
- **Distinct from the landed `mesh-handoff` trust-and-glue fix**, which age-checks a *stored artifact*
  against boot. This is the *live channel*, and the axis is sender identity, not staleness.

## Sources

- Spurrett, Colombetti & Sutton (2025), *Introduction: Scaffolding Bad — Varieties of Situated Cognitive
  Harm*, Topoi 44(2):345–351 — https://link.springer.com/article/10.1007/s11245-025-10167-7
- Timms & Spurrett (2023), *Hostile Scaffolding*, Philosophical Papers 52(1) —
  https://www.tandfonline.com/doi/abs/10.1080/05568641.2023.2231652 · https://philpapers.org/rec/TIMHS
- Mossner & Walter (2025), *Scaffolded Affective Harm*, Topoi 44(2):627–641 —
  https://link.springer.com/collections/aadfbjhfec
- Liao (2026), *Critical 4E Cognitive Science*, Philosophy Compass —
  https://compass.onlinelibrary.wiley.com/doi/10.1111/phc3.70075
