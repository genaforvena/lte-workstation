# Dispatch Staffing Self-Heal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the missing live charter and add a witness reflex that detects and safely repairs missing repository-backed node-local charters before dispatch capacity disappears.

**Architecture:** `scripts/mesh-charter-watch` will be a narrow, read-mostly reflex. It will enumerate live multi-pane tmux windows, copy only missing charter files whose exact source exists in the repository, refuse divergent existing files, write an unconditional run/evidence row, post a board finding on repair or blockage, and re-run the live staffing census. A shell test fixture will exercise missing, repaired, and divergent-charter paths without touching the real node.

**Tech Stack:** POSIX shell, `cmp`/`install`/`mv`, tmux, existing `mesh-staffing`, `mesh-chat`, cron/autowire headers, shell fixture tests.

## Global Constraints

- Do not overwrite an existing divergent node-local charter.
- Do not copy a charter when its repository source is absent.
- Every reflex invocation writes a run row, including the no-op and failure paths.
- Preserve the existing staffing fail-closed behavior for malformed or unreadable charters.
- Keep all unrelated dirty worktree files untouched.

---

### Task 1: Add the failing self-heal reflex test

**Files:**
- Create: `tests/test-mesh-charter-watch.sh`
- Create later: `scripts/mesh-charter-watch`
- Create later: `tests/test-mesh-staffing-hyphen-heading.sh`

**Interfaces:**
- Test invokes `scripts/mesh-charter-watch --test`.
- The production script accepts `--test` and uses `MESH_CHARter_WATCH_HOME`, `MESH_CHARter_WATCH_REPO`, and `MESH_CHARter_WATCH_WINDOWS` only for hermetic fixtures.

- [ ] **Step 1: Write the failing test**

Create a wrapper test that runs the not-yet-existing tool and requires a missing-charter repair, a divergent-charter refusal, an evidence row, and the reflex cadence declaration.

```bash
#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
out="$($root/scripts/mesh-charter-watch --test 2>&1)"
grep -q 'missing charter repaired' <<<"$out"
grep -q 'divergent charter preserved' <<<"$out"
grep -q 'run row written' <<<"$out"
grep -q 'PASS' <<<"$out"
grep -q 'reflex-cadence:' "$root/scripts/mesh-charter-watch"
echo 'test-mesh-charter-watch: PASS'
```

- [ ] **Step 2: Run it to verify it fails**

Run:

```bash
bash tests/test-mesh-charter-watch.sh
```

Expected: FAIL because `scripts/mesh-charter-watch` does not exist.

### Task 2: Make hyphenated window headings parseable

**Files:**
- Modify: `scripts/mesh-staffing`
- Test: `tests/test-mesh-staffing-hyphen-heading.sh`

- [ ] **Step 1: Write the failing test**

Create a fixture for `# foo-bar — private channel` with no explicit `role:` and assert the JSON census returns `role=private channel` and `eligible=true`.

- [ ] **Step 2: Run it to verify it fails**

Run `bash tests/test-mesh-staffing-hyphen-heading.sh`; expected failure is the existing `charter for foo-bar has no role`.

- [ ] **Step 3: Implement the minimal parser fix**

Match the em-dash delimiter separately from the heading name, then fall back to a spaced ASCII hyphen delimiter. This preserves names such as `tg-roz`.

- [ ] **Step 4: Run it to verify it passes**

Run `bash tests/test-mesh-staffing-hyphen-heading.sh`; expected `PASS`.

### Task 3: Implement the guarded repair reflex

**Files:**
- Create: `scripts/mesh-charter-watch`

**Interfaces:**
- `scripts/mesh-charter-watch` performs one bounded audit/repair pass.
- `scripts/mesh-charter-watch --test` runs an isolated fixture and exits zero only when the three required paths are proven.

- [ ] **Step 1: Write minimal implementation**

Implement the live path with these exact decisions:

```bash
#!/usr/bin/env bash
# reflex-cadence: */5 * * * *
# reflex-state: $HOME/.mesh/charter-watch.log
set -euo pipefail

# MESH_CHARter_WATCH_HOME and MESH_CHARter_WATCH_REPO are test-only path overrides.
# MESH_CHARter_WATCH_WINDOWS is a whitespace-separated test-only window census.
```

The live path must:

1. Derive the repository from `MESH_CHARter_WATCH_REPO` or the script's parent directory.
2. Derive the node state from `MESH_CHARter_WATCH_HOME` or `$HOME`; use `$home/.mesh/charter` and `$home/.mesh/charter-watch.log`.
3. Use `MESH_CHARter_WATCH_WINDOWS` when set; otherwise run `tmux list-windows -t "$(hostname)" -F '#{window_name} #{window_panes}'` and retain only rows with at least two panes.
4. For each live window with `repo/charter/<window>.md` present and `home/.mesh/charter/<window>.md` absent, atomically install the exact source bytes with mode `0644` and record `repaired <window> source=<sha256> destination=<sha256>`.
5. Treat an existing symlink, directory, or divergent regular file as `blocked`, never overwrite it, and include the reason in the evidence row.
6. Always append one ISO-UTC `run ... result=... repaired=N blocked=N skipped=N` line to the state log, even when no repair is needed.
7. Post one `[fyi]` board line for repairs or blocks through `MESH_WHO=witness mesh-chat`, but do not make a chat failure hide the local evidence or change the exit status.
8. If `mesh-staffing` is available, run `mesh-staffing --json` after repairs and append `staffing_rc=<n>` plus a bounded first-line diagnostic. Exit nonzero only for an actual blocked repair or a failed staffing check; a no-op healthy run exits zero.
9. Keep `--test` hermetic and exercise missing-source, missing-destination repair, divergent-destination refusal, run-row writing, and a post-repair staffing stub.

- [ ] **Step 2: Run the focused test to verify it passes**

Run:

```bash
bash tests/test-mesh-charter-watch.sh
```

Expected: `test-mesh-charter-watch: PASS`.

### Task 4: Wire and deploy the reflex

**Files:**
- Modify: live `$HOME/.mesh/charter/` by restoring the missing `adint.md` from `charter/adint.md`.
- Modify: live `$HOME/.local/bin/mesh-charter-watch` by deploying the tested source atomically.
- Modify: live crontab through the repository's autowire mechanism.

- [ ] **Step 1: Restore the exact missing charter**

Verify the destination is absent, create no replacement for any divergent file, and atomically copy `charter/adint.md` to `$HOME/.mesh/charter/adint.md`; compare SHA-256 values.

- [ ] **Step 2: Deploy the tested reflex**

Run the repository's normal tool-sync/autowire path; if it cannot see an uncommitted tool, use an atomic temporary copy into `$HOME/.local/bin/mesh-charter-watch` and record source/deployed SHA-256 equality.

- [ ] **Step 3: Wire the declared cadence**

Run the existing autowire tool and verify a live `*/5 * * * *` crontab line for `mesh-charter-watch` exists. Do not create a second duplicate line.

### Task 5: Verify live dispatch recovery and regression behavior

**Files:**
- Verify: `scripts/mesh-staffing`, `scripts/mesh-dispatch`, `scripts/mesh-charter-watch`, live logs, live crontab.

- [ ] **Step 1: Run focused and wiring checks**

```bash
bash tests/test-mesh-charter-watch.sh
bash tests/test-mesh-staffing.sh
bash tests/test-mesh-tg-dispatch-policy.sh
bash tests/test-mesh-dispatch-hledger-gate.sh
scripts/mesh-charter-watch
scripts/mesh-staffing --json
mesh-dispatch --status
mesh-promises --check
```

- [ ] **Step 2: Verify live artifacts**

Require: node-local `adint.md` exists and hashes to the repository source; the reflex log has a fresh run row; staffing returns JSON rather than `rc=2`; dispatch status no longer reports a census-induced zero-worker failure; and the crontab has exactly one charter-watch line.

- [ ] **Step 3: Record the handoff**

Write `mesh-handoff witness` with the repaired paths, source/deployed hashes, test output summary, live staffing/dispatch results, and any remaining owner-directed NO-ACK obligations.
