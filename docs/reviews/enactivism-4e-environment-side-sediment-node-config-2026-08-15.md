# Enactivism & 4E — the ENVIRONMENT-SIDE support structure, and the norm sedimented in it

**Landed:** `scripts/mesh-doctor --sediment` (report-only, on-demand, not wired) · 2026-08-15 · genome mind

## The source (live literature, read in full)

Marta Pérez-Verdugo & Xabier E. Barandiaran, **"The Equilibration of Technical Objects: Uncovering
Normative Layers of Sensorimotor Engagement"**, *Topoi* **45**(2):331–342 (2025),
doi:[10.1007/s11245-025-10259-4](https://doi.org/10.1007/s11245-025-10259-4). Received 25 Feb 2025,
accepted 7 Aug 2025, open access (CC-BY). Read from the authors' own open copy —
`https://publications.barandiaran.net/pdfs/2025-the-equilibration-of-technical-objects-uncovering.pdf`
(PhilArchive's copy 403s to a scripted fetch; the Springer landing page redirects to an IdP).
IAS-Research Centre for Life, Mind and Society, UPV/EHU — the same lineage as `Sensorimotor Life`
(Di Paolo, Buhrmann & Barandiaran 2017), which prior mesh landings on this area already cite.

The operational content, verbatim where it matters:

- Sensorimotor schemes "are not internally represented, but sustained by distributed support
  structures, both **agent-sided** (neuromuscular, postural, sensory) and **environmental** (arrays,
  densities, forces, material compositions, etc.)".
- Therefore "the equilibration of behavioural structures can take place through agent-sided
  transformations, **but also — and this has been less explored — through transformations of the
  environment itself**". That second kind is **technical behaviour**: "we behave technically when we
  actively transform and organise elements of our body and environments with the intended effect of
  constraining or regulating couplings with (or between) other aspects of the environment."
- The product of technical behaviour is a **technical object**, and its crucial feature is that it
  "typically **survive[s] the interaction that [it is] intended to regulate**, while retaining in
  [its] structure the effects of the transformations [it has] undergone… a certain normativity is
  **sedimented in their material structure**". It keeps regulating whoever encounters it next, after
  the perturbation and the agent that answered it are both gone.
- Encounter is then sorted by Piagetian **assimilation / accommodation**: a **canonical** use when
  the new agent's network of schemes resembles the one the object was designed to regulate, an
  **alternative** use when it does not (their example: a teapot repurposed for Ayurvedic nasal
  cleansing). Alternative use is *not* a defect — the paper insists artifacts stay "multistable" and
  the object holds a "**virtuality of use**": it "is designed to regulate virtual (as in non-actual)
  uses".
- Their QWERTY case is the sharp end: "material constraints in the form of frequent typebar clashing
  made QWERTY an effective layout. But soon, with improvements in design, **those initial constraints
  went away**… However, the QWERTY layout is still the standard." The sediment outlives its cause.

## What the mesh already embodies (checked in-genome first, discarded)

Everything the mesh has built on this axis is **agent-side**:

| already have | the sediment it detects | side |
|---|---|---|
| `mesh-doctor` orphan check | a tool built to be wired that nothing schedules | agent |
| `mesh-closure --enacted` (uncommitted, same morning) | an enablement edge no code exercises | agent |
| `mesh-reflex-health --routine-fit` | a declared cadence the world does not run | agent |
| `mesh-sync-tools` | genome vs deployed drift of tool *code* | agent |
| `mesh-fitness` / `mesh-vitality` | whether the production lanes fire and produce | agent |
| memory `a-constant-outlives-its-reader` | a constant inside code whose reader changed | agent |

Also checked and set aside as **not this**: `mesh-autowire` (integrates products, does not audit the
environment), `mesh-card --refresh` (asserts substrate invariants, never reads config *keys*),
`mesh-verify` (reboot survival), `mesh-doctor`'s own umwelt-check (a producer vs its declared output).

The mesh has **no instrument at all for the environment side** — and its environment-side support
structure is not small. `~/.mesh/nodes` is sourced by **149 tools in `scripts/`**; it is gitignored,
node-local, survives every reboot and every `/clear`, and almost every line carries in its trailing
comment the perturbation it answered ("Termux user drifts on reinstall", "released VM — resolvable but
not reboot-managed", "no consumer tunnel on this node BY DESIGN"). That file is a technical object in
exactly the paper's sense: hand-transformed by past operators and past minds so that existing schemes
keep working, and then left in the world to regulate whoever sources it next. Nobody has ever asked
whether its knobs still regulate anything.

## The mechanism: `mesh-doctor --sediment`

Report-only, on-demand, never edits the file. Unit = each knob **set** in `~/.mesh/nodes`.

**Axis 1 — does the sediment still regulate?**

- `UNREAD` — no reference in any scanned surface (genome `scripts/`, deployed `~/.local/bin`,
  `~/.config/systemd/user`, `~/.mesh/reflexes.cron`, `crontab -l`). A norm sedimented in the
  environment that regulates nothing.
- `REDUNDANT` — read, but **every** reference is `${K:-D}`/`${K:=D}` with **one** distinct `D`, and
  `D` equals the value set here. The transformation does no work; deleting the line changes nothing.
  This is the QWERTY shape: the constraint that produced the knob is gone (the reader's own default
  drifted to meet it), the sediment remains.
- `ACTIVE` — everything else.

**Axis 2 — canonical, alternative, or virtual?** A knob also declared in the committed
`nodes.example` is `canonical` (the use the object was designed to regulate); one only on this node is
an `alternative` use — **descriptive, not a fault**, per the paper's multistability; one declared in
`nodes.example` and unset here is an unactualized **virtuality**.

Design choices that carry the weight:

- **A comment mention is not a read.** Full-line comments are stripped from the reader corpus before
  counting — the same rule `mesh-closure --enacted` had to learn hours earlier, arrived at
  independently here (the two UNREAD keys below are named in *nothing but* past mind transcripts).
- **An assignment is a write, not a read.** `K=x` in a script (a `--test` fixture pinning it, a tool
  exporting its own fallback) is not the world consulting *this file's* value. Subtracting assignments
  is what lets a knob whose only real reader is `${K:-D}` reach `REDUNDANT` at all.
- **Conservative in both directions on `REDUNDANT`.** One bare `$K` reference keeps the knob ACTIVE —
  under `set -u` an unset name is a crash, so a bare reader makes the knob load-bearing *at its
  default*. Two distinct defaults keep it ACTIVE — one of them is not the value.
- **`UNREAD` is a LEAD, not a verdict**, and says so in its own header line: a reader on a peer node,
  in a unit this node does not carry, or built by runtime name construction is invisible to a
  literal-name scan. The report measures `${!var}` / `eval` / `printf -v` presence **on the whole
  corpus before it is narrowed** (a built name is precisely what does not appear literally) and prints
  the caveat when the idiom is there — 266 lines on this node, so `UNREAD` **understates**.
- **No value is ever printed.** `~/.mesh/nodes` is the node's secret-adjacent surface (peer IPs, a
  chat id, device serials) and this report can reach a human, a log, or the board. Verdicts need names
  and counts only. That is a gate leg, not a habit (`s11`), because the natural next edit — "print the
  value so the reader can judge" — is a leak.
- Missing config → **exit 2** with an n/a line that is a claim about *this node* ("sediments no
  environment-side knobs"), not a silent green report.

## Live findings (mesh-home, 2026-08-15)

```
knobs set: 39 (canonical 10 · alternative 29) · disabled-in-place: 4 · unactualized in nodes.example: 22
verdicts: ACTIVE 36 · REDUNDANT 1 · UNREAD 2
UNREAD   PHONE_ADB_IP     alternative  prose-mentions=0
UNREAD   PHONE_ADB_PORT   alternative  prose-mentions=0
REDUNDANT MESH_VPN_NODE   alternative  reads=1 (all defaulted · one distinct default · = the set value)
```

- **`PHONE_ADB_IP` / `PHONE_ADB_PORT` are pure sediment.** Hand-verified past the tool: no reader in
  `scripts/`, `~/.local/bin`, user systemd units, `reflexes.cron` or the live crontab; `git log -S`
  finds them in **no committed tool or `nodes.example`, ever**; a home-wide grep finds them only in
  Claude transcripts and file-history — i.e. minds *discussed* them and never wired them. There is no
  `adb connect` anywhere in the genome. Two knobs were written into the node's environment during the
  ADB-over-WiFi work, and every one of the ~150 tools that sources this file has been inheriting them
  since, regulating nothing.
- **`MESH_VPN_NODE` is the QWERTY case, exactly.** Its single real read is `${MESH_VPN_NODE:-phaedra}`
  and the value set here *is* that default. The line was technical behaviour once; the reader's
  default has since met it, and the transformation now does nothing.
- **22 unactualized virtualities** in `nodes.example` vs 10 canonical knobs actually set — this node's
  use of the config object is overwhelmingly (29/39) **alternative**: the object as designed and the
  object as used have drifted apart. Not a fault; a measurement of how far the encounter has moved
  from the designed one, and the first time that distance has ever been a number.
- Incidental, **not this axis's claim** and left for its lane: `OH_MODEL` is set to the tiny model with
  a 2026-07-14 operator rationale in its comment, while `CLAUDE.local.md` records tiny as unusable as a
  transcriber (the room ear pins large in its unit instead). Both facts are on this node; nothing
  reconciles them. Flagged, not touched.

## Gate

13 legs (`s1`–`s13`), every one driving the real script (`"$0" --sediment`) against a fixture node
config — never a helper in-process, since the classifier being right proves nothing if the flag is not
wired to it. Legs cover: a live reader is ACTIVE and unlisted · a comment-only mention is UNREAD with
its prose mention counted · a nowhere-named knob is UNREAD prose-mentions=0 · defaulted-and-equal is
REDUNDANT and a *commented* declaration in `nodes.example` still declares it canonical · a divergent
value is not REDUNDANT · a bare reference keeps ACTIVE · two defaults keep ACTIVE · a value followed by
a second statement on the same line still compares equal · the census (8 set / 2 canonical / 6
alternative / 1 disabled-in-place / 1 unactualized) · the verdicts partition the set knobs · **no value
ever printed** · the name-construction caveat on **both edges** (silent without the idiom, loud with
it) · missing config = exit 2 and says n/a.

**7 mutants, all RED from a scratch copy**, each on a distinct leg: comment-mention counted as a read
(s2) · bare-ref guard dropped (s6) · multi-default accepted (s7) · value-stops-at-`;` removed (s8) ·
value printed (s11) · missing-config exit 2 dropped (s13) · disabled-key parse widened (s9). No-op
control green. `mesh-doctor --test` 0.95s → 1.2s; the report itself runs in 3.5s.

**Two defects the gate caught in its own construction**, both worth keeping:

1. **The first value-leak mutant changed nothing.** It injected `val=[$val]` into a *single-quoted*
   `printf` format, where `$val` never expands — the mutant "printed the value" and printed the literal
   string. It came back green and for a moment read as a vacuous leg; the real leak mutation (pass
   `"$val"` as the argument) goes red immediately. A mutant that does not do the thing it names proves
   nothing about the leg ([[a-shim-that-changes-nothing]]).
2. **The first live run mis-parsed a value and hid a whole verdict class.** `MESH_VPN_NODE` is set on a
   line that carries a second statement (`K=v; export OTHER=w`); taking the tail as the value made the
   comparison silently fail and the run reported `REDUNDANT 0` — a clean-looking green that was a
   parse bug. The value now ends at the `;` when unquoted, or at the closing quote when quoted.

## Honest limits

- The scan is **literal-name**; runtime-built names are invisible and the caveat says so.
- Readers on *other nodes* are invisible: this is a node-local instrument, and a knob unread here may
  be load-bearing on a peer that sources a copied config. `UNREAD` is a lead.
- An unquoted `#` inside a value is eaten with the comment. That can only mis-compare, and a
  mis-compare falls to `ACTIVE` — never to a false `REDUNDANT`.
- Nested defaults (`${K:-${OTHER:-x}}`) parse to a truncated default string, which fails the equality
  test → `ACTIVE`. Conservative in the safe direction.
- Genome and deployed copies of every tool are both scanned on purpose (a deployed-only tool may be
  the reader); the corpus is deduped so `reads=` is not double-counted.
- **Not wired.** Deleting a knob is the operator's call — `UNREAD` names a candidate, it does not act.
  `--sediment` is off the hourly path entirely (`mesh-doctor` with no argument is unchanged).

## Left open

The paper's third layer — Leont'ev/Engeström **activity systems**, where "tensions and contradictions
between levels… drive them to change" — is the natural next landing and is *not* implemented here.
The mesh-native form would be: a knob whose sedimented norm **contradicts** a norm asserted at another
level (the `OH_MODEL` observation above is exactly that shape: an environment-side sediment carrying
one operator instruction against a doctrine line carrying another). Detecting a contradiction between
layers is a different instrument from detecting a dead sediment, and it needs its own review.
