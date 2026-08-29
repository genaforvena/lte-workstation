# wake — the finnegans-fake distillation lane

goal: гнать дистилляцию finnegans-fake до артефакта, а не до плана

Engine: claude. Repo: `~/finnegans-fake` — the distillation of the board corpus into a local
Finnegans-Wake-style model. Data pane: the `wake)` arm of `mesh-dash` — scored rungs recomputed
from `wake/recs-*.json`, the trained adapters from their own `trainlog.json`, and whether a run is
in flight.

**This lane's founding failure is DISAPPEARANCE, and the charter exists to make that impossible.**
`wake` was a hand-created window, never an `ensure_uniform_channel` call, so when it went it left a
trace in NO list: absent from the session, absent from `MESH_MIND_CHANNELS`, and absent from
`MESH_RETIRED_CHANNELS` too. A name in NEITHER list declares nothing — a lane with no mind then
reads exactly like a lane with nothing to say, and no watchdog can separate them (roll-call cannot
even call it SILENT, because the expected set is built from the channel set). Two days of "no
progress" went unnoticed that way. Restored by the operator 2026-08-18. **To retire it, put it in
`MESH_RETIRED_CHANNELS` — that is a DECLARATION of absence; deleting the window is not.**

**The pane must carry what the window is FOR.** Before the `wake)` arm existed the top pane fell
through to the node card — a surface that looks healthy and holds nothing this lane needs.
`mesh-dash --test` goes RED if it ever does again; keep it that way.

**A score is only a score against the run that produced it.** Last recorded state is "144 folds
still lose to 47" — quote the run, not the number alone, and re-derive rather than copying a
figure into prose. [[calibrate-a-derived-axis-against-the-live-corpus]]

**Training runs are long and this node power-cycles.** A run in flight is state that no `/clear`
and no reboot preserves: write the handoff before sleeping on it, and treat a slot that spans a
power-off as UNMEASURED rather than as a quiet one.
[[an-age-that-spans-a-power-off-is-not-a-silence]]

Owed to the board: `[fyi]` when a rung moves, `[done]` for a completed run with its scores, and one
`[idle]` line naming whether a run is in flight — never silence, which is this lane's own fault
mode.
