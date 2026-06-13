# Embedded-python parse sweep — 2026-06-12T12:50Z

Prototype of the [task] the checker proposed at 12:43 (doctor parse-check does `bash -n`
but NOT embedded python in bash tools → mesh-github-watch + mesh-morning ran dead-but-green).
Ran it; found a **3rd** dead-but-green tool.

## Method

`/tmp/pysweep.py`: extract every `python3 <<MARKER`, `python3 -c '...'`, `python3 -c "..."`
block from `scripts/mesh-*`, `compile()` each. 35 blocks across 128 tools.
Plus a targeted grep for the py<3.12 class (backslash inside f-string `{braces}`).

## Real finding: mesh-study fetch() is HOLLOW

`scripts/mesh-study:22` — the `python3 -c` block's first statement is INDENTED:

```
fetch(){ curl -s -m 20 "$src" 2>/dev/null | python3 -c '
  import sys,json          # ← 2-space indent
try: d=json.load(sys.stdin) # ← column 0
...
```

→ `IndentationError: unexpected indent` on ALL python versions (verified by feeding the
block real JSON: rc=1, traceback). curl's stderr is `2>/dev/null` but python's is not, so
a real `mesh-study` fetch spews a traceback and returns ZERO results. `mesh-study --test`
passes ("all deps ok", rc=0) — never exercises fetch → dead-but-green. genome==deployed
(both broken). On-demand canon tool (field-mining), so low blast radius, but the core
fetch has never worked. **Fix: dedent line 22 `import sys,json` to column 0.**

## py<3.12 f-string class: CLEAN

No backslash-inside-`{braces}` hits. mesh-converse:222 has `\"` but in the f-string
LITERAL (outside braces) — legal on all versions, not a bug.

## 4 false positives (extractor artifacts — do NOT chase)

mesh-card:226, mesh-card:234, mesh-peers:26 (`-c "..."` blocks with inner quotes my regex
truncated — `mesh-card --refresh` rc=0, `mesh-peers --json` rc=0, both work live);
mesh-reflexes:29 (shell `home="'"$HOME"'"` quote-juggling broke my single-quote regex —
the assembled block runs rc=0). All verified working by live invocation.

## Recommendation

Wire this sweep into mesh-doctor (or a new mesh-pyparse) as the checker proposed — but it
MUST assemble the real post-shell-interpolation block (or skip blocks with `$(...)`/`$VAR`
inside the python), else it false-positives on the 4 above. The robust version: replace
`$VAR`→placeholder before compile, or run the block through `bash -c ':' ` dry capture.
