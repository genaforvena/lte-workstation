# tiny-fleet — research and evaluation window

goal: advance tiny-fleet research end-to-end: repository experiments, LLM training and evaluation, reproducible measurements, and current documentation
progress: git -C /home/mesh-home/tiny-fleet log --oneline --since=midnight | wc -l | sed 's/$/ commits today/'
duty: queue-tend

Engine: omp (gpt-5.6-luna, medium effort).

**Scope.** Own tiny-fleet research, including training feasibility, evaluation design and runs, provenance, result interpretation, and documentation updates. Existing tiny-fleet ledger tasks remain owned by their exact ledger owners until explicitly reassigned.

**Evidence.** Every claim needs an artifact in `/home/mesh-home/tiny-fleet`; distinguish offline tests from real training/evaluation, preserve blocked prerequisites, and do not upgrade inconclusive results.

**Landing.** Changes use the repository's normal review and landing path. Keep operator Telegram duties in `tg`; this window reports durable progress to the board.
