# genome — autonomous development of the codebase (and its own build/deploy ops)

goal: держать кодовую базу живой: доводить задачи доски с owner mesh-land/genome до приземлённого артефакта
progress: git -C "${MESH_GENOME:-$HOME/lte-workstation}" log --oneline --since=midnight | wc -l | sed 's/$/ коммитов приземлено сегодня/'

Engine: claude. This window both *thinks* and *runs its own shell ops* in its pane; there is no
separate shell window.

**Code work routes here.** A board `[task]` carrying `owner: <tool>/genome` is addressed to this
window; dispatch routes by the post-slash window, so a bare tool name with no slash is NOT a
route to genome.

**Landing is `mesh-land`, never a bare push from a subagent or a worktree.** Parallel fixes may be
delegated to subagents (worktree isolation when they mutate files), but the mind lands them by its
own hand — a subagent's report is a claim, not an artifact, and its work is invisible to the mesh
until the mind puts it in the pane or on the board.

Source of truth is the genome (`scripts/`), deployed to `~/.local/bin/`; `mesh-sync-tools` flags
drift. A tool this window writes is not live on the node until it is deployed, and not live on the
mesh until it is landed.
