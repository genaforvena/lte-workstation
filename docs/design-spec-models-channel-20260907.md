# Models-channel obligation map — 2026-09-07

Task: `design-spec-task-sweep-20260907/spec-models-channel`

Status: complete as a disposition map; owner `tg`.

Source: `docs/superpowers/specs/2026-07-15-models-channel-design.md`.

## Obligation → evidence

| obligation | disposition | evidence or named open task |
|---|---|---|
| Observe the live model by each consumer; UNKNOWN rather than defaults | LANDED | `scripts/mesh-model-resolve`, deployed `~/.local/bin/mesh-model-resolve`; `--test` rc=0, output SHA `9415994b434e534231f7141ba6ccc7a2d34930f5df1da5d2eb4d8e1fc324db0d` |
| Report STT consumers independently | LANDED | resolver rows include room-ear and voice-rx; live voice-rx resolves `ggml-large-v3-turbo-q5_0.bin` |
| Bench wall-clock and WER, both mandatory | LANDED | `scripts/mesh-model-bench`; deployed `--test` rc=0, output SHA `9f2df494676a9239d2680743a10673cb159e56a2197cf1d7793a8ba1438baeb0` |
| Durable fixture pair with provenance and truth | LANDED | `~/.mesh/model-fixtures/stt-ru-operator-0812/{input.wav,truth.txt,provenance.txt}`; additional TTS, wake, diarization fixtures present |
| Append-only measured ledger | LANDED | `~/.mesh/model-bench.log`, 64 lines, SHA `8290fed55e094c3677ff43f7b09438aaae71b70f82fcbf4ec8f3c82190253c2a` |
| Models pane shows live/perf/UNMEASURED | LANDED | `scripts/mesh-dash` models role at lines 3012+, resolver + ledger + shelf/UNMEASURED rendering; `--test-fast` rc=0, output SHA `a4a52c9b5009fffdc6c5a64d01313cb7ce4f696c4a6f0525243c1549a8e8926c` |
| Seed real STT candidates rather than prose backfill | LANDED | ledger contains real STT rows for tiny, base, turbo-q5_0, and GigaAM with wall/fixture/WER fields |
| Persist models window in restore manifest | LANDED | `scripts/mesh-restore:mcp_full_for_win` has models arm; manifest includes `ensure_uniform_channel models` and smoke loop |
| Reboot wiring | LANDED | `@reboot mesh-restore` remains in the existing restore/cron wiring; no new schedule invented |
| Commit and push persistence changes | OPEN | named follow-up: `design-spec-task-sweep-20260907/final-design-spec-verification` must run repository sync/push and independently verify remote state |
| Full live restore kill/replant test | OPEN | `mesh-restore --test` reached a real node-condition failure (block-1 code failure rc=2); preserve that failure until the live tmux restore gate is rerun under `final-design-spec-verification` |
| Candidate search task-fit filter | OPEN | `design-spec-task-sweep-20260907/spec-model-watch` (new implementation task required after this map); current `mesh-model-watch` is deliberately unscheduled and documents the biased-candidate gap |

## Focused verification

```text
mesh-model-resolve --test: rc=0
mesh-model-bench --test: rc=0
mesh-model-watch --test: rc=0, 9/9 passed
mesh-model-autoselect --test: rc=0
mesh-model-swap --test: rc=0
mesh-dash --test-fast: rc=0
mesh-restore --test: rc=1, honest node-condition/code-failure boundary retained above
```

Source SHA256:

```text
mesh-model-resolve  2a26293142c97c697a729ab0d37fcfcdf9540c698a1e7f2c7601b3d0cc76356e
mesh-model-bench    1bdcfb7b0504d78c7c9780d002a07cefa5dd3282a6921d6de863ccefdb8ba082
mesh-model-watch    eb1be06c1d96e2c63fdf17e98f47eacd58c149ee405bf2a63a20bf1809937405
mesh-model-autoselect 01e5e8ab52fef617871ef72fb2aad69be5e209f7db8fec559548fcb160fe9c68
mesh-model-gap      dd3b4b099d11e028630ab07a77cc5982ee30a8cfa7c623502f706f884f6914a1
mesh-dash           9f0736770a23a8f20759d70eecc2a4bc7ddbbef7f243b10d9f0524d421982225
mesh-restore        c5ad7ec0ca2dfd06434ff4264debea582ed881f92aa6a2a851cf246608364b64
reflexes.cron       e4aa5b25db3f263e9e12d1fae9c8976e61ab9226ebf7a6c06a95d50011799167
```

This map does not claim the two OPEN follow-ups are complete.
