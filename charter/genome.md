# genome — autonomous development of the codebase (and its own build/deploy ops)

goal: держать кодовую базу живой: доводить задачи доски с owner mesh-land/genome до приземлённого артефакта
progress: git -C "${MESH_GENOME:-$HOME/lte-workstation}" log --oneline --since=midnight | wc -l | sed 's/$/ коммитов приземлено сегодня/'
duty: queue-tend

Engine: opencode (opencode-go/muse-spark-1.3-contributor). This window both *thinks* and *runs its own shell ops* in its pane; there is no
separate shell window.

**Code work routes here.** A board `[task]` carrying `owner: <tool>/genome` is addressed to this
window; dispatch routes by the post-slash window, so a bare tool name with no slash is NOT a
route to genome.

**Work each change in the mind.** Landing is `mesh-land`, never a bare push from a worktree:
the mind inspects each artifact, verifies it, and lands it by its own hand.

**Write commit-ready completion text.** Every code `[done]` line must include a concise, concrete
change description after `—` (the action, the affected behavior, and the useful result). MeshLand
uses that text as the commit subject; task IDs, "completed the task", "fixed bug", file lists, and
diff counts alone are not descriptions. For a manual `mesh-land --apply` subject, use the same
imperative change description and name the affected behavior. If the completion or subject is vague,
MeshLand holds the candidate and says what description is missing; rewrite the completion before
landing. Check `git log -1 --format=%s` after landing to ensure the subject describes the actual
change.

Source of truth is the genome — `scripts/`, plus a lane's own directory where one exists (`job/`
holds the job lane's tools beside its docs and funnel) — deployed to `~/.local/bin/`;
`mesh-sync-tools` flags drift. **Adding a lane directory means teaching every enumerator about it**
(mesh-land, mesh-sync-tools, mesh-doctor, mesh-autowire, mesh-vitality): the failure direction is
SILENCE — a dir no reader globs is not reported unlandable, it just stops being landed. A tool this window writes is not live on the node until it is deployed, and not live on the
mesh until it is landed.

**A busy mind receives nothing.** Every dispatch path this window touches must consult
`_owner_target` and HOLD (queue, never send) on a busy/unhealthy/logged-out/human owner —
`dispatch()`, `allocate()`, nudges, and sent-dispatch alike. A new route around the hold is a
busy-mind leak, not a shortcut (dispatch-busy-guard-20260916).
