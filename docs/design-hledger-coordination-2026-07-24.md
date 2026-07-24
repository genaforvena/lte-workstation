# hledger at the center of mesh coordination — direction (2026-07-24)

Operator direction, captured before the minds→witness reincarnation so it survives the session
restart. This is a DIRECTION to design and build incrementally, not a landed spec. Origin: a live
Telegram design session with the operator, 2026-07-24 (tg mind).

## The thesis

The mesh already coordinates through the **board** (`~/.mesh/chat.log`): `[task]`/`[taking]`/
`[done]` and the marker family. The operator's move: treat that board as a **first-class hledger
journal**, and put **hledger at the center of coordination** — not off to the side as $-accounting.

**Stop thinking money; think LABOUR.** The unit the mesh actually spends is labour-time (mind
compute), not dollars. Marxist framing: a `TURN` (one provider round-trip) is the abstract
labour quantum — genome's coding, tg's talking, a sense's classifying all reduce to the same
fungible TURN. We measure labour and price it in nothing but itself.

Operator cite: <https://hledger.org/1.52/hledger.html#queries-and-command-options> — "super-improved
coordination on a plate." hledger's query language (`acct:`, `tag:`, `date:`, `status`, `amt:`,
`register`/`balance`/`--pivot`) turns coordination questions into one-line queries instead of greps.

## The three ledgers (all double-entry, parity-checked, own git repos)

1. **money** — `mesh-ledger` (commodity USD): imputed inference $ + energy + depreciation.
2. **promises** — `mesh-promises` (commodity PROMISE): board `[task]`→`[done]` as obligations;
   an unkept promise is a standing liability = the leak detector.
3. **labour** — `mesh-labor` (commodity TURN) — **built 2026-07-24, landed 623efe4**. The third
   axis and the one the operator wants central. Rolling 5h budget like Claude Code's limit
   (`--budget`), board-as-journal attribution (`--branch <slug>` = labour a task cost), feed from
   `~/.mesh/spend.log`, wired into the witness TOP pane beside the other two. See
   [[mesh-labor-turn-axis]] memory for the turn-def caveat (spend.log 15 vs mesh-spend 1688).

All three surface side-by-side on the witness tape (`mesh-witness`) — the mesh measuring what it
consumes, owes, and spends.

## Direction 1 — the board as a first-class hledger journal (the coordination substrate)

Give board posts a **shared tag schema** so hledger queries can slice them:
`owner:<window>` · `task:<slug>` · `prio:<incident|normal>` · `status:`. Then coordination questions
become queries, not greps:
- "who owes labour / has unkept promises" → `hledger -f promises bal tag:owner=<w>`
- "where is labour flowing" → `mesh-labor --balance` / `register tag:task=<slug>`
- "which branch was expensive" → `mesh-labor --branch <slug>`
- "what's unkept and how old" → `mesh-promises --report`

Design task (discover + witness): the board→journal tag schema + a query surface. Build after design.

### The formal rules — "board as a game" (witness, closing the 13:45 [taking])

The operator's frame, made precise. This is the CURRENT REAL SHAPE — cited pieces are landed code,
not proposal; open items are named as such, each with an owner.

**The pieces, and what plays each role:**

| game concept        | mesh reality                                    | status |
|----------------------|--------------------------------------------------|--------|
| the board (rule book) | `~/.mesh/chat.log`, append-only, one line/move   | live (always was) |
| a move                | a board line: `[marker] body`                    | live |
| the journal (score)   | `~/.mesh/{promises,labour,money}/*.journal`, materialized FROM the board | live, 3 journals |
| players (accounts)    | mind-windows — `accounts.journal` is the roster/chart of accounts | live, `ac685ae` (C2) |
| the labour quantum    | commodity `TURN` (`mesh-labor`) — one provider round-trip | live, `623efe4` |
| an obligation         | commodity `PROMISE` (`mesh-promises`) — opened by `[task]`, settled by `[done]` | live |
| a check owed          | commodity `CLAIM` (`mesh-promises`) — opened by `[verify]`, settled by a matching `[fyi]`/`[sense]`/`[done]` FROM the debtor; unaddressed → dedicated `reflex-broadcast` account, never redeemable by construction | live, `a22b704` |
| a claim held on work  | commodity `HOLD` (`mesh-promises`) — opened by a slugged `[taking] <slug>: ...`, settled by a matching `[done]` FROM the same taker | live, `a22b704` |
| money spent           | commodity `USD` (`mesh-ledger`) — inference $ + energy + depreciation | live |
| the score-check       | `hledger check` (parity) + a SECOND independent replay-vs-balance computation that must AGREE — a booking bug fails LOUD, not silently | live, all 3 journals |
| a misnamed player      | quarantined to `:unrouted` (or the dedicated `:reflex-broadcast` for claims) — VISIBLE, never a phantom named account | live |
| the move-tag schema    | ` ; owner:X, task:slug, prio:p, status:s` — an hledger-native tag tail on any board line | DESIGNED, `48dfb37` (discover) — not yet emitted by any poster |
| the query surface      | `mesh-board {open,owes,task,incidents,cost,leaks,count}` — thin wrapper over the 3 journals | DESIGNED (catalog in `48dfb37`), **not yet built** |
| dispatch reads the journal | `mesh-pace` cold-shrink reads `mesh-labor --json` burn rate to gate the event-wake `eff_gap` | live, `6b04aa8` — but `mesh-dispatch`'s own `$n_open` is still a raw `[task]`-line grep, not `mesh-board count` | **open — owner: discover** (Direction 1 migration step 4) |
| alarm fires FROM the journal | `mesh-promises --feed` is still a CRON tick (`31 * * * *`), not a journal-write trigger; leak alarms are batch-computed on the hourly replay, not event-fired the instant a threshold is crossed | **open — no owner yet**, see below |

**Why CLAIM/HOLD, not just PROMISE:** discover's board audit (14:39 fyi) found the mesh's two
leakiest claim shapes — an abandoned `[taking]` and a never-redeemed `[verify]` — had ZERO ledger
visibility (19 open verifies + 2 stale takings, invisible to a detector that only understood
`[task]`→`[done]`). Same double-entry idiom, same journal, same parity/agreement gates — extending
the model was cheaper than inventing a new one, and it is the direct proof that "board as a game"
generalizes past the one marker pair it started on.

**What "dispatch reads/writes the journal" means precisely**, now that two of the three pieces are
real: mesh-labor already GATES dispatch timing (cold-shrink reads burn rate). What's still missing
is dispatch reading its **backlog** from the journal — `mesh-dispatch` counts `[task]` lines
directly off the board (62 raw) instead of the netted `mesh-promises --balance` (12 real). `mesh-board
count` (discover's design, not yet built) is the piece that closes this — swapping dispatch's raw
`n_open` for it is Direction 1's step 4, already scoped, not re-scoped here.

**What "alarm fires FROM a ledger event" means, and why it's still open:** today `mesh-promises
--feed` runs on an hourly cron tick and computes leaks in a batch — a promise that crosses the leak
threshold at :05 isn't LOUD until the next :31 run, up to 26 minutes of silent lag. The board itself
already fires event-first (`mesh-fsnotify` on `chat.log` → `mesh-dispatch` in ~4ms), so the pattern
exists — the ledger side doesn't use it yet. A real fix needs either (a) a `postgresql`-style trigger
on journal write (hledger has no such hook natively — this repo's journals are plain files, not a
DB) or (b) a cheap poll keyed to CHAT_LOG's own mtime via the same fsnotify path dispatch already
rides, re-running `--feed` on every board write instead of hourly. (b) is the cheap, congruent
option — it reuses machinery that already exists rather than adding a new watcher. **Not built this
turn** (scope: this [taking] promised the rules formalized + the two new commodities working, not a
rearchitected alarm path) — filed as an explicit next `[task]`, unclaimed.

**The double-entry error-detecting property, generalized:** every commodity in this model shares one
invariant — TWO independent computations of "what's open" (a python replay of the board vs. an
`hledger balance` query on the materialized journal) must AGREE. A divergence means the journal was
corrupted or hand-edited, and the tool refuses to trust it silently. This is the actual payoff of
"put hledger at the center" — not the double-entry bookkeeping metaphor for its own sake, but a
free, structural CHECKSUM on every ledger the mesh keeps, for zero extra design cost per commodity.

## Direction 2 — minds work by REFLEXIVE TRIGGER, not by cron (labour audit)

With the labour ledger we can SEE per-mind work timing/duration. The failure mode it exposes: a mind
woken by **cron** (every N min, work or not) **burns labour idly** — a TURN with no corresponding
`[task]` on the board. A mind woken by **reflexive trigger** (a board event: new `[task]`, a mention,
a state change) spends labour only on real work.

Direction: move work-waking to **board-event triggers** (we already have `mesh-fsnotify` on
chat.log → `mesh-dispatch`); keep cron only as a **slow liveness backstop**, never hot polling —
a pure event system dies silently with no events AND nothing checking liveness (CLAUDE.md: "cron
reflexes remain the liveness guarantee, the loop is only an accelerant"). The labour ledger becomes
the EVIDENCE: cross-reference per-window turn-burn (`mesh-labor --budget` by-window) against board
activity to flag idle cron-burn. **Audit owner: tg** (turn-burn vs board-activity correlation).

## Direction 3 — minds → witness merge (config DONE, reincarnation pending)

Operator: remove the `minds` window; new 10-window set = **tg tg-roz discover genome witness senses
health sound pub vpn**. Restart the whole session in this composition.

- **Config landed in `~/.mesh/restore.env`** (backup: `restore.env.bak-pre-minds-merge-20260724`):
  `MESH_MIND_CHANNELS` → the 10-set (both assignments), `MESH_RETIRED_CHANNELS` += `minds chat`
  (chat was merged into witness 2026-07-24 but restore.env still carried it — drift now closed),
  `MESH_AGENTIC_FALLBACK` `chat health` → **`witness health`** (the guardrail — the live dispatch
  fallback pool must not name a retired window).
- **The guardrail (why the merge is safe):** dispatch is a **cron reflex** (`mesh-dispatch` at
  :3-59/5 + fsnotify on chat.log), NOT pane-work in the `minds` window — so it survives the window's
  removal and runs throughout. `minds` was the allocation VIEW (already on the witness tape:
  minds_live/minds_work/spend1h/the 3 ledgers) + one claude orchestration mind. witness inherits the
  coordination charter. **Verify after: dispatch still FIRES** (a [task] gets picked up), not just
  that the tape looks fuller — else it's the dead-active-lane shape the chat→witness merge warned of.
- **Follow-up (not blocking):** `mesh-mind-control`'s `minds_manifest()` hardcodes `"minds claude"`
  and other tools mention `minds`/`chat` — these are fallbacks (live paths read tmux); clean + land
  them after the reincarnation.

## Direction 4 — mesh-rns-sh survives connection drops (requested, not yet built)

Operator: make `mesh-rns-sh` survive a link drop so he doesn't keep re-logging-in — "like the mesh."
Two layers (rnsh 1.4.0 supports both):
1. **Far side = persistent tmux**: serve the shell as `rnsh -l -- tmux new-session -A -s rns-mesh`
   (the `-l -- <cmd>` default-command form). Link drops → the tmux session persists on the far side
   → reconnect re-attaches with full state, exactly the mesh's own append-only-session doctrine.
2. **Client = auto-reconnect loop**: wrap the `rnsh -i $EXID <hash>` call in a reconnect-on-non-clean-
   exit loop with backoff; a tmux DETACH (rc 0) = deliberate leave → break; a Link failure (rc≠0) →
   reconnect. Net = mosh-like: drop as much as you want, return to the same live session.
Real tool: `scripts/reticulum/mesh-rns-sh.sh` (deployed via the `scripts/mesh-rns-sh` shim — never
copy). Test over a REAL link drop rip↔mesh-home. **Owner: tg.**

## Open next-steps (post-reincarnation worklist)

- [ ] tg: build mesh-rns-sh resilience (Direction 4) + test over a real drop
- [ ] tg: trigger-vs-cron labour audit (Direction 2)
- [ ] discover + witness: board→journal tag schema + query surface (Direction 1)
- [ ] verify dispatch fires post-merge (Direction 3 guardrail)
- [ ] cleanup: remove `minds`/`chat` from mesh-mind-control manifest + siblings, land
