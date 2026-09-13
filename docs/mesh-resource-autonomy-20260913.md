# Mesh resource and task autonomy

The five-minute `mesh-task-unblock-sweep` reflex now repairs two gaps before running the witness
queue check: it creates one exact-owner resolver for a recent prerequisite-based rejection, and it
verifies that runnable work is visible and claimable through the normal owner queue. Repeated sweeps
reuse the existing resolver. Historical rejections and rejections for invalid or duplicate work do
not reopen automatically. New task descriptions instruct minds to find or create prerequisite work,
implement mesh-owned requirements, and make internal registration choices from evidence without
waiting for permission. An unavailable external datum stays an explicit, retryable blocker while
independent internal work continues.

GPU-bound work on mesh-home can ask `mesh-heavy-run` to obtain declared VRAM headroom with
`MESH_HEAVY_GPU_PREEMPT=1`. The lease touches only `mesh-voice-clone.service`,
`mesh-room-gigaam.service`, and `ollama.service`. It records which allowlisted services were active,
stops only those services, checks measured free VRAM, and restores the recorded active set on normal
exit or lease expiry. A failed acquisition restores immediately and leaves the job queued. Expired
leases are swept once per minute; the default lease is 45 minutes and the maximum is 60 minutes.
Study launches request a 45-minute lease, bounded by the existing heavy-run budget and memory and
pressure gates. The lease helper has a failure cooldown to prevent repeated service churn when the
declared capacity still cannot be reached.

The lease has only been exercised with fake `systemctl` and `nvidia-smi` commands in tests; no live
GPU services were stopped for verification. The five-minute task sweep is already installed in cron.
These source changes become the recurring production behavior once the branch is landed through the
mesh repository's normal landing path.
