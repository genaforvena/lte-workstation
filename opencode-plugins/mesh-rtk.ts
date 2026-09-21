import { Plugin } from "@opencode/plugin"

// mesh-rtk — opencode port of the Claude PreToolUse hook
// (`rtk hook claude`, matcher Bash, in ~/.claude/settings.json).
//
// rtk has no opencode subcommand (claude|cursor|gemini|copilot|droid),
// but the underlying rewrite is engine-agnostic: it reads a Claude
// PreToolUse JSON ({tool_name, tool_input}) and returns updatedInput.
// Opencode's `tool.execute.before` gives us {tool, sessionID, callID} +
// output.args, so we adapt: wrap a bash call as a Claude PreToolUse
// payload, run `rtk hook claude`, and write updatedInput.command back.
// Non-bash tools pass through untouched. Fail-open: rtk absent or
// erroring leaves args as-is (a hook that breaks bash breaks everything).
export default Plugin.define({
  id: "mesh-rtk",
  async setup(ctx) {
    console.info("[mesh-rtk] plugin loaded")
    await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool !== "bash" && event.tool !== "Bash") return
      const input = event.input
      if (!input || typeof input !== "object") return
      const cmd = (input as Record<string, unknown>).command
      if (typeof cmd !== "string" || !cmd) return
      try {
        const payload = JSON.stringify({ tool_name: "Bash", tool_input: { command: cmd } })
        const p = Bun.spawn(["rtk", "hook", "claude"], {
          stdin: new TextEncoder().encode(payload),
          stdout: "pipe",
          stderr: "ignore",
        })
        const raw = await new Response(p.stdout).text()
        await p.exited
        const next = JSON.parse(raw)?.hookSpecificOutput?.updatedInput?.command
        if (typeof next === "string" && next && next !== cmd) (input as Record<string, unknown>).command = next
      } catch {
        // fail-open: leave args untouched
      }
    })
  },
})
