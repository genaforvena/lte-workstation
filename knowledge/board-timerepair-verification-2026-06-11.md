# mesh-board-timerepair verification

Date: 2026-06-11

What it does:
- Repairs only provably future-dated chat lines in `~/.mesh/chat.log`.
- Leaves past-dated and undated lines unchanged.
- Creates a `.pre-timerepair.bak` backup before rewriting the log.

Verification:
- `scripts/mesh-board-timerepair --test` passes.
- Dry-run on a fixture reports the expected number of future lines.
- Live fixture repair rewrites a future-stamped line to yesterday and preserves the other lines.

Verdict:
- Keep as a one-shot repair helper.
- It is still an orphan from the genome/canon point of view, so steward review should decide whether to wire it into the operating model or leave it as a deployment-side helper.

