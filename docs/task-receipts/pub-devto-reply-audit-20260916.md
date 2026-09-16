# dev.to reply queue audit — 2026-09-16

## Scope and live evidence

Ran `mesh-devto-comments --list` at 2026-09-16T03:42Z and personally inspected the five
comments surfaced by the pub dashboard as owed:

| comment | author | disposition | evidence |
|---|---|---|---|
| `3ekdf` | @jasonbotsford0239 | spam; no reply | unsolicited API promotion plus TinyURL link |
| `3eoo9` | @nwfd_engineer | spam; no reply | unsolicited service offer plus checkout link |
| `3ekc9` | @elbert3255 | spam; no reply | unsolicited job-application promotion plus TinyURL link |
| `3ef25` | @stephanheidenreich761 | spam; no reply | unsolicited API promotion plus short URL |
| `3ecl5` | @fromzerotoship | genuine; reply draft below | substantive question/observation about SATURATED vs UNMEASURED and measurement boundaries |

## Draft for the genuine comment

> That distinction is exactly the useful boundary: SATURATED says the counter reached its
> representational limit, while UNMEASURED says the check did not obtain evidence for the
> expected pattern. I’m keeping them separate because the first is a known limit of the
> instrument and the second is a failure to establish a result. The current artifact supports
> that distinction; it does not support claiming either state explains every silent run.

## Delivery boundary

`mesh-devto-comments` is read-only. Its `--help` output documents that dev.to exposes no write
comment endpoint and that replies must be posted by the operator. No external comment was posted
by this audit. The artifact is the handoff for the operator to post the one genuine reply and
ignore the four promotional comments.
