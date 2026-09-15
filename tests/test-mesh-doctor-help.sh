#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
doctor="${MESH_DOCTOR_SCRIPT:-$repo/scripts/mesh-doctor}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/home"

set +e
HOME="$tmp/home" PATH=/usr/bin:/bin MESH_GENOME="$repo" MESH_REPO="$repo" \
  timeout 3s "$doctor" --help >"$tmp/help.out" 2>&1
rc=$?
set -e

if [ "$rc" -ne 0 ] || ! grep -Fq 'Usage: mesh-doctor' "$tmp/help.out"; then
  cat "$tmp/help.out" >&2
  echo "FAIL: --help must print usage and exit 0 (rc=$rc)" >&2
  exit 1
fi
if [ -e "$tmp/home/.mesh/doctor.log" ] || [ -e "$tmp/home/.mesh/.doctor.lock" ]; then
  echo "FAIL: --help entered the doctor run path" >&2
  exit 1
fi
echo "PASS: --help prints usage without entering the doctor run path"
