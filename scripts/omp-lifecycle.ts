// mesh-omp-lifecycle extension — omp's native mesh lifecycle wiring.
//
// omp (Oh My Pi) has no hooks.json; its extension API (ExtensionFactory + pi.on) is the
// seam. This module shells out to scripts/mesh-omp-lifecycle (deployed at
// ~/.local/bin/mesh-omp-lifecycle), which mirrors mesh-codex-lifecycle:
//
//   session_start    → --start   (mesh-task reconcile + mesh-handoff --restore, and this
//                                  window's root session id is recorded as its identity —
//                                  the analogue of Codex's thread id).
//   session_stop     → --receipt (durable receipt + handoff + one TURN + quiet reset).
//   session_shutdown → --end     (last-chance drain for receipts the async handler missed).
//
// Every invocation passes the event JSON on stdin. The omp host is Bun, so the spawn goes
// through Bun.spawn; pi.exec has no stdin option. A spawn failure falls back to pi.exec
// with the JSON on argv so a host change degrades rather than drops the wiring.
//
// session_stop is omp's settle boundary and carries the identity natively: turn_id,
// session_id, messages, last_assistant_message, session_file. Firing it IS the terminal
// settle — the same call site then fires agent_end with willContinue only when a
// continuation was scheduled, and it fires AFTER session_stop, so subscribing here is the
// earlier and better-informed point.
//
// FAIL-SAFE IN BOTH DIRECTIONS. Every handler is wrapped: a throw in this module must
// never block a session_start and must never block the settle the mind needs. The --drain
// retry path (cron/reflex + --end) is the backstop, so a failed or slow lifecycle call only
// defers the receipt — it never loses the turn.
//
// Restore: --append-system-prompt is frozen at process spawn, so the live handoff reaches
// the model through mesh-handoff's hookSpecificOutput.additionalContext, which the omp host
// injects into the first context event of the new session. session_start here only
// reconciles the task pointer and records the root.

import type { ExtensionAPI, SessionShutdownEvent, SessionStartEvent, SessionStopEvent } from "@oh-my-pi/pi-coding-agent";

const TOOL = "mesh-omp-lifecycle";

/** Minimal shape of the text blocks read from assistant messages. */
interface TextBlock {
	type: "text";
	text: string;
}

interface MessageLike {
	role?: string;
	content?: unknown;
}

function isTextBlock(value: unknown): value is TextBlock {
	return typeof value === "object" && value !== null
		&& (value as { type?: unknown }).type === "text"
		&& typeof (value as { text?: unknown }).text === "string";
}

function lastAssistantText(messages: readonly MessageLike[]): string {
	for (let i = messages.length - 1; i >= 0; i--) {
		const message = messages[i];
		if (message.role !== "assistant" || !Array.isArray(message.content)) continue;
		const text = message.content
			.filter(isTextBlock)
			.map((block) => block.text)
			.join("\n")
			.trim();
		if (text) return text;
	}
	return "";
}

export default async function (pi: ExtensionAPI): Promise<void> {
	const log = (level: "info" | "warn" | "error", message: string, context?: Record<string, unknown>): void => {
		pi.logger[level](message, context);
	};

	const emit = async (mode: string, event: Record<string, unknown>): Promise<void> => {
		const payload = JSON.stringify(event);
		try {
			// Bun is the omp host. Bun.spawn pipes stdin; pi.exec cannot.
			const child = Bun.spawn([TOOL, "--" + mode], {
				stdin: "pipe",
				stdout: "pipe",
				stderr: "pipe",
				// Bun.spawn without an explicit env uses the process-start snapshot, so a
				// runtime change to process.env (restore.env, /clear re-read) would be lost.
				env: process.env,
			});
			// Bun.spawn's stdin is a FileSink, not a WritableStream: write the bytes
			// directly, then end the stream so the tool's stdin read returns.
			child.stdin.write(payload);
			await child.stdin.end();
			const code = await child.exited;
			const stderr = await new Response(child.stderr).text();
			if (code !== 0) {
				log("warn", `${mode} rc=${code}`, { stderr: stderr.slice(0, 400) });
			}
		} catch (spawnError) {
			// A non-Bun host or a spawn failure must not lose the wiring: retry through
			// pi.exec with the JSON on argv.
			try {
				const result = await pi.exec(TOOL, ["--" + mode, payload], { timeout: 20_000 });
				if (result.code !== 0 && result.stderr) {
					log("warn", `${mode} rc=${result.code}`, { stderr: result.stderr.slice(0, 400) });
				}
			} catch (execError) {
				log("error", `${mode} failed`, {
					spawn: spawnError instanceof Error ? spawnError.message : String(spawnError),
					exec: execError instanceof Error ? execError.message : String(execError),
				});
			}
		}
	};

	pi.on("session_start", async (_event: SessionStartEvent) => {
		await emit("start", {});
	});

	pi.on("session_stop", async (event: SessionStopEvent) => {
		// stop_hook_active marks the pre-settle pass a stop-hook continuation requested; that
		// pass is by design a non-terminal scheduling point, not a user-visible turn boundary.
		if (event.stop_hook_active) return;
		await emit(
			"receipt",
			{
				type: "agent-turn-complete",
				"session-id": event.session_id,
				"turn-id": event.turn_id,
				"last-assistant-message": (event.last_assistant_message
					&& lastAssistantText([event.last_assistant_message as MessageLike]))
					|| lastAssistantText(event.messages as MessageLike[]),
				"session-file": event.session_file ?? "",
			},
		);
	});

	pi.on("session_shutdown", async (_event: SessionShutdownEvent) => {
		// Process exit is the last retry point for a receipt the asynchronous settle
		// handler did not finish. Best-effort: a slow shutdown must not hang the host.
		await emit("end", {});
	});

	log("info", "mesh omp lifecycle extension loaded");
}
