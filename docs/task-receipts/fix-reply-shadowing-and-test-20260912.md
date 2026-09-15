# mesh-job-reply shadowing and isolated self-test — 2026-09-12

The open `job-autonomy-followups-20260912/fix-reply-shadowing-and-test` task was still live.
Source and installed command resolved to the same file, and the deployed job-reply log contained
the reported `AttributeError: 'str' object has no attribute 'json'` at `_main`'s `a.json` use.

## Change

- Kept parsed options in `cli` and named the bank result `answer`, so the bank loop cannot replace
  the command-line options object.
- Made the DOM child probes use a hidden, dry-only fixture mode that bypasses the shared browser
  lock. Removed the live-browser read from `--test`; its DOM, multi-page overlap, repeated-head,
  `--max`, and timeout assertions now run against hermetic fixtures.
- Added `tests/test-job-reply-shadowing.py`, which exercises `_main` with a salary question and a
  bank answer. Before the fix it failed at `a.dry` with the reported string/object shadowing error;
  after the fix it passes.

## Verification

- `python3 tests/test-job-reply-shadowing.py` — PASS after the expected pre-fix `AttributeError`.
- `timeout 120 ./job/mesh-job-reply --test` — PASS, including logged-out, selector-drift, readable
  DOM control, second-page invitation, overlap dedupe, repeated-head stop, and `--max` assertions.
- Installed `/home/mesh-home/.local/bin/mesh-job-reply --test` — PASS while the HH apply lock was
  deliberately held; all six DOM/pagination/result markers were present and it exited 0.
- Source and installed command are the same symlink target and SHA-256:
  `b588583ea3fd42fa1885fabd6c826ecd0060e7c31a6136c7121690ebb80658b8`.
- User crontab still invokes `$HOME/.local/bin/mesh-job-reply --tg` at `41 */2 * * *`.
- `git diff --check` and `python3 -m py_compile job/mesh-job-reply` — PASS.

## Live dry-run result

Ran the bounded command `/home/mesh-home/.local/bin/mesh-job-reply --dry --json --max 1` at
2026-09-12. It safely exited 2 with `read=nav-failed: браузерный драйвер не поднялся
(mesh-hh-drive --start)`, an empty JSON stdout, and no employer message. A direct `--start` retry
also refused because the HH start lock was already in progress; the browser remained down, so no
safe live read was available. The private evidence is at
`~/.mesh/job/reply-shadowing-dry-run-20260912.json` (empty stdout) and
`~/.mesh/job/reply-shadowing-dry-run-20260912.stderr` (the n/a reason). Reply-state and calendar
hashes were unchanged across the dry run:

- reply state: `bb6042c264e89ccbb98667d8d4fa75d0b3eacfd6cd88be89ffbefb183a4a6f72`
- calendar: `577ca79afdc26d8a036e3bd03cbaf2747adc54f51f720dab4b48c8a346cb894d`

No employer messages were sent. Once the HH start lock clears and `mesh-hh-drive --alive` reports
up, the exact next check is:

```bash
~/.local/bin/mesh-job-reply --dry --json --max 1
```
