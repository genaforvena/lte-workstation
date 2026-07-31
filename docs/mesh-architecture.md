# Mesh Architecture — reasoning about the whole

This is the map you read to hold the mesh in your head at once: how the pieces
(tmux, panes, the board, hledger, reflexes, the uxn lane, the verification doctrine)
fit into one organism. It is a **synthesis** doc — every subsystem has its own deeper
reference (linked inline); this one exists so you can reason about how they compose.

If you read only one thing first, read [`mesh-skeleton.md`](mesh-skeleton.md) (what a
mind is) and [`coordination.md`](coordination.md) (how minds share a substrate). This
doc sits on top of both.

---

## 0. The one idea

**There is no fixed mind.** A *mind* is any node running an agent; a *node* is any
machine on the Tailscale mesh. Run `hostname` to know which body you are in. The mesh
is not a program with a control plane — it is a set of nodes that each keep their own
durable memory (`~/.mesh-card`), talk over a shared append-only log, and tend
themselves and each other through scheduled reflexes.

Three properties fall out of that and explain almost every design decision below:

1. **The scrollback is memory.** State lives where you can see it — in tmux panes, in
   the board log, in on-disk cards and journals — not in an agent's head. Anything not
   written to a shared surface does not exist to the rest of the mesh.
2. **Every claimed capability must produce a real artifact.** Not "the camera works" —
   a non-zero JPEG. Not "the gate passes" — a gate you have *watched go red*. This is
   the **verification doctrine** (§8), and it is the mesh's deepest recurring theme.
3. **The mesh produces itself.** It writes its own tools, wires its own reflexes,
   measures its own consumption, and heals its own substrate. Autopoiesis (§10) is not
   a feature bolted on; it is the operating mode.

---

## 1. Nodes, cards, capabilities

A node is described by two files:

- **`~/.mesh-card`** — the durable, current-state card. `mesh-card --refresh`
  regenerates it from live state and checks the substrate invariant (§11). This is the
  node's authoritative self-description.
- **`~/.mesh/traces.log`** — the volatile history tier (`mesh-trace`), where substrate
  changes and claims are recorded.

Nodes **self-declare capabilities** (opt-in by consumers, nothing imposed):
**minds** (agents) · **senses** (sensors) · **actuators** (act on the world) ·
**connectivity** (exit-node, ingress, uplinks) · **compute**.

**The card is authoritative.** A node whose `minds:` line lists no engine is
**HANDS-OFF** — the mesh must not relaunch, shed, kill, feed, or dispatch to its minds
at all. Blanking that line is the clean "minds off the mesh" switch. Every mind-touching
tool (`mesh-restore`, `mesh-mind-keepalive`, `mesh-channel-keepalive`) gates on the card
first, so a decommissioned node's panes are never even read.

Topology is **flat Tailscale reachability + node-local trace** — no central registry
(the old `vpn-hub` overlay is retired). Discover peers at runtime by filtering
`tailscale status --json` for `tag:lte-node`. Node-specific topology (IPs, roles,
services) lives in the gitignored `CLAUDE.local.md`.

**This node (mesh-home)** is *mind-home* — it runs the full mind channel set + a GPU
(RTX 3060) that is the mesh's first real local-inference organ (STT/TTS/small-LLM). See
[`what-is-a-node.md`](what-is-a-node.md) and [`distributed-embodied-agent.md`](distributed-embodied-agent.md).

---

## 2. tmux — the sensorium

**All observation of a node goes through its tmux session.** The agent runs in a
**hostname-named** session (`tmux new-session -A -s "$(hostname)"`). Other operators —
human or agent — attach and share the same terminal state. Attaching is joining.

Two rules make this load-bearing:

- **tmux is append-only.** Only additive changes: open windows/panes; never
  `kill-window` / `kill-pane` / `kill-session` / `clear-history`. The scrollback *is*
  the node's recent memory; the only intended decay is reboot (clean reincarnation:
  same hostname + card, fresh session).
- **tmux is the only way to see into a node.** Never side-channel probe (`ps`, ad-hoc
  SSH) to infer what an agent is doing — that leaves no shared record. Look with
  `mesh-tell --peek <win>`; wait with `mesh-watch <win> --until <pat>|--change`. Run
  commands *in* a node's windows so output lands in the shared scrollback.

**If the hostname session is missing on a node, restoring it comes first**
(`ssh user@ip "~/.local/bin/mesh-restore"`) — a node without its session is blind to
the mesh and the mesh is blind to it. On a freshly rebooted node the channel windows
don't exist until `mesh-restore` runs (the bootstrap gap: first deploy must go over raw
SSH, then `mesh-tell` works).

---

## 3. Channels & panes

A mind node's session is a uniform set of **2-pane windows** (channels). Each window is
named after its **role**:

```
┌─────────────────────────────┐
│  TOP  = DATA  (mesh-dash <role>, live-refreshing text)   │
├─────────────────────────────┤
│  BOTTOM = MIND  (the agent; runs its own shell ops here) │
└─────────────────────────────┘
```

**The mind pane IS the autonomous execution channel** — the mind both *thinks* and
*runs its own build/deploy/commit ops* there. There is no separate "shell" window.

**The data pane carries what the window is FOR.** If your mind keeps running the same
probe every turn, that signal belongs on top. The test: the mind should be able to act
from the pane alone, never re-fetching the same context. Extend `mesh-dash <role>` to
own the role's live surface; throttle expensive reads so the refresh loop stays cheap.
Hot-reload a data pane with `tmux respawn-pane -k -t <sess>:<win>.0` (never C-c it).

The current channel set (planted by `mesh-restore`, 2026-06-17 re-org — collapsed from
the old 10+ window sprawl):

| channel | engine | duty |
|---|---|---|
| `minds` | claude | orchestration / allocation |
| `genome` | claude | autonomous development of the codebase + its own build/deploy |
| `tg` | claude | operator Telegram comms |
| `senses` | opencode | keep + develop the senses |
| `health` | opencode | node/fleet health |
| `witness` | opencode | self-measurement **AND** board/room coordination (chat merged in 2026-07-24) |

`witness` carries **two duty classes**: on the TAPE (top) it is read-only and never
writes a measurement; on the BOARD (bottom) it *acts* — files `[task]` from chat-review,
drives stuck strands, is `mesh-mind-control`'s agentic fallback. A merge that leaves only
the passive charter creates a dead lane.

**Drive any mind without blocking** by sending to its window:
`mesh-tell <window> "<prompt or op>"`, then `mesh-tell --peek <window>` to read what
landed. This is the standard autonomous pattern; no operator needed for routine ops.

---

## 4. The board — coordination as a shared log

**The rendezvous is the LOG, not a window.** `~/.mesh/chat.log` (written by `mesh-chat`
from every window) is where minds talk *to each other* instead of scanning each other's
panes. One room per node; the durable trace (`traces.log`) is separate.

The board is a **free-form marker log** (no schema on the wire — see the proposed tag
schema in [`design-board-tag-schema-2026-07-24.md`](design-board-tag-schema-2026-07-24.md)):

- `[task] <what>` — an open job. Optional `owner: <tool>/<window>` routes dispatch by
  the post-slash window; `priority:incident` wins the next pace-released slot.
- `[taking] <slug>: <what>` — a claim that stops double-dispatch. **Must reference an
  open `[task]` slug** — it is a claim, not a sign of life.
- `[done] <slug>: <result + cite>` — finished, with commit/file.
- `[verify]` — an **open** claim for *another* window to check (a self-completed check
  posts its result as `[fyi]`/`[sense]`, so the verify scan stays a worklist of open
  claims, not a graveyard of settled ones).
- `[fyi]` / `[design]` / `[chat-review]` / `[handoff]` — context / proposed approach /
  flagged defect / pre-`/clear` work-state snapshot.
- `[heartbeat]` (alive & orienting) / `[idle]` (nothing open — one line, a status yield,
  never a parking lot for a multi-line report).

**A claim that never settles is a leaked promise** — structurally a JS Promise that
never resolves: it holds the awaiter's scan budget forever and ages where nobody is
looking. This is the bridge to hledger (§5): the board's obligations are modeled as a
**standing liability balance** so a leak becomes a queryable quantity instead of a line
that scrolled away.

---

## 5. hledger — coordination as double-entry bookkeeping

> Full design: [`design-hledger-coordination-2026-07-24.md`](design-hledger-coordination-2026-07-24.md).
> Buildable spec: [`superpowers/specs/2026-07-24-hledger-reactive-coordination-design.md`](superpowers/specs/2026-07-24-hledger-reactive-coordination-design.md).

The operator's move: put **hledger at the center of coordination**, not off to the side
as $-accounting. Treat the board as a first-class ledger. Coordination questions become
one-line queries (`bal`, `register`, `tag:`) instead of greps.

**The real payoff is the error-detecting code, not the metaphor.** Every commodity
shares one invariant:

> Two independent computations of "what's open" — a Python replay of the board vs. an
> `hledger balance` on the materialized journal — must AGREE. A divergence means the
> journal was corrupted or hand-edited.

That is a **free structural checksum** on every ledger, plus double-entry parity
(`hledger check` — every transaction sums to zero) catching feeder bugs with no external
oracle. Same shape as the verification doctrine: an artifact that balances against
itself. Each tool has a RED-first `--test` (a gate you have watched fail on an
unbalanced transaction).

Three parallel ledgers, each its own commodity, journal, and git repo (never mixed):

| axis | tool | commodity | books |
|---|---|---|---|
| **money** | `mesh-ledger` | USD | imputed inference $ + energy + depreciation |
| **promises** | `mesh-promises` | PROMISE / CLAIM / HOLD | board obligations; unkept = leak |
| **labour** | `mesh-labor` | TURN | mind turns, rolling 5h budget |

The framing is deliberately Marxist: *stop thinking money; think LABOUR.* The unit the
mesh actually spends is labour-time (mind compute); a **TURN** (one provider round-trip)
is the abstract labour quantum — "genome's coding, tg's talking, a sense's classifying
all reduce to the same fungible TURN."

### 5a. mesh-ledger (USD)

Books the real token flow priced to USD. `expenses:inference:<prov>:<model>` (Dr)
against `assets:budget:{paid|imputed}:<prov>` (Cr). Honesty distinction: flat-plan/free
providers (Anthropic, z.ai) are booked as **imputed** market value ("what this compute
*would* cost metered"), never faked cash; only a genuinely metered pay-go cost books
`paid`. Energy folds in as **real cash** (watt samples → kWh → `$ELEC_RATE`);
depreciation is straight-line from a capex manifest. Each feed is ONE balanced
transaction, tagged `window:<start>..<end>` for idempotency, guarded by a **parity gate**
(refuses to write if `hledger check` fails) and **window reconciliation** (feed windows
must tile without overlap — overlap = double-book).

### 5b. mesh-promises (PROMISE / CLAIM / HOLD)

The board's leak detector. A promise is a **liability**; keeping it is the balancing
posting:

- `[task]` opens `liabilities:promises:<owner>:<slug> +1 PROMISE`.
- `[done]` books the reverse, netting the account to zero.
- Therefore **`hledger bal liabilities:promises` = the current open set.** An
  obligation open-but-not-discharged is a **nonzero, aged, queryable balance** — that
  *is* the leak detector. A leak = an open promise past threshold (default 24h;
  incidents 6h).

The **claim family** exists because the two leakiest board shapes had zero visibility to
a `[task]→[done]`-only detector:

- **CLAIM** (`[verify]`) — a check *owed* by an addressed window (debtor parsed from the
  `A→B:` / `A/B:` / bare-`A:` address form), redeemed by a later `[fyi]`/`[sense]`/`[done]`
  from that debtor. An **unaddressed** `[verify]` routes to
  `liabilities:claims:reflex-broadcast` — a structural dead-letter that can never be
  redeemed (no window posts *as* reflex-broadcast), so it ages loud forever. That is the
  signal for the sharpest leak class.
- **HOLD** (`[taking]`) — a claim held on a task by its taker; only a *slugged* taking
  opens one (a content-free `[taking]` is a heartbeat, not modeled), redeemed by a
  `[done]` from the same taker.

`--check` runs three gates: parity, no-negative-liability (a keep with no open = phantom
over-discharge), and agreement (Python replay == `hledger balance`).

### 5c. mesh-labor (TURN) — the axis the operator wants central

The double-entry ledger over `~/.mesh/spend.log` (the turn stream). `expenses:labour:<prov>:<window>`
(Dr) / `assets:budget:<prov>` (Cr), priced "in nothing but itself" (no USD conversion).
Adds parity/agreement checking, a git audit trail, and:

- **`--budget`** — the rolling `[now-5h .. now]` window (sub-minute precision hledger's
  day-granular dates can't give): spent / cap / remaining / burn / projected exhaustion.
  A mesh rate-limit readout. Cap **unset → report-only** (an invented cap is a faked
  constant).
- **`--branch <slug>`** — a board task's labour cost = its owner-window's turns
  intersected with `[open .. done]`. Guards `0` carefully: 0 is "no data," not "cost
  nothing," when the window wasn't sampled (the silent-fallback trap).
- **`--availability`** — per-window remaining TURN = the **routing denominator**
  (`score = relevance × availability`). No cap ⇒ null ⇒ routing falls back to FIFO.

`mesh-spend` is the raw sampler that *writes* spend.log. Its known trap: it must
enumerate **live tmux windows**, not the static map — the 2026-06-17 re-org renamed
windows and a map-driven loop left `genome/minds/witness/…` at zero turns however busy
(a hollow meter that fed a false 0-TURN `--branch` cost).

### 5d. How the axes compose

The "board as a game" model: the board is the rule book, a marker line is a move, the
journals are the materialized score, the mind-windows (in `accounts.journal`) are the
players. `hledger check` + the replay-vs-balance agreement is the score-check that fails
LOUD. All three axes surface **side-by-side on the witness top pane**. They
cross-reference: `mesh-pace` reads `mesh-labor --json` burn to gate wake timing;
`--availability` is the routing denominator; the labour ledger is the evidence for the
idle-cron-burn audit (a TURN with no `[task]` = wasted labour).

**One sharp limitation** (`accounts.journal`): `hledger check --strict` requires each
full account path declared, and a declared parent does *not* license subaccounts. Both
liability and labour trees have a **dynamic segment** around the window leaf
(`…:<window>:<slug>`), so `--strict` can't validate it. The window-membership check is
therefore enforced in **Python**, deliberately **fail-open** (an absent
`accounts.journal` disables the check rather than nuking every promise to `:unrouted`);
non-roster owners route to a visible `:unrouted` quarantine, never a phantom.

---

## 6. Reflexes — scheduled self-tending

A **reflex** is a scheduled tool that keeps some invariant true. Reflexes are the mesh's
autonomic nervous system: liveness (`mesh-tick`, `mesh-heartbeat`), health
(`mesh-health`, `mesh-reflex-health`), coordination feeds (the hledger `--feed` ticks),
board sync (`mesh-chat-sync`), and channel keepalive.

**Self-wiring via `# reflex-cadence:`.** A tool declares its own cron cadence in its
header:

```bash
# reflex-cadence: */30 * * * *
# reflex-args: --check
```

`mesh-autowire` reads that header and — *after a passing `--test`* — wires it into
`~/.mesh/reflexes.cron` (→ `mesh-reflexes --apply`, add-only, one line per tool name).

Reflexes are guarded by hard-won rules (all §8 verification-doctrine cases):

- **A reflex that passes `--test` is not a reflex that runs.** Passing and being wired
  are unrelated facts — check the tool is actually in cron *and* has a target that
  exists (a reflex tending a phantom window is permanently green and vacuous).
- **A step everything depends on needs its own unconditional cadence.** The genome push
  once rode inside conditional paths (`--autoland` exits before it; `--apply` pushes only
  its own commits), so 55 commits sat local 11h and the *operator* noticed before any
  reflex did. A load-bearing step must not be conditional on some other run having work.
- **Liveness-touch convention.** A reflex that rewrites its state artifact *only when the
  value changes* leaves mtime frozen on a stable-but-live value → mtime-aging watchdogs
  misread it as dead. Decouple ran-live from value-changed: `mesh-state-touch` on *every*
  successful eval (mtime = liveness), content = the change-gated write.

Some tools are **intentionally unwired** (invoked manually, node-specific, or test
harnesses). CLAUDE.md's "On-demand canon" section lists them, and `mesh-doctor`'s orphan
check reads that section — so an orphan WARN keeps meaning "built to be wired but isn't"
instead of drowning in intended-unwired tools.

---

## 7. Context management — surviving the /clear

A mind's pane context window is its scarcest resource. Three levers, in order of use:

1. **Subagents spend context outside the pane.** Delegate heavy-context work (broad
   searches, multi-file audits, long log reads, independent parallel fixes) to the Agent
   tool — only the *conclusion* comes back. Boundaries: substrate stays in the mind's own
   hands (a subagent is a second writer nobody can see); the board is the mind's voice
   (subagents return findings, the mind posts); a subagent's report is a **claim, not an
   artifact** (verify before acting — "my subagent says the tests pass" is the same
   sentence as "the camera works").

2. **The handoff survives `/clear`.** `/compact` is retired mesh-wide; `/clear` + handoff
   is the one context lever. Before any `/clear`, write
   `mesh-handoff <window> "<done> + <next> + <key paths>"` — it posts one `[handoff]`
   board line **and** writes durable `~/.mesh/handoff/<window>.md`. The SessionStart hook
   (`mesh-handoff --restore`) cats that file back into the freshly-cleared session, so
   the mind wakes holding its own thread. A bare `/clear` that drops uncommitted
   work-state is a fault.

   `mesh-clear <window>` is the **gated** `/clear`: it refuses unless a handoff exists,
   is fresh (< 900s), *and* a tiny local model (`gemma4:e2b-it-qat`, the benched winner)
   confirms the handoff covers the recent scrollback. Strictly **fail-safe** — model
   unsure/unreachable → BLOCK, never auto-clear (a false all-ok loses the thread
   irreversibly). Every clear is logged to `mesh-clear-log` so clears are fixed by
   numbers, not blind.

3. **A ScheduleWakeup (loop) survives `/clear`** (measured). This makes an interval
   `/clear` mid-task safe: the handoff restores state, the wakeup restarts motion — clean
   context *and* finished tasks. Rules: **task-scoped only, never an idle heartbeat**
   (stop it the moment you post `[done]`/`[yield]`); the wakeup prompt carries the pointer
   and the handoff carries the detail; a pending wakeup is **invisible state**, so it does
   not survive an engine restart — cron reflexes remain the liveness guarantee, the loop
   is only an accelerant.

---

## 8. The verification doctrine — the deepest theme

Every claimed capability must produce a real artifact. This started as "not 'the camera
works,' a non-zero JPEG" and has generalized, through repeated live failures, into a
family of traps that all share one shape: **something that looks like evidence but
asserts nothing.** The canonical cases (each with a commit) are the mesh's most-cited
institutional memory:

- **The silent fallback.** `cmd 2>/dev/null || echo <default>` turns total failure into a
  plausible constant. `mesh-room-music`'s beat detector ran under a python with no numpy →
  import raised → `|| echo 500` → every render used the flat fallback for weeks; only the
  params log showed it. *A fallback must be rare and loud; if a default is
  indistinguishable from success, it will be one.*
- **The test that never fails.** A gate you have not seen fail is not a gate — break the
  fix, watch it go red, restore it. The **self-grep** is the archetype: `grep -q '<literal>' "$0"`
  always finds the grep line itself; 33 of 52 liveness gates could not go red.
- **The test that forges the artifact.** A `--test` must never write to the log a human or
  watchdog reads for liveness — `mesh-guardian`'s dry-run wrote its mock peer into the real
  log, and the reflex had never actually run.
- **The proxy that is not the claim.** `[ -x "$BIN" ]` is not "it runs" — whisper.cpp's
  binary was executable and died rc=127 for a day (rpath patched on `main` but not the
  libs). *Executable and loadable are different claims.* A wrapper's test must exercise the
  thing it wraps.
- **The reachable-but-hollow sense.** A phone that answers but whose driver returns
  empty/cleanup-noise is cron-green while its state goes stale for days. `--test` must
  assert a *real read produces data* (≥N axes / a parseable value), not just exercise the
  offline classifier.
- **The predicate that names a node/window.** A guard bound to `TG_HOST="imozerov-…"` went
  permanently false when minds migrated; the keeper never ran and Telegram sat unread while
  every pass logged green. Bind guards to the *thing itself*, never to a name that ages out;
  make the else-branch say *why* it skipped.

The through-line into the rest of the architecture: hledger's parity/agreement gates
(§5), the uxn ROM-vs-twin cross-check (§9), and the reflex-wiring rules (§6) are all the
*same doctrine* applied to different substrates — assert the artifact, not a proxy for it;
never let a default be indistinguishable from a success. See the dev.to drafts
([`devto-vacuous-pass-draft.md`](devto-vacuous-pass-draft.md),
[`devto-self-nullifying-draft.md`](devto-self-nullifying-draft.md)) and
[`epistemics.md`](epistemics.md) for the essay-length treatment.

---

## 9. The uxn lane — gates as data

> Full reference: `scripts/uxn/README.md`. The "why" essay:
> [`research-uxn-gates-as-data.md`](research-uxn-gates-as-data.md). The claims sweep:
> [`uxn-doctrine-claims.md`](uxn-doctrine-claims.md).

**The problem the lane solves is not "we need a VM."** It is §8's deepest instance: *an
operational predicate you cannot trust* — checks that can never go red, and thresholds
whose provenance is written nowhere. The one-line claim: *a predicate as a hash-pinned
bytecode, cross-checked against a native twin at the boundaries, honestly refusing to
answer outside its domain.*

Uxn is a tiny stack VM (Varvara is its device model) from Hundred Rabbits — a ~43 KB C89
emulator with no deps beyond libc. The mesh vendors it plus `uxnasm` and `chibicc` (a C→
uxntal compiler) because it makes **byte-identical cross-architecture execution cheap**.

Two data planes replace the shell gate:

- **Gate logic lives in a ROM, not a bash line.** A predicate compiles to a few hundred
  bytes (`lease-gate.rom` 200 B). The host shim is ~20 lines of pure I/O — it does no
  arithmetic. RED-first proof: break the guarded config and the self-grep gate stays GREEN
  while the ROM goes RED; corrupt the ROM's arithmetic and the bug wrongly passes —
  proving the ROM does the work, not a constant.
- **Thresholds live in a ledger, not inline.** `scripts/uxn/threshold-ledger` — 22 rows of
  `name | params | consts | s-expression`, run by a hash-pinned evaluator (`lisp-eval.rom`).
  Recalibration is a diff of the consts column, not a code edit. Resolution order
  `env > ledger > inline-fallback` (a missing ledger degrades to prior behaviour). 17 live
  mesh tools resolve defaults through it.

**ROM + 64-bit twin — the reduce-a-series class.** A gate answering a boundary is a
*decision*; a gate reducing a whole series to one calibrated number is a *measurement*.
The ROM owns the reduction and its domain; a genuinely different 64-bit awk twin
cross-checks it, so an AGREE is evidence about arithmetic *and* ordering.
`mesh-series-stats --claims` re-derives every standing doctrine number (e.g. the sound-corpus
medians, §12) from the live ledger with the ROM and twin side by side —
because the corpus is a **sliding window**, any `n=` quoted in prose is stale before it is
committed, so claims must cite the gate's current answer, not a pinned constant.
`mesh-rom-calibrate` (cron `7 6 * * *`) is the general oracle: runs both implementations on
identical inputs and posts `[chat-review]` loudly on disagreement, logs agreement silently
(keeping the N-version-diversity signal that ROM uniformity would destroy).

**The net device — where §8 bites hardest.** A `0xd0` Varvara device adds addressed
sockets to the emulator so a travelling ROM can pick its own next hop and the far node
needs only `uxncli` — no shell. Two idioms are load-bearing:

- **"bind state read IS the accept."** The state-register read is the one poll that
  deliberately *blocks* until a peer arrives (the vector-less equivalent of an arrival
  callback). So you must *not* check "did it bind?" by reading state — that read consumes
  the wait and reads a healthy bind as a failure.
- **"absent device reads as a plausible state."** On an emulator with no `0xd0` page, the
  device read falls through to bare memory = 0 = `Disconnected` — so *"this build has no
  network"* and *"the far node refused"* arrive as the same byte. The fix is an **identify
  probe** (a write memory cannot fake) compared as an ordering, making three outcomes
  distinct where they were one. An unimplemented port refuses *loudly* rather than
  answering a plausible state — "an organ declared before it was armed."

**The hop trampoline — "hop-serve BECOMES ROM."** `hop-serve` binds, accepts one caller,
reads a `uxp1` packet header one byte at a time (a bulk read would swallow the payload it
is about to become), then a position-independent copier relocates the arriving ROM and
jumps into it. It works because **the socket lives in the emulator's device page, not the
64 KB being overwritten** — the arriving ROM wakes holding a live connection. Payoff: mesh-home
ships a ROM over TCP to a 2013 Note3 carrying only a static `uxncli` (no shell, no ssh)
and the phone's emulator *becomes* the code and answers.

**Deploy via shim, never copy.** The ROM is never rebuilt per node; only the emulator is
per-platform (`cross-build.sh`, static-linked). Host-tool logic + tests live in
`scripts/uxn/`; a thin deploy shim in `scripts/` carries only the cron header.

**Meta-detectors are blind to the lane by construction** and had to be taught its shape:
`mesh-fitness`'s size-bloat proxy counted only the tool file (0 inline asserts by design)
and false-flagged every ROM dispatcher — fixed to count asserts across the sibling
`test-<name>` harness too ("an assert the proxy cannot see is not a missing assert"). The
unifying reason: the detectors assume logic *and* its assertions live inline in one shell
file; the uxn lane deliberately splits logic into a hash-pinned ROM, thresholds into a
ledger, and assertions into an external truth-table + native twin.

---

## 10. Autopoiesis — the mesh producing itself

Two production lanes plus a meta-layer:

- **Codebase lane:** `mesh-generate` → `mesh-feed` → the genome. New tools are proposed,
  fed through the pipeline, landed via `mesh-land`.
- **Perception lane:** `mesh-sense-evolve` grows the sensorium.
- **Meta-layer:** `mesh-vitality` (do the lanes produce?), `mesh-needs` (goals
  self-derived), `mesh-fitness` (is what they produce sound?), `mesh-autowire` (do
  products integrate?), watched by `mesh-reflex-health` (do the lanes fire at all?).

The genome (`scripts/`) is the **source of truth**, deployed to `~/.local/bin/`;
`mesh-sync-tools` flags drift. Landing is `mesh-land` (settles a fix, gated), and the
unconditional push cadence (§6) is what actually gets the genome onto origin. See
[`docs/self-organization.md`](self-organization.md), [`genome-audit.md`](genome-audit.md),
and [`study-2026-07-24-autopoiesis-self-optimization.md`](study-2026-07-24-autopoiesis-self-optimization.md).

---

## 11. The substrate invariant — the one contended resource

Sensors and compute are a **commons** — mark freely. But the **substrate** (routing,
`ip rule`/`ip route`, DNS, default route, `iptables`/`nft`, WireGuard, the SSH path) is
**single-writer and contended**: one routing table per node, and a bad edit severs the
path you reach the node through.

The protocol before any substrate change: **Detect** other operators → **Claim** on the
shared trace → **Coordinate via tmux** (one writer at a time) → **Apply under `mesh-dms`**
(schedule the rollback *first*, cancel only after `mesh-health` + `mesh-card --refresh`
confirm the invariant).

**The substrate invariant:** a node that *offers* a route (exit-node, VPN egress) never
carries its **own** control plane on it. The host stays on the clean default route; only
forwarded client traffic rides the offered route, and the forwarding mark must *exclude*
LAN/private ranges + Tailscale CGNAT. `mesh-card --refresh` flags violations. This is the
same doctrine as §8 applied to networking: the artifact for a network change is *every
node still reaches the internet and the LAN*, captured before and after — not "the
interface came up." Full protocol + worked example: [`coordination.md`](coordination.md).

---

## 12. Perception, fusion, and the sound studio (in brief)

- **Perceive:** location, motion, light, presence, room-sense, voice — re-observed live,
  never stored (decays on reboot). Honest-fusion rule: an unreachable input renders
  UNKNOWN/partial, never a faked all-clear.
- **Fusion:** `mesh-situation`, `mesh-sensorium`, `mesh-home-state` derive higher-order
  state from the raw senses.
- **Metabolism:** `mesh-relay` (text → cheapest-available inference pool → text; Groq
  primary + local-mind fallback).
- **Sound studio:** records → grind. `mesh-records` (the archivist, ledgers every record
  before its organ prunes it) → `mesh-sound-reflex` (the grinder) → `mesh-room-music`. Its
  own §8 lesson: *check what your ranker selects for, not just that it ranks* — the
  `mesh-soundscape` score's heaviest term is `dyn`, so its top end is anti-correlated with
  the beat-density every consumer actually wants (a cough scored 65 and poked a paid turn);
  fixed with a rhythm-density floor. And *calibrate a derived axis against the real corpus,
  never an assumed 0..1* — medians pinned as constants rot as the sliding-window corpus
  turns over (hence `mesh-series-stats --claims`, §9).

---

## How it all fits — the metabolic loop

The pieces form a closed loop, not a stack:

```
   perceive ──▶ board (mesh-chat)  ──▶ minds act in panes ──▶ genome/senses grow
      ▲              │  obligations              │  turns spent            │
      │              ▼                           ▼                         │
   reflexes    hledger ledgers            handoff / clear            mesh-land
   (autonomic) (promises·labour·money)    (context survives)         (deploy)
      │              │                           │                         │
      └──────────────┴───────── verification doctrine ────────────────────┘
                        (assert the artifact, at every layer)
```

- **tmux panes** are where minds see and act; the **board** is where they coordinate.
- **hledger** turns coordination into a checksummed quantity (what's owed, spent, open).
- **reflexes** keep the whole thing alive without an operator, and **autopoiesis** grows
  it.
- **The verification doctrine** is the mortar in every joint — every gate, feed, and
  reflex must assert a real artifact, because a default indistinguishable from success
  *will* become one.

There is no fixed mind, no control plane, no single source of truth beyond the artifacts
themselves. Reason about the mesh by asking, at any layer: *what artifact proves this,
and have I seen its gate go red?*
