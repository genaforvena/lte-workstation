#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
rules="$root/MESH.md"
test -s "$rules"
grep -Fq 'mesh-unblock' "$rules"
grep -Fq 'GPU, VRAM, Ollama residency' "$rules"
grep -Fq 'FYI/chat lines as evidence' "$rules"
grep -Fq '`mesh:3`' "$rules"
grep -Fq '`mesh:7`' "$rules"
grep -Fq '`mesh:8`' "$rules"
grep -Fq 'node-owned' "$rules"
grep -Fq 'mesh-unblock' "$rules"
grep -Fq 'MESH.md' "$root/AGENTS.md"
grep -Fq 'MESH.md' "$root/CLAUDE.md"
echo 'test-mesh-mind-rules-wake: PASS'
