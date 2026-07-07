# Truncation-Safe Markers — Operator Hardening Item #2

Pattern ported from guy-fawxible (2026-06-23 hardening pass).

## Problem

Tools that track processing position in logs using **absolute line counts** are vulnerable to silent
event-loop death when logs are rotated or truncated:

```
Run N:   offset=100, total=100, save 100
Rotate:  log shrinks to 50 lines
Run N+1: offset=100, total=50 → 50 <= 100 → "no new lines" → SKIP FOREVER
```

The tool is running, reflexes report it as green, but it never processes anything again (silent death).

## Solution

Before processing, check for truncation and reset:

```bash
offset=0
[ -f "$OFFSET_FILE" ] && offset="$(cat "$OFFSET_FILE" 2>/dev/null || echo 0)"
total="$(wc -l < "$LOG" 2>/dev/null || echo 0)"

# Truncation-safe marker: if log SHRANK, it was rotated/truncated
if [ "$total" -lt "$offset" ]; then
  # Post visible alert (never silent)
  MESH_WHO="<tool>@$(hostname)" mesh-chat "[note] <tool>: log shrank (was $offset, now $total) — reset to 0; re-processing from top." >/dev/null 2>&1
  
  # Reset and re-read (to account for the [note] line itself)
  offset=0
  total="$(wc -l < "$LOG" 2>/dev/null || echo 0)"
fi

# Only AFTER the truncation check:
printf '%s\n' "$total" > "$OFFSET_FILE"
[ "$total" -le "$offset" ] && exit 0
```

## Key Points

1. **Check BEFORE saving** — detect shrinkage using the OLD offset
2. **Post visible alert** — never silently drop a reset (the whole point)
3. **Re-read after alert** — the [note] is now in the log, update total
4. **Use `total < offset`, not `<=`** — allows for exact-boundary cases
5. **Both line-based and timestamp-based offsets** are vulnerable (though timestamp-based is more resilient)

## Which Tools Need This

- ✓ `mesh-url-watch` — implemented (2026-07-07)
- Check: any tool that uses `wc -l < $LOG` + persisted offset file

## Exit Code Convention (Related Hardening)

While you're at it, document exit codes:

```bash
[ "${1:-}" = "--test" ] && {
  # test code
  exit 0  # or exit 1 on FAIL, or exit 2 on n/a (tool present but condition not met)
}

# In the main reflex:
command -v required-tool >/dev/null 2>&1 || exit 2  # n/a, not an error
some-condition || exit 2  # condition not met, n/a
```

This allows test suites to distinguish between:
- `exit 0` = ok (worked)
- `exit 1` = FAIL (real error)
- `exit 2` = n/a (tool present but not applicable — missing config, required peer unreachable, etc.)

## References

- guy-fawxible `gf-tick` (2026-06-23 operator hardening pass, item #2)
- guy-fawxible `DECISIONS.md` section "Log rotation + truncation-safe markers"
