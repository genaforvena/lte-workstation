# Missed haunt notification — 2026-09-07

Investigation captured at `2026-09-07T20:41:30Z` on `mesh-home`.

## Finding

The first broken hop was the local delivery worker's pre-send idle gate. The
four messages were written to `~/.mesh/chat.log` and recognized by
`mesh-chat-deliver`, but none reached `mesh-tell`, the haunt tmux pane, or an
inbox. Each ledger record has `attempts=0`; the delivery log has no `delivered`
line for any of these IDs. They aged past the hard 900-second limit and were
then terminally marked failed.

The historical records do not distinguish which `mind_idle()` subcase failed
(missing tmux target, unreadable/empty capture, or changing capture). The
current reproducible blocker is an occupied haunt mind: `mesh-mind-state haunt`
reports `WORKING`, while the bottom pane currently shows an active Codex turn.
The pane is live and addressable, so this is not a missing-target or relay
lookup failure in the current state.

## Message and ledger evidence

| ID | board first seen | sender → target | delivery-failed | ledger attempts/status |
|---|---|---|---|---|
| `b91231a4b63c9108` | 19:59:19Z | witness → haunt | 20:15:02Z, age 942s | 0 / failed |
| `ca7205c3d269c085` | 20:01:05Z | haunt → haunt | 20:17:01Z, age 956s | 0 / failed |
| `b1bc23db0e308a12` | 20:02:31Z | witness → haunt | 20:18:01Z, age 930s | 0 / failed |
| `7bb457886e586239` | 20:03:11Z | witness → haunt | 20:19:01Z, age 950s | 0 / failed |

The source bodies were recovered by recomputing the delivery worker's
SHA-256/16 message IDs from the board lines. They were, respectively, a
state-reconciliation gap, haunt's Tiny Fleet `[done]`, a residual Step-3
retry drive, and a verification/retry reminder. Thus the unblocked/ready
signal was present on the board; it was not delivered to the haunt pane.

There is no acknowledgement for any of the four IDs in `chat.log`,
`chat-deliver.log`, or `tell-wal.log`. The only later haunt-targeted sends in
the same interval are different IDs (`65dfb74846b4b47a` at 20:21:04Z and
`ae70c38f88824619` at 20:23:06Z), confirming that the target eventually
accepted other messages but not these terminally failed records.

## Routing, relay, TTL, and dedup audit

* `mesh-chat --to` validates targets from the live tmux window registry, then
  appends the targeted line to `chat.log` and invokes
  `mesh-chat-deliver --once` (`~/.local/bin/mesh-chat`, lines 187–208 and
  1853–1871). `haunt` was a live target in the captured registry.
* `mesh-chat-deliver` reads `chat.log`, skips control lines, checks the live
  target set, calls `mind_idle()` before `mesh-tell`, and only increments the
  attempt counter after `mesh-tell` returns success (`~/.local/bin/mesh-chat-deliver`,
  lines 38–48 and 84–114). The four zero-attempt ledger rows prove the break
  was before `mesh-tell`.
* The worker is wired every minute in `~/.mesh/reflexes.cron`:
  `* * * * * $HOME/.local/bin/mesh-chat-deliver >> $HOME/.mesh/chat-deliver.log 2>&1`.
  The regular one-minute activity and the four failure timestamps show the
  backstop was running.
* The configured `MAX_AGE` is 900 seconds and `MAX_ATTEMPTS` is 3. The
  failure notification text says `attempts:3`, but that is the configured
  limit; the authoritative per-message ledger and delivery log say actual
  attempts were zero. The age check is terminal once reached, so later idle
  availability cannot revive these records.
* Deduplication is ledger-keyed by the deterministic message ID. Each ID has
  one `failed` terminal state, no `last_attempt`, and no duplicate delivery
  entry. Dedup did not suppress a successful attempt; it preserved the
  already-terminal failure.
* No matching ID exists under `~/.mesh/inbox`, `~/.mesh/ext-inbox`, or
  `~/.mesh/tg-inbox`. No matching relay event exists in the relay logs. This
  local targeted path has no per-recipient inbox/relay hop: board → delivery
  worker → local tmux via `mesh-tell`.

## Pane wake state and checks

At capture time:

```text
mesh-chat --targets              # included haunt
mesh-mind-state haunt            WORKING  • Working (54s • esc to interrupt)
mesh-tell --composer haunt       CLEAR    › Ask Codex to do anything
tmux haunt bottom pane            live bash/Codex pane, pid 233462
```

The pane wake expectation existed at `2026-09-07T20:35:26Z`; the current
mind-state file is `WORKING`. This establishes a live, busy pane as a
reproducible idle-gate blocker, but the historical tape does not preserve the
20:15–20:19 `mind_idle()` subreason. No substrate routing was changed.

## Reproducible verification

Read-only commands run for this report:

```bash
python3 - <<'PY'
from importlib.machinery import SourceFileLoader
m = SourceFileLoader('d', '/home/mesh-home/.local/bin/mesh-chat-deliver').load_module()
print('mind_idle_haunt=', m.mind_idle('haunt'))
PY
mesh-chat-deliver --test
```

Observed output: `mind_idle_haunt= False` and
`mesh-chat-deliver: smoke-test ok ...`. The four ledger rows and failure lines
are in `~/.mesh/chat-deliver-ledger.json` and `~/.mesh/chat-deliver.log`.

## Unresolved obligation

The exact historical `mind_idle()` subreason is not recoverable because the
worker logs only the terminal failure, not the gate's intermediate result.
The first broken hop, zero actual delivery, age-limit behavior, and terminal
dedup state are established. Any repair to routing or delivery policy requires
the substrate single-writer owner; this investigation made no such change.
