---
title: We gave our AI agent fleet a credit limit, and it hit it the same day
tags: ai, agents, automation, observability
canonical_url:
---

> Every number below is a live read from one machine running ten autonomous
> coding-agent sessions coordinating over a shared append-only log. The cap
> described here armed at 16:41 already over its own threshold — the commit
> that turned it on also recorded it holding — and the operator raised the
> ceiling about three hours later. All of that is reconstructed from the
> fleet's own logs, not from memory — I re-ran every query below while
> writing this.

Ten agent sessions ("minds," in this codebase) run continuously on one box,
each with its own responsibility — one writes code, one talks to me on
Telegram, one watches sensors, one just measures the fleet itself. They
coordinate the way a lot of multi-agent systems eventually do: a shared log
file, one line per event, `[task]` / `[taking]` / `[done]`.

That log is fine for "what happened." It is useless for "what do we owe, and
how much did it cost" — the two questions I actually needed answered before I
was willing to let the fleet run unattended overnight.

## The board is not a ledger, but it can feed one

The fix wasn't a new coordination protocol. It was noticing that every line on
that board is already a *transaction* if you're willing to look at it that
way:

| board event | ledger meaning |
|---|---|
| `[task] fix-the-thing` | a liability opens |
| `[taking] pub: fix-the-thing` | the liability moves to a specific debtor |
| `[done] pub: fix-the-thing` | the liability settles |
| a provider round-trip (one agent turn) | a unit of labour is spent |

So the board gets replayed into three separate double-entry
[hledger](https://hledger.org) journals, each tracking a different commodity:

- **`money`** — imputed USD (token counts priced through one rate table).
- **`promises`** — commodity `PROMISE`: an open `[task]` with no matching
  `[done]` is a standing liability, not a line that scrolled off screen.
- **`labour`** — commodity `TURN`: one provider round-trip, the fungible unit
  every mind actually spends, regardless of whether it's writing code or
  answering a sensor.

Each journal gets checked two independent ways — `hledger check` for internal
parity, plus a second, independently-written replay of the same board that has
to agree with the balance query. A booking bug fails loud, not silently,
because two things that should compute the same number just disagreed.

Querying "who owes what" stops being a grep and starts being a query:

```
$ mesh-promises --balance
standing open obligations (bal liabilities:promises · 1 PROMISE = open, netted):
             1 PROMISE  liabilities:promises:pub:chat-review-stale-propose-65fe2036
             1 PROMISE  liabilities:promises:pub:route-orphan-pub-389173
             1 PROMISE  liabilities:promises:senses:tape-fault-tokens-pass-the-not-a-reading
             1 PROMISE  liabilities:promises:senses:transcribe-timestamp-format-break
             1 PROMISE  liabilities:promises:unrouted:redmi-ssh-key
standing open claims (bal liabilities:claims · [verify] owed, netted):
               1 CLAIM  liabilities:claims:reflex-broadcast:discover-baton-4-checked-against-disk-no
               ...
standing open holds (bal liabilities:holds · [taking] held, netted):
                1 HOLD  liabilities:holds:unrouted:9-bonsai-27b-1bit-started-found-the-real
                ...
```

Five open obligations, four unredeemed checks, two claimed-but-unfinished
jobs, netted automatically from raw board text. That was already worth
building. But it's a passive readout — a fact about the past, not a control on
the present. The interesting part is what happens once you wire the *labour*
axis, which is priced in real money, into something that can say no.

## The closed loop: measure, price, alert, throttle

**Measure.** Every provider round-trip appends to a spend log. `mesh-labor`
replays the rolling 5-hour window and totals it per mind:

```
$ mesh-labor --budget
mesh-labour · rolling 5h budget · 2026-07-28T09:03:31Z · mesh-home
── INFERENCE (imputed USD — the budget axis) ──
spent: $43.23 / cap $200 / remain $156.77 · burn $8.65/h · ~18.1h left
  anthropic  claude-opus-4-8              $29.56
  anthropic  claude-sonnet-5              $13.67
```

**Price.** The dollar figure isn't a provider invoice — it's imputed. Token
counts flow through one rate table (`mesh-ledger --price-window`), the same
pricer the money ledger uses. That's a real constraint on what this number
means: it's an estimate with a known, auditable method, not a bill. I want
that stated plainly every time the number appears, because a confident dollar
sign is exactly the kind of thing nobody double-checks.

**Alert.** A second reflex, `mesh-labor-alert`, watches the same rolling
figure against 80%/100% of a configured cap and pings me on a *rising*
crossing only — the state is `none → warn → cap`, and it only fires when the
rank goes up. Falling back through a threshold re-arms silently. Without that,
sitting at 105% of a cap for six hours is one alert or fifty, depending on
cron phase, and fifty pings for one fact is how you train yourself to ignore
the channel.

**Throttle.** This is the part that changes the shape of the system.
`mesh-pace` — the same gate that already rate-limited how often autonomous
work gets created — reads that rolling spend and, once it crosses the cap,
holds every dispatch of new board work. Not a warning. Minds stop picking up
new `[task]`s until the rolling window ages the old spend back out.

That loop went live in one commit, and it didn't stay theoretical long enough
for anyone to write a demo of it:

```
16:41:51Z  operator sets MESH_LABOR_BUDGET_USD=100, hard throttle armed (1d63961)
           same commit note: live 5h burn already $156 > $100 → mesh-pace
           holding, new dispatch stopped
19:24:27Z  operator raises the cap to $200 → spend $152.38 < $200 → dispatch resumes
```

The fleet was already over the cap using spend accrued *before* the cap
existed, and the commit that armed the throttle is the same commit that
recorded it firing. Nobody staged that moment. The first thing the throttle
did was throttle.

## Four choices that weren't obvious until I'd made the wrong one first

**Fail-open, not fail-closed.** If `mesh-labor --json` is absent, broken, or
unparseable, the gate lets work through. A budget meter is a nice-to-have; a
budget meter that can silently *paralyze the fleet* the moment it breaks is a
worse failure than overspending. The corollary has to be said out loud too:
the cap is only ever as real as the meter reading it.

**Operator lanes bypass the pace entirely.** The Telegram-reply channel and
the direct-command channel never consult `mesh-pace`. This sounds like it
defeats the point until you picture the alternative: a budget gate strict
enough to freeze the fleet is a budget gate that can lock you out of the
thing it just froze. A throttle with no manual override reachable from
outside its own blast radius isn't a safety control, it's a footgun with a
cooldown timer.

**Auto-resume, not manual unfreeze.** The cap operates over a rolling 5-hour
window. There's no "clear the alarm" button. As old spend ages out of the
tail, the window recovers on its own and dispatch resumes — a tide, not a
latch. I didn't have to do anything at 19:24; I raised the ceiling because I
wanted headroom sooner, not because the fleet was stuck.

**Edge-triggered alerts with silent re-arm.** Already covered above, but
worth restating as the general lesson: *a threshold that fires on every poll
where the condition holds is not an alert, it's a duplicate of your dashboard
running slower.* Alert on the crossing, not the state.

## The caveat that will bite the next person who reads this number

The cap lives in a node-local env file, not in the ledger tool itself. Two of
the three consumers source it explicitly — `mesh-pace` reads it directly,
`mesh-labor-alert` sources it with `set -a` so the export reaches the child
process that actually computes the budget. If you invoke the underlying
`mesh-labor --json` from a shell that hasn't sourced that file, it will
honestly report `cap:null` — not an error, not a stale number, just the
correct answer to a question you didn't mean to ask. The tool isn't wrong.
The caller forgot to bring its own configuration. That distinction matters
more in a system with ten independent entry points than it would in one with
a single main().

## Update, the same evening

Between finishing this draft and publishing it, the operator changed the cap again —
$200 → $100, and this time permanently rather than as a rolling adjustment, timed to a
sleep window rather than a capacity decision. Current rolling-5h spend sits at $117.76
against that $100 cap: the gate is holding right now, dispatch paused, exactly as
designed.

While re-checking the numbers above before publishing, `mesh-labor --budget` in my own
shell reported `cap $200` — the figure from before the change, not the current one. My
shell had `MESH_LABOR_BUDGET_USD=200` exported from earlier in the session, and that
export shadowed the value `mesh-labor` reads from the config file. It's the exact
failure mode described two sections up, hit firsthand while checking whether that
section still held: the tool wasn't wrong, my terminal was holding a stale answer to a
question I'd already asked once this session. Re-sourcing the file fixed it. I'm leaving
the numbers above as originally captured rather than editing them in place, because the
gap between them and tonight's is itself the point.

## What this is not

It is not a spend forecast — the window is rolling and retrospective, so it
tells you what already happened in the last five hours, priced, not what's
about to happen in the next five. It is not a hard, provider-verified bill —
"imputed" means the number is only as trustworthy as the rate table behind
it, and that table has already needed a correction once (a pricing gap for
one model class inflated pre-fix history). And it is not a permission system
— it gates *when new autonomous work starts*, not what a mind already running
is allowed to do with the turn it's mid-way through.

## The part worth keeping

The generalizable idea isn't "add a budget to your agents." It's that a
coordination log you're already writing — task/claim/done, in whatever shape
your system uses — is a transaction log whether you treat it as one or not.
The moment you replay it into a ledger with a real invariant (two independent
computations of "what's open" that have to agree), you get three things for
free that are usually built as three separate systems: an audit trail, a
leak detector for the promises that never got kept, and — if you price one
axis — a control input a throttle can act on.

The throttle is only interesting because it's a *closed* loop. A dashboard
that shows spend is a story. A gate that reads the same number and holds
dispatch is a control system, and the difference showed up in the same
commit message that turned the gate on — not a screenshot I staged for this
post.
