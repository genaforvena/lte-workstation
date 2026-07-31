# witness labour-tape Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the witness TAPE pane's one-line labour summary with a live rolling-5h double-entry tree (assets:budget vs expenses:labour by window, netting to an explicit computed `0`), promoted to the primary view; promise and money ledgers become thin footer lines below it.

**Architecture:** `mesh-labor` gains a new render mode (`--balance --rolling`) that reuses its existing rolling-window spend.log tally (`turns_between`, already shared with `--budget`) and prints it as a Dr/Cr tree instead of a cap table. `mesh-witness` calls that live (measured 35ms — cheap enough per render tick) from `render_pane()`, reordered above the existing promise/resource ledger blocks.

**Tech Stack:** bash (`scripts/mesh-labor`), Python 3 (`scripts/mesh-witness`). No new dependencies.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-24-witness-labour-tape-design.md` — every requirement below traces to a component in that file.
- **This repo does not `git commit` tool changes directly.** The established pattern (CLAUDE.md single-writer/mesh-land discipline, and the stuck-strands fix landed earlier the same day): edit the source in `scripts/`, deploy a copy to `~/.local/bin/<tool>` for live use, leave the source file **uncommitted** in the working tree, and let the separate `mesh-land` tool commit+push once the file has "settled" (unchanged for its settle window). Do **not** run `git commit` on `scripts/mesh-labor` or `scripts/mesh-witness` as part of this plan — every "commit" step below is replaced with a "deploy" step.
- Both tools are self-testing via `<tool> --test` (no separate `tests/` directory in this codebase) — follow that convention, don't create new test files.
- `mesh-witness` prepends `~/.local/bin` to its own `PATH` at import time (line 49) specifically so subprocess calls resolve under cron's stripped PATH — Task 2 depends on Task 1's `mesh-labor` already being deployed to `~/.local/bin` (same machine, same session — just do Task 1 first).
- No new caching layer. `mesh-labor --balance --rolling` is called live on every `mesh-witness --pane` render (measured cost of the underlying tally: 35ms, pure file read, no git/hledger fork).

---

### Task 1: mesh-labor — rolling self-balancing tree renderer

**Files:**
- Modify: `scripts/mesh-labor:380-459` (add a GATE5 test block inside the existing `do_test()`)
- Modify: `scripts/mesh-labor` (add new `do_balance_rolling()` function, placed directly above the `# ============================ DISPATCH ============================` marker currently at line 461)
- Modify: `scripts/mesh-labor:465` (the `--balance)` dispatch case)

**Interfaces:**
- Consumes: existing `turns_between lo hi` (prints `epoch prov win` rows, one per turn — defined at `scripts/mesh-labor:96`), existing `$WINDOW_H` global (rolling window hours, env `MESH_LABOR_WINDOW_H`).
- Produces: `do_balance_rolling()` — no args, prints the tree to stdout, no return value consumed elsewhere. `independent_window_tally lo_iso hi_iso` — prints `count win` pairs to stdout, used internally by `do_balance_rolling` and directly by the test. New CLI surface: `mesh-labor --balance --rolling`. Task 2 shells out to exactly this command.

**Scope note:** the design spec's Component 1 interface line mentions an optional `--window-hours N` override; the spec's own "Open question" section defers it as unscoped follow-up (nothing consumes it — the pane always wants the mesh-wide default `$WINDOW_H`). This plan does **not** implement `--window-hours` — `do_balance_rolling` always uses `$WINDOW_H` directly, matching `do_budget`'s existing behavior. Don't add the flag; it would be dead code with no caller.

**Revision note (post-Task-1-review, before Task 1 was deployed):** the original design below computed its trailing checksum by bucketing the SAME `$rows` two different ways (a raw line count vs a sum of per-window awk buckets) — the task reviewer correctly caught that this is a mathematical identity (partitioning a set and summing bucket sizes always recovers the total count, for any data), not a live correctness check. Revised design: the checksum now compares `turns_between`'s count (epoch/mktime arithmetic) against a SECOND, independently-implemented parser, `independent_window_tally` (ISO-8601 timestamp STRING comparison — no mktime, no OFFSET correction, a genuinely different code path over the same raw `$SPEND_LOG`). A bug in either implementation's window-boundary math has real odds of not reproducing in the other, so a real divergence can surface here — matching the "two independent computations must AGREE" idiom `mesh-ledger`/`mesh-promises` already use elsewhere in this mesh (see `docs/design-hledger-coordination-2026-07-24.md`).

- [ ] **Step 1: Write the failing test**

Open `scripts/mesh-labor`. Find `do_test()` (starts at line 380). Immediately before the final line of the function —

```bash
  [ "$fail" = 0 ] && { echo "mesh-labor --test: PASS"; return 0; } || { echo "mesh-labor --test: FAIL"; return 1; }
}
```

— insert this new GATE5 block (after the GATE4 fail-safe block, before that closing line):

```bash
  # GATE 5 — --balance --rolling: a per-WINDOW (not per-provider) Dr/Cr tree whose trailing
  # checksum is an INDEPENDENT cross-check (turns_between's epoch/mktime math vs
  # independent_window_tally's ISO-string comparison — two genuinely different implementations
  # reading the same $SPEND_LOG), not a tautological recount of the same bucketed rows.
  local rd="$td/rolling"; mkdir -p "$rd"
  cat > "$rd/spend.log" <<EOF
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn tg claude anthropic paid Opus
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn tg claude anthropic paid Opus
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn tg claude anthropic paid Opus
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn genome claude anthropic paid Opus
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn genome claude anthropic paid Opus
$(date -u -d '-1 hour' +%Y-%m-%dT%H:%MZ) turn witness opencode zai paid GLM
EOF
  local rtree
  rtree="$(SPEND_LOG="$rd/spend.log" MESH_SPEND_LOG="$rd/spend.log" MESH_LABOR_WINDOW_H=5 bash "$0" --balance --rolling 2>/dev/null)"
  if printf '%s\n' "$rtree" | grep -qE '^  tg +3$' && printf '%s\n' "$rtree" | grep -qE '^  genome +2$' \
     && printf '%s\n' "$rtree" | grep -qE '^  witness +1$'; then
    echo "  ✓ GATE5 rolling tree: per-window counts correct (tg=3 genome=2 witness=1), no provider nesting"
  else
    echo "  ✗ GATE5 rolling tree: window counts wrong — got: $rtree"; fail=1; fi
  if printf '%s\n' "$rtree" | tail -1 | grep -qE '^ *0$'; then
    echo "  ✓ GATE5 checksum: trailing balance line is 0 (turns_between and independent_window_tally AGREE)"
  else
    echo "  ✗ GATE5 checksum: trailing line is not a bare 0 — got: $(printf '%s\n' "$rtree" | tail -1)"; fail=1; fi

  # GATE 5b — divergence proof: a turn stamped EXACTLY at the lower window boundary must be
  # EXCLUDED (turns_between's own contract: "lo exclusive, hi inclusive"). Mutate a copy of
  # independent_window_tally (flip '>' to '>=', a plausible off-by-one) and show it WRONGLY
  # counts the boundary turn — a real, reproducible divergence on the SAME fixture, proving
  # do_balance_rolling's checksum can actually catch this bug class, not print a constant.
  local lo_fixed hi_fixed lo_ep hi_ep
  lo_fixed="$(date -u -d '-3 hours' +%Y-%m-%dT%H:%MZ)"
  hi_fixed="$(date -u +%Y-%m-%dT%H:%MZ)"
  lo_ep="$(date -u -d "$lo_fixed" +%s)"; hi_ep="$(date -u -d "$hi_fixed" +%s)"
  local bd="$td/boundary"; mkdir -p "$bd"
  printf '%s turn tg claude anthropic paid Opus\n' "$lo_fixed" > "$bd/spend.log"
  local turns_boundary ind_boundary ind_mutated mutated
  turns_boundary="$(SPEND_LOG="$bd/spend.log" bash -c "$(declare -f turns_between); turns_between $lo_ep $hi_ep" | wc -l | tr -d ' ')"
  ind_boundary="$(SPEND_LOG="$bd/spend.log" bash -c "$(declare -f independent_window_tally); independent_window_tally $lo_fixed $hi_fixed" | awk '{s+=$1} END{print s+0}')"
  mutated="$(declare -f independent_window_tally | sed 's/ts>lo/ts>=lo/')"
  ind_mutated="$(SPEND_LOG="$bd/spend.log" bash -c "$mutated; independent_window_tally $lo_fixed $hi_fixed" | awk '{s+=$1} END{print s+0}')"
  if [ "$turns_boundary" = 0 ] && [ "$ind_boundary" = 0 ]; then
    echo "  ✓ GATE5b boundary: a turn exactly AT the lower bound is correctly EXCLUDED by both parsers (exclusive-lo semantics agree)"
  else
    echo "  ✗ GATE5b boundary: exclusive-lo semantics wrong — turns_between=$turns_boundary independent=$ind_boundary (want 0/0)"; fail=1; fi
  if [ "$ind_mutated" != "$ind_boundary" ]; then
    echo "  ✓ GATE5b divergence: a mutated (inclusive-lo) independent tally WRONGLY counts the boundary turn ($ind_mutated vs $ind_boundary) — the cross-check is live"
  else
    echo "  ✗ GATE5b divergence: mutated copy still agreed — fixture doesn't exercise the bug"; fail=1; fi
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash scripts/mesh-labor --test 2>&1 | tail -20`

Expected: the GATE5/GATE5b lines print `✗` or the test errors outright (`independent_window_tally: command not found` — the function doesn't exist yet, and `--balance --rolling` isn't wired), final line reads `mesh-labor --test: FAIL`.

- [ ] **Step 3: Implement `independent_window_tally` and `do_balance_rolling`**

Find the line `# ============================ DISPATCH ============================` (currently line 461, immediately after `do_test()`'s closing `}`). Insert these two new functions directly above it:

```bash
# ============================ ROLLING BALANCE TREE ============================
# independent_window_tally: a SECOND, independently-implemented rolling-window turn tally used
# only to cross-check do_balance_rolling's checksum. Deliberately does NOT call turns_between or
# reuse epoch/mktime math — it compares zero-padded ISO-8601 timestamp STRINGS lexicographically
# (valid because e.g. '2026-07-24T10:00Z' < '2026-07-24T10:30Z' as plain strings, matching
# numeric/chronological order) against explicit ISO bounds, a different code path from
# turns_between's mktime+OFFSET correction. A real bug in either implementation (an OFFSET sign
# flip, a mktime DST edge case, an off-by-one in the window bound) has real odds of NOT
# reproducing identically in both, so a genuine divergence can surface here — unlike re-summing
# the same already-bucketed rows. Same exclusive-lo/inclusive-hi contract as turns_between.
independent_window_tally(){  # argv: lo_iso hi_iso -> prints "count win" pairs, one per window
  local lo="$1" hi="$2"
  [ -f "$SPEND_LOG" ] || return 0
  awk -v lo="$lo" -v hi="$hi" '
    $2=="turn" && NF>=6 { ts=$1; win=$3; if (ts>lo && ts<=hi) c[win]++ }
    END { for (w in c) print c[w], w }
  ' "$SPEND_LOG"
}
# do_balance_rolling: the double-entry view of the rolling-5h window --budget already tallies:
# same turns_between source, same per-window grouping (windows ARE the accounts), printed as
# Dr/Cr instead of a cap table. The trailing checksum compares turns_between's total against
# independent_window_tally's total — two genuinely separate parsers, not the same bucketed rows
# recounted two ways.
do_balance_rolling(){
  local hi lo; hi="$(date -u +%s)"; lo=$(( hi - $(awk "BEGIN{print int($WINDOW_H*3600)}") ))
  local rows; rows="$(turns_between "$lo" "$hi")"
  local total; total="$(printf '%s\n' "$rows" | grep -c .)"
  printf 'assets:budget            %6d TURN\n' "$(( -total ))"
  printf 'expenses:labour           %6d TURN\n' "$total"
  printf '%s\n' "$rows" | grep . | awk '{c[$3]++} END{for(w in c) print c[w], w}' | sort -rn | \
    awk '{printf "  %-20s %6d\n", $2, $1}'
  local hi_iso lo_iso
  hi_iso="$(date -u +%Y-%m-%dT%H:%MZ)"; lo_iso="$(date -u -d "-${WINDOW_H} hours" +%Y-%m-%dT%H:%MZ)"
  local ind_total; ind_total="$(independent_window_tally "$lo_iso" "$hi_iso" | awk '{s+=$1} END{print s+0}')"
  printf '%s\n' "$(printf '%0.s-' $(seq 1 30))"
  printf '%30d\n' "$(( total - ind_total ))"
}

```

Then edit the `--balance)` dispatch case (currently a single line):

```bash
  --balance)  ensure_repo; hledger -f "$(main_journal)" balance expenses:labour assets:budget --tree "${@:2}" ;;
```

replace with:

```bash
  --balance)
    if [ "${2:-}" = "--rolling" ]; then
      do_balance_rolling
    else
      ensure_repo; hledger -f "$(main_journal)" balance expenses:labour assets:budget --tree "${@:2}"
    fi ;;
```

- [ ] **Step 4: Run test to verify it passes**

Run: `bash scripts/mesh-labor --test 2>&1 | tail -15`

Expected: all three GATE5 lines print `✓`, final line reads `mesh-labor --test: PASS`.

- [ ] **Step 5: Eyeball the real output, then deploy**

Run: `bash scripts/mesh-labor --balance --rolling`

Expected: a tree matching the format in the design spec — `assets:budget`/`expenses:labour` header pair, one indented line per window with a real turn count, a dashed rule, and a trailing bare `0` (or `assets:budget -0 TURN` / `expenses:labour 0 TURN` with no window lines and a trailing `0` if the rolling window is currently empty — both are valid, honest output).

Deploy (do NOT `git commit` — see Global Constraints):

```bash
cp scripts/mesh-labor ~/.local/bin/mesh-labor && chmod +x ~/.local/bin/mesh-labor
mesh-labor --balance --rolling   # re-run from the deployed copy to confirm it matches
```

---

### Task 2: mesh-witness — promote the labour tree to the pane's primary view

**Files:**
- Modify: `scripts/mesh-witness:17-19` (module docstring, "Cost discipline" paragraph)
- Modify: `scripts/mesh-witness:43-44` (add a new module-level env-configurable constant beside `LEDGER`)
- Modify: `scripts/mesh-witness` (add a new `_labour_tree()` helper directly above `def render_pane(embed=False):`, currently line 403)
- Modify: `scripts/mesh-witness:450-497` (reorder: labour tree first, resource ledger and promise ledger become footers below it)
- Modify: `scripts/mesh-witness:612-682` (`smoke_test()` — add presence/ordering/failure-fallback assertions)

**Interfaces:**
- Consumes: Task 1's `mesh-labor --balance --rolling` (must be on `PATH`, which `mesh-witness` already prepends with `~/.local/bin` at line 49 — deploy Task 1 first).
- Produces: no new CLI surface on `mesh-witness` itself — this is an internal render-order and content change. New env var `MESH_LABOR_BIN` (test-injection only, default `"mesh-labor"`), following the exact pattern `MESH_WITNESS_LEDGER`/`MESH_WITNESS_TAIL` already establish in this file.

- [ ] **Step 1: Write the failing test**

Open `scripts/mesh-witness`. Find the `# --- EMBED CONTRACT ...` block inside `smoke_test()` (starts at line 648) and the `finally:` that closes the sandboxed-ledger `try:` (line 679). Insert this new block immediately before that `finally:` line (i.e., as the last statements inside the `try:`, after the existing `MESH_WITNESS_TAIL` assertions):

```python
        # --- LABOUR TREE (primary view, live `mesh-labor --balance --rolling` call) ---
        # Real spend.log content is environment-dependent (nondeterministic across machines/runs),
        # so this asserts PRESENCE + ordering + the failure fallback, not specific numbers — same
        # convention as the METRICS loop above, which allows UNKNOWN for live-subprocess fields.
        if "labour ledger" not in plain:
            print("smoke-test: FAIL (pane render missing labour ledger section)"); sys.exit(1)
        # promoted ABOVE resource ledger (only checked if that section is present on this machine —
        # its own file may not exist in a bare checkout, and this test must stay hermetic either way)
        if "resource ledger" in plain and plain.index("labour ledger") > plain.index("resource ledger"):
            print("smoke-test: FAIL (labour ledger not promoted above resource ledger)"); sys.exit(1)
        # failure mode: mesh-labor unreachable/erroring must render the loud fallback, never a
        # silently-dropped section. MESH_LABOR_BIN lets the test point at a broken stub without
        # touching the real ~/.local/bin/mesh-labor (same injection idiom as MESH_WITNESS_LEDGER).
        import shutil
        stubdir = tempfile.mkdtemp(prefix="witness-test-stub-")
        try:
            stub = os.path.join(stubdir, "broken-mesh-labor")
            with open(stub, "w") as f:
                f.write("#!/bin/sh\nexit 1\n")
            os.chmod(stub, 0o755)
            broken = _cli(env_add={"MESH_LABOR_BIN": stub})
        finally:
            shutil.rmtree(stubdir, ignore_errors=True)
        if "labour tree render FAILED" not in broken:
            print("smoke-test: FAIL (broken mesh-labor did not trigger the loud labour-tree fallback)"); sys.exit(1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 scripts/mesh-witness --test 2>&1 | tail -15`

Expected: `smoke-test: FAIL (pane render missing labour ledger section)` (the section header text doesn't exist yet — current code emits `-- labour ledger (mesh-labor · labour-time · rolling 5h budget · ...) --`, which does NOT contain the literal substring being checked for placement purposes here in the same way after the rewrite; more directly: `plain.index("labour ledger")` may exist already coincidentally via the OLD one-liner block's header, which also contains "labour ledger". To get a clean, meaningful RED here, run the NEW failure-fallback assertion first as the discriminating check — expect it to fail with `smoke-test: FAIL (broken mesh-labor did not trigger the loud labour-tree fallback)` since nothing calls `mesh-labor` live yet.

- [ ] **Step 3: Update the module docstring**

Replace (lines 17-19):

```python
Cost discipline: ALL the (moderately) expensive reads live in --measure, which a reflex runs on
a cadence. The pane render (--pane / no-arg) only tails the ledger — a pure file read — so the
data pane refreshes cheaply every frame while the measurement itself is throttled to the cron.
```

with:

```python
Cost discipline: ALL the (moderately) expensive reads live in --measure, which a reflex runs on
a cadence. The pane render (--pane / no-arg) only tails the ledger — a pure file read — so the
data pane refreshes cheaply every frame while the measurement itself is throttled to the cron.
One deliberate exception (2026-07-24): the labour tree calls `mesh-labor --balance --rolling`
live on every render — measured ~35ms (a pure spend.log tally, no git/hledger subprocess), cheap
enough per-tick, and required for the rolling-5h window's sub-minute freshness a --measure-cadence
cache can't give.
```

- [ ] **Step 4: Add the `MESH_LABOR_BIN` constant**

Replace (lines 43-44):

```python
LEDGER = os.environ.get("MESH_WITNESS_LEDGER") or os.path.expanduser("~/.mesh/witness.log")
MESHDIR = os.path.expanduser("~/.mesh")
```

with:

```python
LEDGER = os.environ.get("MESH_WITNESS_LEDGER") or os.path.expanduser("~/.mesh/witness.log")
MESHDIR = os.path.expanduser("~/.mesh")
# test injection only (mirrors MESH_WITNESS_LEDGER above) — production never sets this, always
# resolves the real mesh-labor off PATH.
LABOR_BIN = os.environ.get("MESH_LABOR_BIN") or "mesh-labor"
```

- [ ] **Step 5: Add the `_labour_tree()` helper**

Directly above `def render_pane(embed=False):` (currently line 403), insert:

```python
def _labour_tree():
    """Live rolling-5h double-entry labour tree from `mesh-labor --balance --rolling`.

    Returns the tree text (no trailing newline) or None on any failure — the caller renders a
    loud fallback line, never a silently-dropped section."""
    try:
        out = subprocess.run([LABOR_BIN, "--balance", "--rolling"], capture_output=True,
                             text=True, timeout=5).stdout.rstrip("\n")
        return out if out else None
    except Exception:
        return None


```

- [ ] **Step 6: Reorder — labour tree first, resource + promise demoted to footers**

Replace the entire block from the resource-ledger comment through the end of the labour-ledger block (lines 450-497 — everything between the `# a first-order self-reading` try/except above it and the `lines.append("")` that follows, i.e. this exact span):

```python
    # resource ledger — the mesh measuring what it CONSUMES (mesh-ledger, double-entry, parity-checked).
    # Cheap: tails a one-line summary mesh-ledger writes each hourly feed; no live hledger in this render.
    try:
        with open(os.path.expanduser("~/.mesh/.ledger-summary")) as f:
            summ = f.read().strip()
        if summ:
            lines.append("")
            lines.append("-- resource ledger (mesh-ledger · double-entry · `mesh-ledger --dash`) --")
            lines.append("  " + summ)
    except OSError:
        pass

    # promise ledger — the mesh's UNKEPT board obligations (mesh-promises, double-entry leak detector).
    # Cheap: tails the one-line summary + a short leak worklist mesh-promises caches each feed; no live
    # replay here. This is witness's DRIVING surface — a leaked promise is a [task] made and not kept,
    # and driving its owner (pick-up-or-retire) is witness's board duty.
    try:
        with open(os.path.expanduser("~/.mesh/.promises-summary")) as f:
            psumm = f.read().strip()
        if psumm:
            lines.append("")
            lines.append("-- promise ledger (mesh-promises · unkept board obligations · `mesh-promises --report`) --")
            lines.append("  " + psumm)
            try:
                with open(os.path.expanduser("~/.mesh/.promises-leaks")) as f:
                    leaks = f.read().rstrip("\n")
                if leaks:
                    lines.append("  leaked (drive owner: pick-up-or-retire):")
                    lines.append(leaks)
            except OSError:
                pass
    except OSError:
        pass

    # labour ledger — the mesh measuring what it SPENDS in labour-time (mesh-labor, double-entry,
    # commodity TURN, rolling 5h budget à la Claude Code). The third axis beside money + obligations:
    # money is imputed, promises are owed, but a TURN is the thing actually consumed. Cheap: tails the
    # one-line summary mesh-labor caches each feed; the live budget is `mesh-labor --budget`.
    try:
        with open(os.path.expanduser("~/.mesh/.labor-summary")) as f:
            lsumm = f.read().strip()
        if lsumm:
            lines.append("")
            lines.append("-- labour ledger (mesh-labor · labour-time · rolling 5h budget · `mesh-labor --budget`) --")
            lines.append("  " + lsumm)
    except OSError:
        pass
    lines.append("")
```

with:

```python
    # labour ledger — PRIMARY view (operator 2026-07-24: "chat.log as an hledger accounting
    # system that balances itself around labour spent"). Live rolling-5h Dr/Cr tree, not a cached
    # one-liner — see _labour_tree() and the Cost discipline note above for why this is exempted
    # from the pane's usual pure-file-read rule.
    lines.append("")
    lines.append("-- labour ledger (mesh-labor · rolling 5h · self-balancing · `mesh-labor --balance --rolling`) --")
    tree = _labour_tree()
    if tree:
        lines.extend("  " + l for l in tree.splitlines())
    else:
        lines.append("  (labour tree render FAILED — this frame BLIND, not all-clear)")

    # resource ledger — the mesh measuring what it CONSUMES (mesh-ledger, double-entry, parity-checked).
    # Cheap: tails a one-line summary mesh-ledger writes each hourly feed; no live hledger in this render.
    # Footer position (demoted 2026-07-24): labour is now the primary axis on this pane.
    try:
        with open(os.path.expanduser("~/.mesh/.ledger-summary")) as f:
            summ = f.read().strip()
        if summ:
            lines.append("")
            lines.append("-- resource ledger (mesh-ledger · double-entry · `mesh-ledger --dash`) --")
            lines.append("  " + summ)
    except OSError:
        pass

    # promise ledger — the mesh's UNKEPT board obligations (mesh-promises, double-entry leak detector).
    # Cheap: tails the one-line summary + a short leak worklist mesh-promises caches each feed; no live
    # replay here. This is witness's DRIVING surface — a leaked promise is a [task] made and not kept,
    # and driving its owner (pick-up-or-retire) is witness's board duty. Footer position (demoted
    # 2026-07-24): labour is now the primary axis on this pane.
    try:
        with open(os.path.expanduser("~/.mesh/.promises-summary")) as f:
            psumm = f.read().strip()
        if psumm:
            lines.append("")
            lines.append("-- promise ledger (mesh-promises · unkept board obligations · `mesh-promises --report`) --")
            lines.append("  " + psumm)
            try:
                with open(os.path.expanduser("~/.mesh/.promises-leaks")) as f:
                    leaks = f.read().rstrip("\n")
                if leaks:
                    lines.append("  leaked (drive owner: pick-up-or-retire):")
                    lines.append(leaks)
            except OSError:
                pass
    except OSError:
        pass
    lines.append("")
```

Note: the `.labor-summary` file and the code that writes it (`mesh-labor`'s `write_summary`/`do_dash`) are untouched — out of scope, still a valid path for other consumers of `mesh-labor --dash` (confirmed via `grep -rn "labor-summary" scripts/` — only this now-replaced block read it from `mesh-witness`).

- [ ] **Step 7: Run test to verify it passes**

Run: `python3 scripts/mesh-witness --test 2>&1 | tail -15`

Expected: `smoke-test: ok`. If it fails on the ordering check, confirm real machine state has `~/.mesh/.ledger-summary` (it does, per earlier investigation) and re-check the reorder in Step 6 was applied in the right sequence (labour block, then resource block, then promise block).

- [ ] **Step 8: Eyeball the real output, then deploy**

Run: `python3 scripts/mesh-witness --pane --embed 2>&1 | head -40`

Expected: the `-- labour ledger ... --` section appears directly after the sparkline/measure-age block, with a real Dr/Cr tree and trailing `0`; `-- resource ledger --` and `-- promise ledger --` appear after it.

Deploy (do NOT `git commit` — see Global Constraints):

```bash
cp scripts/mesh-witness ~/.local/bin/mesh-witness && chmod +x ~/.local/bin/mesh-witness
mesh-witness --pane --embed 2>&1 | head -40   # re-run from the deployed copy to confirm it matches
```

---

### Task 3: Integration check on the live fused pane

**Files:** none modified — this task only runs and observes.

**Interfaces:**
- Consumes: Task 1's deployed `~/.local/bin/mesh-labor`, Task 2's deployed `~/.local/bin/mesh-witness`.
- Produces: nothing new — final verification that the two pieces compose correctly through `mesh-dash`, the actual host of the witness TOP pane in the live tmux session.

- [ ] **Step 1: Render the fused pane through mesh-dash**

Run: `timeout 20 scripts/mesh-dash --once witness 2>&1 | head -50`

Expected: the labour tree appears as the first ledger section after the sparkline block, with resource and promise ledgers following it, then the board half (churn/claims/digest-gaps/board-tail) unchanged from the stuck-strands fix landed earlier.

- [ ] **Step 2: Run mesh-dash's own smoke test**

Run: `timeout 30 scripts/mesh-dash --test 2>&1 | tail -5`

Expected: `smoke-test: ok` (this test drives through `mesh-witness --pane`/`--embed`, so it exercises Task 2's changes transitively — no direct edit to `mesh-dash` needed for this feature).

- [ ] **Step 3: Confirm both source files are uncommitted and ready for mesh-land**

Run: `git status --short -- scripts/mesh-labor scripts/mesh-witness`

Expected: both files show as modified (`M`), matching the "deploy live, leave uncommitted" convention from Global Constraints. Do not commit or run `mesh-land --apply` — landing is a separate, later step (the files need to "settle" first, same as every other change in this session).

- [ ] **Step 4: Relay to the board**

Per CLAUDE.md ("a direct operator↔mind conversation must relay its discussed+agreed outcomes to chat.log"), post one `[fyi]` summarizing what landed (both file paths, the new `--balance --rolling` flag, the pane reorder, that both are deployed-but-uncommitted for the next `mesh-land` pass) — same pattern used for the stuck-strands fix earlier in this session.
