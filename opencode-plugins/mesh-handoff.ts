import type { Plugin } from "@opencode-ai/plugin"

// mesh-handoff — opencode port of the Claude SessionStart hook
// (`mesh-handoff --restore` in ~/.claude/settings.json, matcher startup|clear).
//
// Claude injects charter + handoff as SessionStart additionalContext.
// Opencode has no SessionStart hook; the closest seam is
// `experimental.chat.system.transform`, which runs per session and lets us
// prepend the same two tiers (charter = what this window IS,
// handoff = what it was doing) to the system prompt.
//
// Window resolution mirrors mesh-handoff: MESH_WHO first (board attribution),
// TMUX_PANE → tmux window name second. Injected once per sessionID so a
// long session is not re-bloated every turn. Best-effort: any failure
// resolves to empty (a hook that breaks the session is worse than no context).
const seen = new Set<string>()

async function sh(cmd: string): Promise<string> {
  try {
    const p = Bun.spawn(["bash", "-lc", cmd], { stdout: "pipe", stderr: "ignore" })
    const out = await new Response(p.stdout).text()
    await p.exited
    return out.trim()
  } catch {
    return ""
  }
}

async function thisWindow(): Promise<string> {
  const who = process.env.MESH_WHO ?? ""
  if (who) return who.split("@")[0]
  const pane = process.env.TMUX_PANE ?? ""
  if (!pane) return ""
  const win = await sh(`tmux display-message -p -t "${pane}" '#W' 2>/dev/null`)
  return win.split("\n")[0]?.trim() ?? ""
}

async function shRc(cmd: string): Promise<{ out: string; rc: number }> {
  try {
    const p = Bun.spawn(["bash", "-lc", cmd], { stdout: "pipe", stderr: "ignore" })
    const out = (await new Response(p.stdout).text()).trim()
    const rc = await p.exited
    return { out, rc }
  } catch {
    return { out: "", rc: 127 }
  }
}

function shQuote(s: string): string {
  return "'" + s.replace(/'/g, "'\\''") + "'"
}

// Pre-switch snapshot: the TUI-side /clear IS session.new (alias of /new),
// so a mind that clears by hand instead of mesh-clear would otherwise drop
// its thread and the next session would restore a STALE handoff. Snapshotting
// on session.new closes that exact hole; mesh-clear's own pre-write stays the
// primary path (rc 0/4/5/6 all mean "best available handoff is in place").
// session.deleted gets the same best-effort snapshot. What has NO hook by
// construction is a bare TUI exit or window close — no event fires — so those
// still rest on the pre-clear write + the 5-minute snapshot reflex + refs/wip.
async function snapshotWin(
  client: { app: { log: (a: unknown) => Promise<unknown> } },
  why: string
): Promise<void> {
  try {
    const win = await thisWindow()
    if (!win) return
    const { rc } = await shRc(`mesh-handoff --snapshot ${shQuote(win)} >/dev/null 2>&1`)
    await client.app
      .log({ body: { service: "mesh-handoff", level: rc <= 6 ? "info" : "warn", message: `pre-switch snapshot (${why}) win=${win} rc=${rc}` } })
      .catch(() => {})
  } catch {
    // fail-safe is SILENCE — never break a session switch on our own malfunction
  }
}

export const MeshHandoff: Plugin = async ({ client }) => {
  await client.app.log({ body: { service: "mesh-handoff", level: "info", message: "plugin loaded" } }).catch(() => {})
  return {
    "experimental.chat.system.transform": async (input, output) => {
      const sid = input.sessionID ?? ""
      if (!sid || seen.has(sid)) return
      const win = await thisWindow()
      if (!win) {
        await client.app.log({ body: { service: "mesh-handoff", level: "warn", message: "skip: no window (MESH_WHO and TMUX_PANE both empty)" } }).catch(() => {})
        return
      }
      const safe = win.replace(/[^A-Za-z0-9._-]/g, "_")
      const home = process.env.HOME ?? ""
      const charter =
        (await sh(`cat "${home}/.mesh/charter/${safe}.md" 2>/dev/null || cat "$PWD/charter/${safe}.md" 2>/dev/null`)) ||
        ""
      const handoff = await sh(`cat "${home}/.mesh/handoff/${safe}.md" 2>/dev/null`)
      const parts: string[] = []
      if (charter)
        parts.push(
          `Charter for the \`${win}\` window (durable INSTRUCTION, not work-state — what this window IS and what it owes):\n\n${charter.slice(0, 6000)}`
        )
      if (handoff)
        parts.push(
          `Work-memory handoff restored (mesh-handoff, pre-/clear). This is YOUR thread from before the /clear — resume from it:\n\n${handoff.slice(0, 4000)}`
        )
      if (parts.length) {
        output.system.push(parts.join("\n\n---\n\n"))
        seen.add(sid)
        await client.app.log({ body: { service: "mesh-handoff", level: "info", message: `injected charter=${charter ? "yes" : "no"} handoff=${handoff ? "yes" : "no"} win=${win}` } }).catch(() => {})
      }
    },
    event: async ({ event }) => {
      const t = (event as { type?: string }).type ?? ""
      if (t === "tui.command.execute") {
        // /clear IS session.new (alias of /new) — snapshot the outgoing thread.
        const cmd = (event as { properties?: { command?: string } }).properties?.command ?? ""
        if (cmd !== "session.new") return
        await snapshotWin(client, "session.new")
        return
      }
      if (t === "session.deleted") {
        await snapshotWin(client, "session.deleted")
      }
    },
  }
}
