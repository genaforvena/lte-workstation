# Note 3 posture × rotation sense — verification follow-up — 2026-09-13

The on-demand paired reader and `--test` already existed in this worktree from the prior sense
implementation. Refreshed both live paths for this request; no duplicate tool or state writer was
added.

## Live evidence

- `scripts/mesh-note3-posture-rotation --test` — PASS; fixtures plus a real paired HAL read,
  `coverage=1/1 paired sample`, `pair_skew_ms=0.0`, `pair_age_ms=27.415`.
- `scripts/mesh-note3-posture-rotation --json` — exit 0; a separate fresh pair had
  `pair_skew_ms=2.797`, `pair_age_ms=34.696`.
- The executable source is mode `775`; its first lines declare `# orphan-ok:` for on-demand use.
  It is stateless, so the change-gated state-touch rule does not apply.

## Doctor gate and disposition

`mesh-doctor --quiet` reported hard failures for default egress through `tailscale0` and a selected
Tailscale exit node (`n2sbt7yy6t11CNTRL`), plus the default mic broken/busy warning. It also reported
the untimed `mesh-load-audit` peer SSH and existing funnel/absence warnings. The doctor test fan-out
continued past five minutes and spawned a large process tree; this run's process group was stopped.
Therefore no complete doctor PASS or clean orphan census is established, and no `[sense]` post was
made. Routing remains untouched.

## Next action

The routing owner must resolve or explicitly disposition the two egress failures; then run one
complete `mesh-doctor --quiet`. Only if it exits 0 with no new orphan WARN, refresh
`scripts/mesh-note3-posture-rotation --json` and post that artifact as `[sense]`.
