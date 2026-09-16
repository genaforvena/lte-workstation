---
name: mesh-operator-followthrough
description: Carry an actionable operator request from intake through durable task ownership, verified result, and requested delivery in any mesh window. Use for deferred or multi-step work, including Telegram handoffs.
---

Read the current window charter with `mesh-handoff --charter <window>`; its account,
resource and communication boundaries apply. A chat reply or handoff is not a queue entry.

Node-local resource coordination is part of mesh follow-through: temporary CPU, memory, GPU,
VRAM, and resident Ollama-model contention is an internal queued/retry decision, not an
operator-facing permanent block. Before a resource-bound attempt, record the measured
headroom and choose an available slot, bounded retry edge, or safe preemption. On mesh-home,
GPU jobs use `mesh-heavy-run` with `MESH_HEAVY_GPU_PREEMPT=1` and the measured minimum-free-
VRAM threshold; its `mesh-gpu-lease` may stop and later restore only mesh-managed services.
Never stop, signal, or reinterpret an unrelated external process. Preserve active/protected
consumers, refuse ambiguous ownership, and make the stop/restart decision explicit in the
artifact; if the lease cannot reach headroom, restore managed state and keep the task queued.

This is an adjustable workflow, not a fixed ritual. Adapt and improve the shared skill
when evidence shows a better procedure; record the reason and verify the change.
Follow the living-skill guidance in mesh-window-turn. Do not weaken authorization,
ownership, privacy, or receipt/verification requirements through a skill edit.

Before promising deferred work or starting a multi-step request:

1. Preserve the inbound ask key supplied by the channel. For direct pane requests use
   a unique, stable key and record its source in the plan. Read `mesh-task replay --json`
   and search that key before creating work; reuse the existing chain on redelivery.
2. Write a durable TSV plan, using `owner<TAB>step<TAB>description`. Descriptions name
   the expected artifact and the operator's actual acceptance condition. If delivery
   is requested, include a delivery step owned by the authorized channel, with receipt
   as its artifact. Run `mesh-task create <chain> <plan.tsv> <ask-key>`.
3. The exact owner runs `mesh-task take <chain> <step>` before execution. A routing
   message means offered, not claimed. Say queued only after verifying the queue row.
4. Continue authorized work. Record progress using `mesh-task progress <chain> <step>
   <artifact> <next-action> <next-update-ISO>`. Contention or a missing prerequisite needs
   a typed block with a concrete retry event, not an untracked "later" in a handoff.
5. Verify the requested result, then run `mesh-task done <chain> <step> <artifact>
   [result]`. Board prose alone cannot settle the ledger. Rejection needs a concrete
   reason via `mesh-task reject`; an acknowledgment is not completion.

For requested delivery, save the source ask key, task ID, artifact path/digest,
destination, time, and transport message/file ID (or the tool's actual receipt).
Check existing receipts before retrying. If a send may have succeeded but its receipt
is missing, reconcile the sent log before sending again. A successful text fallback
does not prove a requested file arrived. Keep that delivery step open with the exact
failure and retry edge until verified. This skill does not authorize new recipients,
messages, account access, or repeated external actions outside the user's scope.

Ordinary questions answered fully in this turn need a factual reply, not a fabricated
work chain. Separate the answer from any still-open action request in the same message.
Keep private job, account, and message data in node-local evidence, not public receipts.

Full lifecycle command contract: `docs/operator-task-lifecycle.md` in the genome.
