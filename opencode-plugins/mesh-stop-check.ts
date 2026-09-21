import { Plugin } from "@opencode/plugin"

// mesh-stop-check — opencode port of the Claude Stop hook
// (`mesh-stop-check` in ~/.claude/settings.json).
//
// STRUCTURAL GAP, stated plainly: Claude's Stop hook can `decision: block`
// and the engine feeds `reason` back as the next turn. Opencode's
// `session.idle` event is observe-only — it cannot block the stop. So this
// port does the observable half: on idle it runs the SAME verdict
// (`mesh-stop-check --dry-run <win>`, same board + same ledger) and, when
// the verdict is WOULD BLOCK, re-wakes the mind by appending the reason as
// a session message via the SDK client. A missed wake is still caught by
// the next board write via mesh-fsnotify/mesh-dispatch — the same
// fail-safe direction as the Claude hook (errors → allow the stop).
export default Plugin.define({
  id: "mesh-stop-check",
  async setup(ctx) {
    console.info("[mesh-stop-check] plugin loaded")
    const controller = new AbortController()
    void (async () => {
      for await (const item of ctx.event.subscribe({ signal: controller.signal })) {
        const event = item as { type?: string; properties?: { sessionID?: string } }
        if (event.type !== "session.idle") continue
        const sessionID = event.properties?.sessionID ?? ""
      if (!sessionID) continue
      const who = process.env.MESH_WHO ?? ""
      const win = who ? who.split("@")[0] : ""
      if (!win) continue
      try {
        const p = Bun.spawn(["mesh-stop-check", "--dry-run", win], {
          stdout: "pipe",
          stderr: "ignore",
        })
        const out = await new Response(p.stdout).text()
        await p.exited
        if (!out.includes("WOULD BLOCK")) continue
        const reason = out.replace(/^mesh-stop-check: WOULD BLOCK.*\n/, "").slice(0, 2000)
        await ctx.session.prompt({
          sessionID,
          text: `mesh-stop-check (opencode idle port — Claude Stop:block has no equivalent here, so this re-wakes instead):\n\n${reason}\n\nResolve each: discharge it ([done] <slug> / [fyi] with the result), or post one [idle] line stating why and stop.`,
        })
      } catch {
        // fail-safe is ALLOW — never pin a mind awake on our own malfunction
      }
      }
    })()
    return () => controller.abort()
  },
})
