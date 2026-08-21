# Reflexes — read this before scheduling anything

A reflex is something that runs without being asked. It is the last thing to add, not the first,
and on a freshly planted machine the correct number of reflexes is **zero**.

## Why zero on day one

There is nothing to tend yet. And a scheduled thing with nothing to tend does not sit idle — it
reports success. Every run finds nothing wrong, because there is nothing there, and prints green.
Weeks later that green is read as "the machine is being watched", when what it actually says is
"the check ran and its subject does not exist".

This is not a hypothetical. In the mesh this comes from:

- Three keepalive tools passed their own tests and were **in no schedule at all**. Passing a test
  and running are unrelated facts.
- One reflex was scheduled and tended a window that a reorganisation had deleted — permanently
  green, tending a phantom.
- One guard was keyed on a machine's hostname. The work moved to another machine, the condition
  went permanently false, and the guard **never executed once** while every run logged green.
- A retired organ left its old state file on disk holding a plausible last value. Everything
  downstream kept reading it as current for days.

The common shape: **the check survived its subject.** Nothing in a green result distinguishes
"healthy" from "absent".

## The gate

Before you schedule anything, all four must be true:

1. **There is a target that exists right now.** Name the file, the account, the folder. If you have
   to describe it in the future tense, it does not exist.
2. **It has already needed doing by hand, more than once.** Twice is a coincidence; that is the
   floor, not the bar.
3. **Its failure is visible.** You can say what a broken run looks like on the dash, and it does
   not look like a healthy one.
4. **It can report "I could not check".** Not a default value, not zero, not silence — a distinct
   state that says the check itself did not happen. A fallback that is indistinguishable from a
   success will eventually be one.

If any is false, do not schedule it. Register it as an organ instead (below), which runs when the
view is rendered and cannot rot in the dark.

## Organs — the honest middle step

```sh
mishe organ mail "ls -1 ~/Downloads | wc -l"
```

An organ runs when the dash renders. It is not scheduled, so it cannot go stale unwatched, and it
prints where somebody is looking. Three of its states are distinct on purpose:

- output → shown
- non-zero exit → `FAILED rc=N` with the message
- exit 0, no output → `EMPTY (ran, produced nothing)` — **not** blank, because a check that ran and
  said nothing is unknown, not fine

Most things that feel like they want a reflex want to be an organ. Start there. If after a few
weeks an organ has been genuinely load-bearing, then it is a candidate for scheduling.

## If you do schedule something

One at a time. On macOS, `launchd` (`launchctl`) is the native path and `cron` still works but is
deprecated and interacts badly with the sandbox and with Full Disk Access prompts — a cron job that
touches `~/Documents` or `~/Desktop` can be denied silently and report success.

Whatever runs it, hold three rules:

- **Write down that it exists**, on the board, when you create it — otherwise the only record of a
  scheduled job is inside the scheduler, and nobody reads schedulers.
- **Touch the state file on every successful run**, not only when the value changes. Otherwise a
  long-stable-but-live value looks identical to a dead job: the timestamp is how you tell "still
  running" from "stopped", and the content is how you tell what it said.
- **Watch it fail once, on purpose.** Break it, see the red, restore it. A gate you have never seen
  fail is not a gate — you have no evidence it can distinguish anything at all.

## Retiring one

Deleting the schedule is not retiring the reflex. Whatever state file it wrote **stays on disk
holding its last value**, and every reader keeps treating that value as current. Delete the
artifact too, or replace it with a line that says explicitly that this is retired and when.

An absence and a stale plausible value look identical from downstream. Only one of them is honest.

And whatever you schedule, `mishe burn` has to be able to find it. It strips crontab lines and macOS
launch agents that mention mishe; anything you wire by another route — a systemd user unit, a
launchd label that does not carry the name, a hook — is invisible to the teardown and turns "nothing
remains" into "nothing remains except". If you add a scheduling route, add it to `burn_scan` in the
core in the same change.
