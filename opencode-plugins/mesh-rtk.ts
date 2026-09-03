import type { Plugin } from "@opencode-ai/plugin"

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
export const MeshRtk: Plugin = async ({ client }) => {
  await client.app.log({ body: { service: "mesh-rtk", level: "info", message: "plugin loaded" } }).catch(() => {})
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash" && input.tool !== "Bash") return
      const cmd = output?.args?.command
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
        if (typeof next === "string" && next && next !== cmd) output.args.command = next
      } catch {
        // fail-open: leave args untouched
      }
    },
  }
}
