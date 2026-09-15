# Task-only coordination witness — verification artifact

Task: `task-only-coordination-20260908/task-only-coordination`

The witness pane renders structured unfinished task state from
`~/.mesh/tasks.journal`; non-task coordination accounting is not rendered as
task work. Raw `chat.log` appears only as an explicitly labelled,
unfiltered evidence tail. The materializer consumes every source line as bytes,
records `source_events`, `replayed_events`, `source_errors`, byte count, and a
SHA-256 digest, while malformed task-state records remain evidence and do not
become tasks.

Live source coverage at 2026-09-08T07:59Z:

```text
events=36065 replayed_events=36065 errors=0 bytes=18134672
sha256=4db8781a21880bb31bf5b9e2e52433fed590a3fef69e823cf07e92958230aef8
complete=True
```

Focused verification passed:

```text
bash tests/test-mesh-task-source-coverage.sh
bash tests/test-mesh-witness-promises.sh  # compatibility test name; exercises mesh-task-journal
bash tests/test-mesh-witness-lifecycle.sh
bash tests/test-mesh-witness-hledger-gate.sh
bash tests/test-mesh-witness-promises-single-writer.sh  # compatibility test name
bash tests/test-mesh-witness-task-queue-fit.sh
python3 tests/test-witness-open-pane.py
bash -n scripts/mesh-task-journal scripts/mesh-task-watch
python3 -m py_compile scripts/mesh_task_log.py
git diff --check
```

Current live verification is recorded by `~/.mesh/tasks.journal`: task-source replay
must be `PASS`, source and replayed event counts must match, and the pane displays
only unfinished task rows plus the unfiltered raw chat tail.
