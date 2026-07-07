# mesh-nudge Integration Guide

## Overview

`mesh-nudge` consolidates keystroke injection into **one hardened module**, eliminating 7 copy-pasted instances
across `mesh-tick`, `mesh-tell`, `mesh-mind-compact`, `mesh-mind-state`, `mesh-restore`, `mesh-channel`,
and `mesh-channel-keepalive`.

This pattern was identified in guy-fawxible (gf-nudge, 2026-06-23 control-plane hardening item #1):
> "keystroke injection was copy-pasted into 10 tools; the base64 paste sequence was re-invented with its own
> version of the same repeatedly-fixed bugs (paste-burst detectors, newline-per-message, shell-quoting)."

## What mesh-nudge Does

Injects a message into a tmux pane (bottom = mind pane of a window), with protective guards:

```bash
printf 'your message' | mesh-nudge <window> [--raw]
```

### Return Codes (Posix-semantic)

- **0** = Injected (message sent, pane accepted it)
- **1** = FAIL (pane not found, tmux error, bare shell detected)
- **2** = N/A (tmux session missing, tool not configured)
- **3** = Deferred (agent WORKING or NEEDS-INPUT — didn't send, retry next tick)

### Modes

**Standard mode** (default):
```bash
printf 'work' | mesh-nudge genome
```
- Guards: clears line + refuses bare shells + defers if agent is busy
- Use for: nudging agents (mesh-tick, mesh-mind-compact role-streams)

**Raw mode** (`--raw`):
```bash
printf 'user input' | mesh-nudge --raw tg-reply
```
- No guards: injects as-is, no clear, no idle check, no defer
- Use for: human-facing reply consoles where a human may be mid-typing

## Current Copy-Paste Instances (Consolidation Candidates)

| Tool | Lines | Pattern | Risk |
|------|-------|---------|------|
| mesh-tick | 143 | `tmux send-keys -t '$pane' C-u; echo $NB64 \| base64 -d \| tmux load-buffer...` | Standard + CYCLE dedup |
| mesh-tell | ~120 | `tmux send-keys -t ...C-u; echo $b64 \| base64...` | Standard + ACK probe |
| mesh-mind-compact | ~80 | `tmux send-keys...C-u...base64...` | Standard |
| mesh-mind-state | ~90 | Similar standard pattern | Standard + --stats gate |
| mesh-restore | ~85 | Standard pattern | Standard |
| mesh-channel | ~75 | Standard pattern | Standard + retry loop |
| mesh-channel-keepalive | ~95 | Standard pattern | Standard + shed+relaunch |

## Refactoring Checklist

For each tool, follow this pattern:

### Before: Copy-Pasted Keystroke Logic

```bash
run "tmux send-keys -t '$pane' C-u; sleep 0.1; echo $NB64 | base64 -d | tmux load-buffer -b mtick\$\$ -; tmux paste-buffer -p -d -b mtick\$\$ -t '$pane'; sleep 0.5; tmux send-keys -t '$pane' C-m"
```

### After: Use mesh-nudge

```bash
# Option A: shell function for readability
inject_nudge(){
  printf '%s' "$1" | run "mesh-nudge '$WIN'"
  return $?
}

# Then use it:
inject_nudge "$NUDGE_MSG" || { echo "nudge deferred"; exit 3; }

# Option B: direct call
if ! printf '%s' "$NUDGE_MSG" | run "mesh-nudge '$WIN'"; then
  rc=$?
  case "$rc" in
    3) echo "nudge deferred — agent busy"; exit 3 ;;
    *) echo "nudge failed"; exit 1 ;;
  esac
fi
```

### Special Cases

**mesh-tick with CYCLE dedup:**
```bash
# BEFORE: always clears and sends unless rc=0 (injected)
# NOW: still track CYCLE, but rely on mesh-nudge for the guard
CYCLE=0
[ "${4:-}" = --cycle ] && CYCLE="${5:-0}"

if [ "$CYCLE" -eq 0 ]; then
  printf '%s' "$NUDGE" | mesh-nudge "$WIN"
  # No explicit rc check needed — mesh-nudge handles defer
else
  echo "mesh-nudge dedup: cycle $CYCLE > 0, skip"
fi
```

**mesh-tell with ACK probe:**
```bash
# BEFORE: injects then probes for ACK
# NOW: same, but simpler pane management
if printf '%s' "$prompt" | mesh-nudge "$paneref"; then
  if [ "$ack" = 1 ]; then
    # proceed with ack_probe() as before
  fi
fi
```

**mesh-mind-state / mesh-restore with busy-defer:**
```bash
# These already have busy-detection. mesh-nudge ALSO checks via mesh-mind-state,
# so there may be redundancy. After migration, consider removing the tool's own check
# and relying on mesh-nudge's deferred rc=3.
```

## Safety Checks Before Integration

1. **Test each tool's smoke test** (usually exists, ensure it still passes)
2. **Manually test the nudge** on a real window:
   ```bash
   tmux new-session -d -s test -c ~
   tmux new-window -t test -n work -c ~
   printf 'echo injected' | mesh-nudge -t test:work
   ```
3. **Verify no hanging sends** — mesh-nudge has no infinite loops, sleeps are bounded
4. **Check mode-specific behavior** — tools using `--raw` reply consoles are rare; most are standard

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Refactor bug introduces a hang | Add `--test` to every tool; run before deploying |
| mesh-nudge call fails silently | All tools should check rc=3 (deferred) and rc!=0 (error) |
| Copy-paste still exists after refactor | Post-refactor grep: `grep -r 'C-u.*base64.*load-buffer' scripts/` should return only documentation |
| Message loss on defer | Tools should queue deferred nudges and retry; don't silently drop |

## Post-Integration Verification

After all 7 tools are migrated:

1. **Grep for old pattern:** `grep -r 'tmux.*C-u.*base64' scripts/` should only match documentation
2. **Run all `--test` targets:** Each tool should still pass its test
3. **Verify keystroke-injection paths covered:**
   - Idle nudge (mesh-tick standard)
   - Role-stream NUDGE (plan/check/verify/chat/heartbeat)
   - Reply console (mesh-tg-reply, mesh-tg-team-reply)
   - Mind shed/relaunch (mesh-channel-keepalive)
4. **Live test:** Run a few cron cycles, verify minds still wake and respond

## References

- guy-fawxible `gf-nudge` (2026-06-23 hardening pass, item #1)
- guy-fawxible `DECISIONS.md` section "gf-nudge consolidation"
- [`mesh-nudge` source](../scripts/mesh-nudge)
