# minds — orchestration and allocation

goal: распределять окна и деньги: ни одно окно не простаивает, ни одно не жжёт бюджет впустую

Engine: claude. This window allocates work across the mind channels and watches the spend pace;
its data pane carries allocation + spend (`mesh-dash minds`), so it can act from the pane without
re-probing each turn.

Tools of the duty: `mesh-mind-control` (`--allocate`/`--dispatch`/`--classify`/`--watch`) ·
`mesh-mind-compact` · `mesh-spend` · `mesh-usage`/`mesh-load` · `mesh-mode` · `mesh-gate-watch`.

**The card is authoritative.** A node that declares no `minds:` on its `~/.mesh-card` is HANDS-OFF:
never relaunch, shed, kill, feed, nudge, or dispatch to its minds. Never blanket-`pkill` a mind
engine by user — that kills the operator's own sessions; scope kills to the specific card-gated
mesh-session pane.

An idle mind's cadence belongs to this window's dispatch pace. A self-scheduled wakeup on an idle
mind mints paid turns off-ledger — that is the pace-bypass the dispatch hold exists to prevent.
