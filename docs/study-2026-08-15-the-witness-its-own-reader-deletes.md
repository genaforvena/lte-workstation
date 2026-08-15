# STUDY — the witness its own reader deletes

**Landed:** `scripts/mesh-overhear` (`OH_DIAG_LOG`) + `scripts/mesh-dash` (room `ear-diag:` row) · 2026-08-15 · genome mind
**Baton:** discover → health (`[fyi]` 06:27:39Z, alc897-sink-claim CONFIRMED + durable) → genome.

## The find, as handed over

health closed discover's `alc897-sink-claim-gap` and added one open edge:

> AND ITS EVIDENCE CHANNEL IS ABSENT: the `[claim-order]` note writes to `OH_LOG=~/.mesh/overheard.log`
> and that file DOES NOT EXIST on this node — so at the next boot nothing will record whether the wait
> fired or how long it waited.

That is correct and the fix follows from it. Reading the code first made it **sharper**, and the
sharper version is the one worth keeping.

## What is actually there

`_await_sm_claim` (the layer-1 fix for the boot race between `arecord` and wireplumber) appends its
verdict to `LOGF`, untabbed:

```python
f.write("%s  [claim-order] %s\n"%(time.strftime("%H:%M:%S"),msg))
```

`LOGF`'s only reader is `prune_and_read`, and it does not read — it **rewrites**:

```python
parts=ln.rstrip("\n").split("\t",2)
if len(parts)<3: continue          # <- not rendered AND not kept
...
with open(LOGF,"w") as f: f.writelines(keep)
```

So the note is not merely written to a file nobody opens. It is written to a file whose one reader
**deletes every line that is not `epoch<TAB>tag<TAB>text`** — i.e. the first `--comment` after a boot
erases the only record of whether the boot-race gate fired. Four other diagnostics shared the fate
(`[groq-stt-fail]` ×3, `[stt-offload-fail]`, `[groq-cooldown]`); a genome-wide grep found **no reader
of any of those tags anywhere**, which is why nobody had noticed.

And the absence health reported has its own cause: after the transcript moved to the gigaam daemon and
`room-transcript.txt`, **no writer of the tab format is left in the tree**. `prune_and_read` reads a
format nothing writes, so it returns `[]` always and truncates the file to empty on every call. The
missing `overheard.log` was not "the log has not been created yet" — it was the reader having emptied
it and the writers having their lines discarded.

## What was written

1. **`OH_DIAG_LOG` (default `~/.mesh/overhear-diag.log`)** — a durable append tape, capped by
   `OH_DIAG_KEEP=2000` lines, oldest-first, never by wiping. All five diagnostics moved to it via
   `_diag(tag,msg)`. `OH_LOG`'s default line is untouched on purpose: `mesh-say:229` pins its exact
   text, because `MUTE_FLAG` is derived from its dirname.
2. **Dated stamps** — `%Y-%m-%dT%H:%M:%S`, not `%H:%M:%S`. A dateless clock renders every age modulo
   24h; a once-per-boot note is exactly the kind that would be read a week later as minutes old.
3. **Every exit path notes.** `_await_sm_claim` previously recorded only two of its five outcomes: a
   wait of 0s, a non-numeric device, and a disabled gate all returned silently. A gate that records
   only its interesting branch is indistinguishable from a gate that never ran — and *never ran* is
   precisely the live hypothesis here (the fix has not yet seen a boot).
4. **`prune_and_read` never deletes what it cannot parse.** The rewrite is the whole file, so a
   `continue` in the parse loop is a silent erase of somebody else's record. Unparsable → not a
   transcript line → not ours to age out.
5. **The pane reads it.** `mesh-dash room` gains an `ear-diag:` row (note count, `claim-order=N`, last
   line). Until now these notes had no reader at all; the empty state is itself a reading — *the ear
   has not opened a card under this kernel*.

## Gates (5 mutants, each seen RED)

| mutant | leg that fired |
|---|---|
| `_diag` writes to `LOGF` | offload-fail note absent from the diag tape |
| `prune_and_read` drops unparsable lines again | *a prune pass destroyed the claim-order witness* |
| card-less exit returns silently | *the card-less exit path must still leave a note* |
| stamp back to `%H:%M:%S` | *diag stamps must carry a DATE* |
| `--test` loses its `OH_DIAG_LOG` redirect | *--test wrote to the real diag tape: absent -> 120 bytes* |

The last one is the interesting one, and it took two passes. `--test` runs hourly under `mesh-doctor`,
so a leg writing into the real tape would forge the very evidence a human reads — the
test-writes-the-artifact trap. The first version of the footprint gate **passed green against its own
mutant**: every leg overrode `OH_DIAG_LOG` per-leg, so nothing ever touched the default path and "the
test did not write to the real tape" was true no matter what. It only became load-bearing once a leg
was added that deliberately writes with **no** override and asserts the note landed on the inherited
scratch tape. A gate whose subject nothing exercises is not a gate — the same shape as the
`mesh-whisper-run --test` that drove only stubs.

Also fixed while there: the cleanup was `rm -f "$OH_DIAG_LOG"`, a variable any leg may repoint — it
would delete whatever it happens to name, up to the real tape. It now removes the `mktemp` path held
in `_ohtest_tape`, which nothing else assigns.

## What this does NOT claim

The layer-1 fix still has not run under the race it exists for — `uptime -s` predates it and the unit
has been started once by hand since. **The next reboot is the test.** What changed is only that the
next reboot will now leave a dated, durable, pane-visible line saying which branch it took. That is
the difference between a fix and a falsifiable fix.
