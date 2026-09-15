# Independent verification: path-watch hourly relay alerts — 2026-09-12

Task: `mesh-path-watch-hourly-relay-repeat-20260912/verify-hourly-repeat-fix`

## Live task and board evidence

At 19:12Z, `~/.mesh/tasks.journal` showed this exact step `RUNNING` under
`witness` after `mesh-task take`; `mesh-task audit` agreed. The predecessor is
`DONE` with artifact
`docs/task-receipts/path-watch-hourly-relay-repeat-20260912.md`.

The raw `~/.mesh/chat.log` contains the cited `path-watch@mesh-home` relay
alerts at 15:49:02Z, 16:49:01Z, and 17:49:01Z (source lines 57288, 57498,
57665). Their intervals are 3599 and 3600 seconds. It also contains a fourth
alert at 18:49:01Z (line 57797), one hour after the third.

The raw `~/.mesh/path-watch.log` records intervening relay-to-direct recoveries
and direct-to-relay edges, including:

| Tape time | Edge |
| --- | --- |
| 15:34:01Z | relay → direct |
| 15:44:02Z | direct → relay |
| 16:14:01Z | relay → direct |
| 16:24:01Z | direct → relay |
| 16:39:01Z | relay → direct |
| 16:44:01Z | direct → relay |
| 17:19:01Z | relay → direct |
| 17:44:02Z | direct → relay |
| 17:54:01Z | relay → direct |
| 18:04:02Z | direct → relay |
| 18:19:01Z | relay → direct |
| 18:24:02Z | direct → relay |
| 18:34:01Z | relay → direct |
| 18:44:01Z | direct → relay |

The fourth alert follows the 18:44 direct-to-relay edge by one debounced pass.
This independently supports distinct relay episodes, rather than repeated
announcements of one continuously unresolved episode. The one-hour live window
did elapse and produced a further alert, so there is no pending-window
limitation to report.

## Regression and deployed wiring

- Source regression: `rtk mesh-path-watch --test` passed at 19:13:26Z. It
  reported a live Tailscale status read plus baseline, debounce, once-only,
  recovery, offline, UDP edge, BLIND, batching, suppression, and cooldown
  fixtures.
- Deployed regression: `rtk ~/.local/bin/mesh-path-watch --test` passed with
  the same result.
- Source and installed copy SHA-256 both equal
  `384ba31d7dae563cccf8b0ab024d5b812e69529202868fb3b223ff636ff8cf97`.
- Live crontab entry: `4-59/5 * * * * $HOME/.local/bin/mesh-path-watch`,
  appending to `~/.mesh/path-watch.cron.log`.
- Live status at 19:14:01Z succeeded and reported
  `imac-rozalia=relay`.
- The previously landed focused artifact documents the same-peer cooldown
  fixture and code path: `docs/chat-review-mesh-path-watch-relay-crossing-no-episode-cooldown-20260909.md`.

## Result

The three cited events and the additional live event are genuine post-deploy
relay crossings separated by recoveries. The 3600-second same-peer alert
cooldown and the five-minute scheduled invocation are present and tested. The
predecessor's conclusion that no code change is warranted is supported by this
independent verification.
