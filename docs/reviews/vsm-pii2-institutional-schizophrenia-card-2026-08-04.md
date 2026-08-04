# VSM pathology PII2 — "institutional schizophrenia": the node's identity declared twice, differently

**Live literature review · 2026-08-04 · viable system model / management cybernetics → node self-description**
Landed: `scripts/mesh-card` (`identity_conflicts()` / `identity_verdict()`, new `--identity` mode,
new `identity-coherence:` line in the card's live block). Report-only — the card never fails on it.

## The angle: a failure-mode taxonomy, not the model

The task asked for a **known critique or failure mode** of Beer's VSM. The area has a purpose-built
one: **José Pérez Ríos's Taxonomy of Organizational Pathologies (TOP)** — 26 named ways a viable
system fails, grouped I (structural) / II (functional) / III (information systems & channels). It is
the standing answer to the common charge that the VSM is a descriptive diagram with no diagnostic
teeth.

Sources read for this review (both fetched and read in full, not cited from memory):

- **José Pérez Ríos, "The Viable System Model and the Taxonomy of Organizational Pathologies in the
  Age of Artificial Intelligence (AI)", *Systems* 13(9):749, 29 Aug 2025,
  [doi:10.3390/systems13090749](https://doi.org/10.3390/systems13090749)** — the live one: Pérez Ríos
  himself re-stating TOP a year ago and re-reading every pathology through AI adoption. (MDPI's HTML
  and PDF both 403 to the fetcher; the PDF came down as bytes and was read via `pdftotext`.)
- **José Pérez Ríos, "Models of organizational cybernetics for diagnosis and design", *Kybernetes*
  39(9/10):1529–1550 (2010),
  [doi:10.1108/03684921011081222](https://doi.org/10.1108/03684921011081222)** — the canonical
  enumeration of all 26 pathologies with definitions (I1–I4, II1–II17, III1–III5).
- Espinosa, "Revisiting the Viable System Model as an emancipatory systems approach", *SRBS* 42
  (2025), [doi:10.1002/sres.3090](https://doi.org/10.1002/sres.3090) — surveyed for context (Jackson's
  standing criticisms); not the landing.

The pathology landed, verbatim:

> **PII2. Institutional schizophrenia.** Two or more different identity conceptions produce conflict
> within an organization.
> — Pérez Ríos 2025, §2.3.2 *Pathologies Related to System 5*; identically in Pérez Ríos 2010, §4.II.

System 5 **is** identity — Pérez Ríos makes answering "who am I, what is my purpose, where are my
boundaries" the *mandatory first stage* of any VSM application. PII2 is the failure where that answer
exists more than once, in conflict, and different parts of the system act on different copies.

## Why it is NOT already embodied

Grepped `scripts/` + `docs/reviews/` first (per the VSM coverage memory — this ground is dense).
Already landed and deliberately not re-trodden: algedonic channel + saturation defense
(`mesh-algedonic`), S3↔S4 homeostat / II5–II6 "headless chicken" (`mesh-vitality homeostat34`), Beer
ACP indices, requisite variety (`channel_variety`), residual variety / II7 S1 autonomy
(`residual_variety`), power-relations & agenda concentration (`power_concentration`), II11 System 3\*
independent audit (`mesh-liveness-loop --audit-cron`), III1/III2 write-only information systems
(`mesh-doctor`'s umwelt-check: a `.state` producer with no reader anywhere).

**PII2 had zero hits.** The nearest thing is `mesh-card`'s own `minds_off_by_channels()` — which
exists *because of* one PII2 instance (ds's card declared `minds: claude opencode ollama` while its
`restore.env` said `MESH_MIND_CHANNELS="none"`, and every card-trusting tool believed the wrong
conception). But that function **reconciles one specific pair at the moment of writing**. It does not
ask how many rival conceptions the node is carrying, and nothing else does either.

## The mesh instance

A mesh node's S5 identity is not held in one place. It is declared across:

- `~/.mesh-card` — `minds:` / `senses:` / `actuators:` (doctrine: **the card is AUTHORITATIVE**)
- `~/.mesh/restore.env` — per-channel `MESH_*_CMD` (which engine each mind IS),
  `MESH_MIND_CHANNELS` (which channels exist), `MESH_RETIRED_CHANNELS` (which are decommissioned)
- `~/.mesh/nodes` — `MESH_ROLES`

Shell sourcing is **last-wins**, so a redeclared key is behaviourally fine — and that is exactly what
makes it a *pathology of conception* rather than of execution. The earlier line is dead, but it still
**reads as live** to a human, and to an agent grepping the file for "what engine is health?". Same
family as the doctrine entries *"a stale `Wants=` resurrects a retired organ"* and *"a constant
outlives its reader"*.

### What it found, live, on mesh-home

```
$ mesh-card --identity
identity: ⚠ CONFLICTED — VSM PII2 (institutional schizophrenia), 19 conflict(s)
  - redeclared MESH_MINDS_CMD: L22="$HOME/.local/bin/mesh-agy" -> L64="$MESH_CLAUDE_CMD" ...
  - redeclared MESH_HEALTH_CMD: L34="opencode -m opencode/deepseek-v4-flash-free" -> L66="$MESH_CLAUDE_CMD" ...
  - redeclared MESH_HEALTH_CMD: L66="$MESH_CLAUDE_CMD" -> L259="$MESH_SONNET_CMD" ...
  - redeclared MESH_CONSUME_CHANNELS: L145="minds:… vpn:14400 models:28800"
                                   -> L282="minds:… models:28800 witness:28800 diary:28800" ...
  … 19 total across 13 keys
```

**13 keys carry ≥2 conflicting conceptions.** `MESH_HEALTH_CMD` alone is declared three times, in
three different engines. `MESH_CONSUME_CHANNELS` carries two different channel rosters — one of them
missing `witness` and `diary` entirely. Anyone reading the file top-down learns the wrong answer
about who the `health` mind is; this is the readable form of the already-recorded
[[keepalive-sticky-engine-pins-old-mind]] / [[retrying-opencode-reads-as-sovereign-blocks-engine-switch]]
confusions.

The live card now carries the verdict:

```
  invariant-check: OK
  identity-coherence: ⚠ CONFLICTED (19 — PII2 institutional schizophrenia; see `mesh-card --identity`): …
```

## What was built

`scripts/mesh-card`:

- `identity_conflicts [env] [card]` — prints one line per conflict, three kinds:
  1. **`redeclared`** — same `MESH_*` key, two different **source texts**. Comparison is on source
     text deliberately: `A="$X"` and `A="$Y"` may expand alike, but PII2 is about the conceptions a
     *reader* holds, and a reader reads the text. Identical re-assignment is redundancy, **not**
     schizophrenia — not flagged.
  2. **`planted+retired`** — a channel named in both `MESH_MIND_CHANNELS` and
     `MESH_RETIRED_CHANNELS`: alive and decommissioned at once.
  3. **`card-vs-policy`** — card `minds:` non-empty while the allowlist names no real channel (the
     ds regression, now *measured* instead of silently reconciled). It compares against the card **as
     it stood** — which is the correct reading: the pathology is that other tools have been acting on
     that conception.
- `identity_verdict` — the one card line: `COHERENT` / `⚠ CONFLICTED (n): <first>` /
  `n/a (no readable restore.env — cannot ask)`. **A missing `restore.env` returns rc=2, never a
  silent COHERENT** — n/a must be a claim about the node, not a blank that reads as health.
- `mesh-card --identity` — the full list.
- Parsing is **mawk-safe** (no gawk 3-arg `match()`), a quoted value keeps a `#` inside it, and a
  commented-out declaration is not a declaration — restore.env carries several
  `# MESH_MIND_CHANNELS="..."` archaeology lines that would otherwise be pure noise.
- Sourcing for the effective (last-wins) values happens in a **subshell**: `restore.env` exports
  dozens of variables and must not rewrite its inspector's environment.

### Gates (RED-first; four mutants seen red from a scratch copy)

Nine arms in `mesh-card --test`, all driving the real functions against fixture surfaces, plus arm (9)
which drives **one real `--refresh`** over a scratch `HOME` and asserts the *rendered* card line — the
check is provably wired, not merely correct in isolation. Mutants proven red:

| mutant | arm that catches it |
|---|---|
| drop the `seen[k] != v` guard | (1) a plain re-export reads as a conflict |
| tolerate a leading `#` (**both** the awk pattern and the prefix `sub()`) | (3) commented-out archaeology counted as live |
| `return 0` instead of `return 2` on a missing `restore.env` | (7) a node that could not be asked reads COHERENT |
| delete the render line from `refresh()` | (9) no `identity-coherence:` line at all |

Mutant (ii) is recorded as **compound on purpose**: loosening only the awk pattern makes a comment
yield the mangled key `# MESH_A_CMD`, which collides with nothing — the arm would pass *for the wrong
reason*. Both edits together are the realistic slip.

`--test` runs in 5.3s, inside the `timeout 30` doctor/autowire impose.

## Not fixed here (deliberate)

- **The 19 conflicts themselves.** `restore.env` is a runtime, gitignored, operator-owned surface;
  deleting a dead `MESH_HEALTH_CMD` line is a substrate edit for the operator, not a genome change.
  The detector's job is to make the count visible. It is now on the card.
- **The card was 11 days stale** (`as-of: 2026-07-24`) despite `mesh-card-watchdog.timer` claiming a
  15-minute cadence. Noticed while producing the artifact; separate finding, worth its own `[task]`.

## Left in the tree

Uncommitted, per the task contract (steward lands): `scripts/mesh-card`, this file. The deployed
`~/.local/bin/mesh-card` is untouched — the live card line above was produced by running the genome
copy directly, and will not persist until this lands and `mesh-sync-tools` deploys it.

**Still unembodied from TOP** (next VSM review candidates): **I1–I4 structural** — vertical unfolding
and recursion-level completeness (is each mesh recursion level itself a complete S1–S5?); **II4
inadequate representation vis-à-vis higher levels** (S5↔S5 across recursion levels — a node's identity
failing to propagate to the fleet); **II14/II16 autopoietic "beasts"** (a subsystem growing at the
expense of the whole); **II1 ill-defined identity** and **II3 S5-collapses-into-S3**.
