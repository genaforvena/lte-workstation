#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT

frame="$(cat <<'FRAME'
goal-source=FRESH · ЦЕЛЬ НЕ ОБЪЯВЛЕНА
== check data (refresh 30s) — 2026-09-28T20:00:00Z — all text ==
  self: IDLE · last /clear 6d ago · spend: mesh-spend --tokens
egress enp42s0 | supervised 4UP/0DOWN | organs 15LIVE/0DARK
-- FLEET (ALL nodes — LIVE, 1s) --
  9 nodes: 3 ssh · 2 lan · 4 down | PATH: OK peers=8 direct=2 relay=0 offline=6
  up: mesh-home(LOCAL vitals=OK) · imac-rozalia(NO-CARD)
-- DOCTOR (this node, cached 4m): 2026-09-28T19:56:00Z UNKNOWN doctor --cron deferred --
  ✗ UNKNOWN full doctor remains deferred
  ✗ prior snapshot (may be stale): FAIL
-- CPU/GPU load (who's busy — load-audit + vram-watch, cached) --
  load-audit(1m): CPU=QUIET · GPU=GPU-IDLE · load1=9.12/16c
  GPU HEALTHY (5m): vram=4576/12288M(37%) util=14% temp=50C throt=0x0
  GPU decoder: {"source":"nvidia-smi"}
-- organs: all LIVE (none DARK) --
  146 states: 16 alarm · 33 stale · 97 quiet
  ✗ source alarm omitted from the full roster
-- autopoiesis: reflexes=OK vitality=OK | feed 4m | evolve 50s | streams none --
-- pane live 2026-09-28T20:00:00Z · 30s · ticks every frame --
FRAME
)"

rendered="$(printf '%s\n' "$frame" | MESH_DASH_PANE_ROWS=11 MESH_DASH_PANE_COLS=80 \
  python3 "$ROOT/scripts/mesh-dash-pane-compact.py" check "$fixture")"

stats="$(printf '%s\n' "$rendered" | python3 -c 'import sys; d=sys.stdin.read().splitlines(); print(len(d), sum(max(1, (len(line)+79)//80) for line in d), max(map(len, d), default=0))')"
read -r lines rows max_width <<<"$stats"
[ "$rows" -le 9 ] \
  || { echo "FAIL: compact check uses $rows rows ($lines lines, max width $max_width); 11-row pane reserves 2 rows for the live lease" >&2; exit 1; }
[ "$max_width" -le 80 ] \
  || { echo "FAIL: compact check contains a $max_width-column row" >&2; exit 1; }
for marker in \
  'goal-source=FRESH · check=2026-09-28T20:00:00Z' \
  '-- FLEET LIVE · 9 nodes:' \
  '-- DOCTOR UNKNOWN · cached=4m · full doctor deferred' \
  '-- CPU/GPU CPU=QUIET GPU=HEALTHY/5m vram=4576/12288M(37%) util=14% temp=50C' \
  '-- organs 15LIVE/0DARK · 146 states · 16 alarm · 33 stale · 97 quiet' \
  '-- autopoiesis reflexes=OK vitality=OK feed=4m evolve=50s streams=none' \
  'supervised=4UP/0DOWN' \
  'omitted: node/VPN/doctor/organ details; full=mesh-dash --once check'; do
  printf '%s\n' "$rendered" | grep -Fq -- "$marker" \
    || { echo "FAIL: short check projection lost required marker: $marker" >&2; exit 1; }
done
printf 'test-mesh-dash-health-pane-fit: PASS (%s rows at 80 columns; FLEET/DOCTOR/GPU/organs/liveness preserved)\n' "$rows"
