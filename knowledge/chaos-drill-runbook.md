# Chaos Drill Runbook — First Supervised-Reflex Drill

**Status**: Ready to run. Requires operator to write `~/.mesh/chaos.optin` (gated).

---

## What this drills

`mesh-chaos` exists and is hardened, but `~/.mesh/chaos.optin` is empty — no experiments
have ever run. This runbook executes the first real chaos drill: SIGTERM each supervised
loop reflex and confirm `mesh-supervise` restarts it within 30 seconds.

**What it proves**: the supervision tree actually recovers reflexes mid-life, not only at
reboot. This is the "self-healing supervision" gap from `eternity-and-its-fields.md`.

---

## Pre-flight

```bash
mesh-supervise --status          # all must be UP before starting
mesh-chaos --report              # baseline (will show only "no opt-in" lines)
cat ~/.mesh/supervise.list       # confirm the patterns match what mesh-chaos will target
```

---

## Step 1 — operator writes opt-in (gated)

```bash
cat > ~/.mesh/chaos.optin << 'EOF'
# Supervised reflex resilience drill — first chaos run on ilya.
# Only reflex: class (supervised loops). NO substrate experiments.
reflex:mesh-chat --watch
reflex:mesh-trace --watch
reflex:mesh-snapshot --loop
reflex:mesh-provenance --loop
reflex:mesh-selfcare --loop
EOF
```

These patterns each match exactly ONE process (the `-f` pgrep pattern is the loop's
command line). `mesh-sync-tools --loop` is excluded from the first drill because its
loop interval is 3600s — slow recovery would be a false alarm, not a fault.

`mesh-session-watchdog` is excluded: it monitors minds and could produce noisy alerts
during the drill.

---

## Step 2 — dry run (safe, no kill)

```bash
# Run dry-run 5 times to cycle through all 5 experiments (one per minute-bucket)
for i in $(seq 1 5); do
  mesh-chaos --dry
  sleep 61   # wait for next clock-minute bucket
done
```

Verify each experiment is printed without "refused" or "AMBIGUOUS".

---

## Step 3 — run one real experiment

```bash
mesh-chaos          # fires one experiment (clock-minute-indexed, rotating)
sleep 60            # wait for mesh-supervise */2 cron to fire
mesh-supervise --status   # should show all UP
mesh-chaos --report       # should show RECOVERED ✅ for the experiment
```

Expected output in chaos.log:
```
2026-..T..Z EXPERIMENT reflex:mesh-trace --watch — SIGTERM pid XXXXX (...)
2026-..T..Z RECOVERED reflex:mesh-trace --watch (new pid YYYYY) ✅
```

---

## Step 4 — run the full rotation

```bash
# 5 experiments, one per minute — covers all opted-in reflexes
for i in $(seq 1 5); do
  mesh-chaos
  sleep 61
done
mesh-supervise --status     # all UP
mesh-chaos --report         # 5x RECOVERED ✅
```

---

## Step 5 — record the resilience artifact

```bash
mesh-chaos --report >> ~/.mesh/knowledge/chaos-drill-results.md
mesh-chat "[done] ilya: first chaos drill complete. $(grep -c RECOVERED ~/.mesh/chaos.log)/5 reflexes confirmed self-healing. Resilience is a measured fact."
```

---

## What RECOVERED means

Each `RECOVERED ✅` line is a **measurable proof** that:
- The supervisor detects the dead process within one `*/2` cron cycle (≤120s)
- The restart command in `supervise.list` correctly relaunches the loop
- The new pid is distinct (not the same process returning from SIGTERM ignore)

A `RESILIENCE GAP` line means the reflex has no supervisor — it needs a `supervise.list`
entry or a `Restart=` unit directive.

---

## Pause / abort at any point

```bash
touch ~/.mesh/chaos.pause   # immediate kill-switch (mesh-chaos checks this first)
```

Remove with `rm ~/.mesh/chaos.pause` after investigating.

---

## After the drill

```bash
rm ~/.mesh/chaos.optin   # optional: remove to return to dormant state
# OR leave it — periodic scheduled chaos is the intended steady-state
```

The field recommendation (`fields-to-mine.md`) is to leave it running as a **standing
reflex** — the drill becomes continuous resilience verification, not a one-time event.
Wire it to `*/30 mesh-chaos` in crontab after confirming the full rotation passes.
