#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
rules="$root/AGENTS.md"
test -s "$rules"
grep -Fq 'mesh-unblock' "$rules"
grep -Fq 'GPU, VRAM, Ollama residency' "$rules"
grep -Fq 'FYI/chat lines as evidence' "$rules"
grep -Fq '`mesh:3`' "$rules"
grep -Fq '`mesh:7`' "$rules"
grep -Fq '`mesh:8`' "$rules"
grep -Fq 'node-owned' "$rules"
grep -Fq 'mesh-unblock' "$rules"
grep -Fq 'invariant-registry' "$rules"
grep -Fq 'WE DO NOT GUESS' "$rules"
# No second copy and no pointer file: the contract lives in AGENTS.md only.
test ! -e "$root/MESH.md"
# No duplicate contract: mesh: bullets and the registry live in exactly one doctrine file.
test "$(grep -rl 'invariant-registry' "$root/AGENTS.md" "$root/CLAUDE.md" 2>/dev/null | wc -l)" = "1"
! grep -Fq '`mesh:12`' "$root/CLAUDE.md"
echo 'test-mesh-mind-rules-wake: PASS'
