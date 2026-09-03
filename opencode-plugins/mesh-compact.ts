import type { Plugin } from "@opencode-ai/plugin"

// mesh-compact — opencode port of the /clear-only doctrine + handoff discipline.
//
// Claude side: autoCompactEnabled + mesh-clear (write handoff → /clear → log)
// + mesh-handoff --snapshot (*/5 extractive safety net) + refs/wip commit.
// Opencode side: `compaction.auto` in config + this
// `experimental.session.compacting` hook, which injects what the default
// compaction prompt would otherwise drop: the window's charter goal, the
// board slugs it owes, and the refs/wip recovery pointer. Extractive, not
// inventive — mirrors the snapshot's "copies signal, invents no next-step".
export const MeshCompact: Plugin = async ({ client }) => {
  await client.app.log({ body: { service: "mesh-compact", level: "info", message: "plugin loaded" } }).catch(() => {})
  return {
    "experimental.session.compacting": async (input, output) => {
      const who = process.env.MESH_WHO ?? ""
      const win = who ? who.split("@")[0] : ""
      output.context.push(
        `## Mesh work-state that must survive compaction (extractive — copy, don't invent):` +
          `\n- Window: ${win || "(unknown — resolve via TMUX_PANE '#W')"}` +
          `\n- The window's charter goal (mesh-handoff --goal ${win || "<win>"} --oneline) and deadline countdown.` +
          `\n- Open board obligations owned by this window (slugs from mesh-promises --json: open/claims/holds where owner/debtor/taker == ${win || "<win>"}) — carry each slug + one-line lead.` +
          `\n- Uncommitted work pointer: refs/wip/${win || "<win>"} (recover: mesh-wip-commit --restore ${win || "<win>"}) — never describe tree state from memory, name the ref.` +
          `\n- Whatever was half-done + the literal next command, capped short. If unknown, say so rather than inventing a next step.`
      )
    },
  }
}
