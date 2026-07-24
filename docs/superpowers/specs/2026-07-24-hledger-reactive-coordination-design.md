# hledger-centered reactive coordination — design (2026-07-24)

Operator direction (tg design session, 2026-07-24): put **hledger at the center of mesh
coordination**, replace mind-call crons with reactive board-event reflexes, define roles as a
chart of accounts, and make `chat.log` a proper hledger journal source. Supersedes the direction
capture in `docs/design-hledger-coordination-2026-07-24.md` (Directions 1 + 2) with a buildable
spec. Scope is **mind-call reflexes only** — the data plane keeps its crons.

## Thesis

The mesh already coordinates through the board (`~/.mesh/chat.log`): the `[task]`/`[taking]`/
`[done]` marker family. Treat that board as a first-class **hledger journal**, and make the ledger
the coordination substrate — so "who owes labour", "where is labour flowing", "what's unkept" are
one-line hledger queries, and a mind is woken **from a ledger event**, not by a cron tick.

The unit is **labour-time**, not money: a `TURN` (one provider round-trip) is the abstract labour
quantum. We already meter it — `mesh-labor --budget` reports per-window TURN balances on a rolling
5h window today.

**An unwired reflex is a liability.** A tool that *declares* a trigger (`# reflex-cadence:`, a
charter, an `AGENTIC_FALLBACK` naming) but has never been *seen to fire* is a promise with no
settlement — the never-wired-reflex / phantom-target / vacuous-gate family from CLAUDE.md. Double
entry makes it a queryable account (`debt:wiring:<tool>`) instead of a doctrine paragraph.

## Non-goals

- Not touching data-plane crons (sensor reads, records prune, health sweeps, path-watch, etc.).
- Not re-implementing turn booking. `mesh-spend`/`spend.log`/`mesh-labor` stay the meter; the
  reactor only **reads** the ledger. One meter, never two.
- Not merging windows or restarting the session — that reincarnation (minds→witness) is separate
  and already landed in `restore.env`.

---

## Component 1 — Board grammar (chat.log stays human, gains a schema)

`mesh-chat` is the single write choke point for the board and becomes the **grammar enforcer**.

**What it does:** validates *marker* posts against a tag grammar; passes *conversation* lines
through untouched.

**Grammar (marker lines only):**
- `[task]` — requires a `slug` and `owner:<window>` (the `owner: <tool>/<window>` post-slash form
  is accepted; the routed target is the post-slash window). Optional `prio:incident`, `turns:N`.
- `[taking]` / `[done]` — must lead with the task slug (`[taking] <slug>: …`).
- `[verify]` / `[fyi]` / `[design]` / `[handoff]` / `[heartbeat]` / `[idle]` — recognized markers,
  free-form body (no slug requirement).

**Enforcement is loud-reject, never silent-repair.** A malformed marker post is refused and printed
back with the specific reason (`missing owner:`, `[taking] with no slug`, `owner names retired
window <w>`). It is NOT auto-corrected — a silently-fixed post hides the producer bug (the
silent-fallback doctrine). Non-marker lines (plain conversation) are never validated and never
journalized.

**Interface:** unchanged CLI (`mesh-chat "<line>"`); new behavior is a validation pass before the
append. A `--lint` flag validates without posting (for producers to self-check). Exit non-zero on
reject.

**Depends on:** the account/window set (Component 2) to know which `owner:` values are legal.

## Component 2 — Chart of accounts = the window set (roles)

A committed accounts file `~/.mesh/accounts.journal` (source of truth in `scripts/`, deployed) is
the **role definition**. One `account` declaration per window, its charter as the trailing comment:

```hledger
account labour:tg        ; operator Telegram comms — talk fast, delegate real work
account labour:genome    ; autonomous codebase development + its own build/deploy ops
account labour:witness   ; self-measurement (tape, read-only) AND board/room coordination (acts)
account labour:senses    ; keep + develop the senses
account labour:health    ; node/fleet health
account labour:discover  ; missed-opportunity discovery, board→journal query surface
account labour:sound     ; sound studio — records, grind, room music
account labour:pub       ; public ingress / outward comms
account labour:vpn       ; egress / substrate connectivity
account labour:tg-roz    ; Rozalia channel
```

Parallel trees `promises:<window>` and `debt:wiring:<tool>` share the same window leaf-names.
Commodities: `TURN` (labour), `PROMISE` (obligations), `USD` (money — unchanged, mesh-ledger).

**Why window = account (not an abstract role layer):** today's windows already *are* the roles;
an intermediate role→window map is a table every query and every mind must carry. hledger validates
postings against declared accounts with `--strict`, so a post to a **retired or misspelled window
is a parse error**, not a phantom dispatch — the account file is the single roster, and
`mesh-restore`'s "never hand-maintain a count beside the roster" lesson applies: the accounts file
*is* the roster, queries count it.

**Two-duty windows (witness):** kept as a charter comment, not a sub-account, because most windows
have one duty and forcing every post to name a duty is friction. If witness's passive/active split
ever needs separate metering, it promotes to `labour:witness:tape` / `labour:witness:board` then —
YAGNI until measured.

## Component 3 — `mesh-board-journal` (the transformer)

New tool. Deterministically transforms marker posts in `chat.log` → `~/.mesh/board.journal`
(hledger format). hledger reads the *derived* file; the board stays a human one-liner tape.

**What it does:** reads new bytes since last run, emits one transaction per relevant marker:
- `[task] <slug> owner:<w> [turns:N]` → opens a `PROMISE` obligation on `promises:<w>` and (if
  `turns:N` present) a labour estimate; description carries `task:<slug>` and `owner:<w>` tags.
- `[done] <slug>` → settles the matching `promises:<w>` obligation.
- `[taking] <slug>` → status tag only (claim, not a booking).

**Offset tracking:** persists `(inode, byte-offset)` — NOT byte-offset alone. `chat.log` /
`chat-sync` can rotate/prune (the pruned-offset trap that bit room byte-offsets); on inode change,
restart from 0 and dedup by transaction key. Idempotent: re-running over the same input produces
the same journal (keyed by timestamp+slug+marker).

**Labour attribution** stays sourced from `mesh-labor` (spend.log), NOT invented here — the
transformer books *promises*; labour TURNs are the existing meter. `board.journal` + `mesh-labor`'s
view compose via hledger include, not a second labour count.

**Interface:** `mesh-board-journal` (incremental, default) · `--rebuild` (from byte 0, for repair) ·
`--check` (parity: every `[done]` matches an open `[task]`; unmatched = a leak, exit non-zero).

## Component 4 — `mesh-board-reactor` (wake fires FROM the ledger)

One long-running process. inotify on `chat.log` → run `mesh-board-journal` → for each **new journal
posting**, route a wake:
- new `[task]` → wake `owner:<window>` with the slug in the prompt.
- `[verify] <window> — …` / by-name mention → wake the named target.
- (Phase 2) threshold events: high-tokens → `mesh-mind-compact`; scheduled study window → study.

**Wake = `mesh-tell <window> "<slug>: <task body>"`** — lands in the pane, shared scrollback, the
mind acts. The reactor never does the mind's work; it only routes the wake.

**Pacing is an hledger query (the ledger IS the pacer).** Before waking window `<w>`:
- read `labour:<w>` TURNs over the rolling 5h (`mesh-labor --budget`, by-window).
- headroom vs the window's budget → wake now.
- exhausted → the event **queues**; picked up when the window's ledger drains. Queue order is
  **priority-then-oldest**: `prio:incident` wins the next headroom slot but **never mints one** —
  the spend hold stands, incidents win a released slot, they don't bypass the pace (the exact
  dispatch-hold rule today).

This makes pacing per-window-fair for free and keeps **one meter**: the reactor reads the same
labour ledger the tape shows, no private token-bucket state to disagree with it.

**Interface:** `mesh-board-reactor` (daemon) · `--shadow` (log `would-wake <w> slug=<s>
pace=<ok|queued>` and take NO action — the migration diff mode) · `--status` (queue depth, last
wake per window, pace state).

**Depends on:** Components 1–3 (grammar so `owner:` is trusted; journal for the events; accounts
for the roster). Runs on the mind node only (card declares `minds:`); early-returns HANDS-OFF
elsewhere.

## Component 5 — Watchdog pair (zero cron for minds)

Two systemd **user** units (linger already on this node), `Restart=always`:

- `mesh-board-reactor.service` — runs Component 4.
- `mesh-reactor-watchdog.service` — asserts three liveness artifacts every ~30s:
  1. reactor process alive (and its inotify watch is on the current chat.log inode);
  2. `board.journal` freshness — mtime not lagging `chat.log` mtime past a lease (the
     lease-exceeds-cadence rule);
  3. no `[task]` sitting **untaken** past an age bound (the event system produced an event and
     nothing consumed it).

On any fault: restart the reactor and post `[fyi] reactor-watchdog: <what> — restarted` **loud**
(the honest-fault rule — a silent restart is a hidden liability). The reactor **cross-checks** the
watchdog (asserts its unit is active) so a dead watchdog is itself visible, closing the
who-watches-the-watcher gap the "watchdog pair" choice accepts.

**This pair is the liveness guarantee that replaces cron.** It must be **seen red** before any cron
line is removed (Component 7).

## Component 6 — Wiring debt (unwired reflex = liability)

`debt:wiring:<tool>` — a standing `PROMISE`-commodity liability, opened when a reflex *declaration*
exists (a `# reflex-cadence:` header, a charter, an `AGENTIC_FALLBACK` naming) with **no observed
firing**, closed on the tool's first real fire.

- **Openers:** `mesh-autowire` (on wiring a declaration) and the reactor (on routing to a target)
  write the debt open; `mesh-reflex-health` reconciles.
- **Closer:** first artifact-confirmed firing (a state write, a board post, a ref move) settles it.
- **Surface:** the balance `debt:wiring` (count of open wiring liabilities) joins the three
  existing ledger figures on the **witness tape**, visible daily. A never-fired reflex is now a
  number that grows, not a paragraph nobody rereads.

This is the double-entry generalization of the CLAUDE.md verification lessons: reachable ≠
producing, declared ≠ runs, `--test`-green ≠ wired.

## Component 7 — Migration (each phase artifact-verified; cron stays live until proven)

Cron is **not** deleted on faith. Phases, each gated on a real artifact:

- **P1 — journal, read-only.** Ship Components 1–3. `mesh-chat` enforces grammar; transformer emits
  `board.journal`; put the three balances + `debt:wiring` on the witness tape. Cron unchanged.
  *Artifact:* `hledger -f board.journal bal` answers a real query; `--check` finds a real leak.
- **P2 — reactor in shadow.** Run `mesh-board-reactor --shadow` beside the still-live cron
  `mesh-dispatch`/`mesh-fsnotify`. Log `would-wake` vs what cron actually dispatched; diff for a
  day. *Artifact:* the shadow log routes the same `[task]`s cron did, with pace decisions matching
  the spend hold. Fix divergences here, cron still the source of truth.
- **P3 — flip.** Arm the watchdog pair; **see it red** (kill reactor → watch restart post; park a
  fake untaken `[task]` → watch the alarm). Only then remove the mind-waking cron lines:
  `mesh-dispatch` (:3-59/5), the `mesh-fsnotify … -- mesh-dispatch` line, `mesh-chat-sync` (→ folded
  into reactor, or kept if it's cross-node board bridging — decide at flip), `mesh-queue-tend`.
  *Artifact:* a real `[task]` posted with `owner:<w>` is picked up end-to-end through the reactor
  path (pane shows the wake, mind posts `[taking] <slug>`), cron lines confirmed absent from
  `crontab -l` and `reflexes.cron`.
- **P4 (later, non-blocking).** Migrate threshold/scheduled crons (`mesh-mind-compact
  --high-tokens`, `mesh-study`/`study-bridge`) into reactor-internal events. Not day one.

**Data-plane crons and one-shots stay untouched** (e.g. the 2026-07-25 zai-revert one-shot).

## Coordination note

genome already holds `[taking] event-driven-dispatch` (task 13:20Z) on the board — **this spec is
that task's design**. It lands through genome's lane via `mesh-land`, coordinated on the board, not
as a second parallel build. discover + witness own the board→journal query surface (Direction 1).
Substrate discipline unchanged: the systemd units are a substrate change → claim on `mesh-trace`,
apply under the single-writer rule.

## Open questions deferred (YAGNI until measured)

- witness duty-split accounts — only if the passive/active lanes need separate metering.
- Cross-node board bridging under a zero-cron model — `mesh-chat-sync`'s fate decided at P3 flip
  (fold vs keep as the one bridging exception).
- Per-window budget *values* — start report-only (`MESH_LABOR_BUDGET_TURNS` unset today); arm caps
  once the shadow phase shows real per-window burn.
