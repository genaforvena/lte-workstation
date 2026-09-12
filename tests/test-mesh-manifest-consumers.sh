#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d -t mesh-manifest-consumers.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

repo="$tmp/repo"
mkdir -p "$repo/scripts" "$repo/job" "$tmp/bin"
reader="$root/scripts/lib/mesh-manifest-reader.sh"
source "$reader"

cat > "$repo/scripts/mesh-manifest" <<'EOF'
#!/usr/bin/env bash
case "${1:-}" in
  --check) [ "${MESH_MANIFEST_FIXTURE_CHECK:-0}" = 0 ] ;;
  --list) cat "$MESH_MANIFEST_FIXTURE_ROWS" ;;
  *) exit 2 ;;
esac
EOF
chmod +x "$repo/scripts/mesh-manifest"

rows="$tmp/rows.tsv"
cat > "$rows" <<'EOF'
# mesh-manifest v1
source_path	installed_basename	domain	kind	deploy_policy	cadence_policy	compatibility_owner
scripts/mesh-compat	mesh-compat	core	tool	install	none	scripts:mesh-compat
scripts/sub/mesh-compat		core	tool	none	none	scripts:mesh-compat
scripts/sub/mesh-nested	mesh-nested	operations	tool	install	none	scripts:mesh-nested
scripts/sub/mesh-worker.service		operations	unit	systemd	unit	scripts:mesh-worker.service
scripts/README.md		operations	asset	none	none	scripts:README.md
EOF

MESH_MANIFEST_FIXTURE_ROWS="$rows" mesh_manifest_tool_paths "$repo" > "$tmp/tools"
grep -qx 'scripts/mesh-compat' "$tmp/tools"
grep -qx 'scripts/sub/mesh-nested' "$tmp/tools"
! grep -qx 'scripts/sub/mesh-compat' "$tmp/tools"
MESH_MANIFEST_FIXTURE_ROWS="$rows" mesh_manifest_unit_paths "$repo" > "$tmp/units"
grep -qx 'scripts/sub/mesh-worker.service' "$tmp/units"
MESH_MANIFEST_FIXTURE_ROWS="$rows" mesh_manifest_orphan_paths "$repo" > "$tmp/orphans"
grep -qx 'scripts/sub/mesh-nested' "$tmp/orphans"
grep -qx 'scripts/sub/mesh-worker.service' "$tmp/orphans"

# The adapter itself must refuse both an unknown classification and a repeated installed owner,
# without leaking a partial path list to a consumer.
sed 's/operations\ttool\tinstall/operations\tunknown\tinstall/' "$rows" > "$tmp/unknown.tsv"
if MESH_MANIFEST_FIXTURE_ROWS="$tmp/unknown.tsv" mesh_manifest_tool_paths "$repo" > "$tmp/unknown.out" 2>"$tmp/unknown.err"; then
  echo 'manifest reader accepted an unknown classification' >&2
  exit 1
fi
[ ! -s "$tmp/unknown.out" ]
grep -q 'unknown kind' "$tmp/unknown.err"

cat > "$tmp/duplicate.tsv" <<'EOF'
# mesh-manifest v1
source_path	installed_basename	domain	kind	deploy_policy	cadence_policy	compatibility_owner
scripts/a/mesh-duplicate	mesh-duplicate	operations	tool	install	none	scripts:mesh-duplicate
job/mesh-duplicate	mesh-duplicate	operations	tool	install	none	job:mesh-duplicate
EOF
if MESH_MANIFEST_FIXTURE_ROWS="$tmp/duplicate.tsv" mesh_manifest_tool_paths "$repo" > "$tmp/duplicate.out" 2>"$tmp/duplicate.err"; then
  echo 'manifest reader accepted duplicate installed basenames' >&2
  exit 1
fi
[ ! -s "$tmp/duplicate.out" ]
grep -q 'duplicate installed basename' "$tmp/duplicate.err"

if MESH_MANIFEST_FIXTURE_ROWS="$rows" MESH_MANIFEST_FIXTURE_CHECK=1 mesh_manifest_rows "$repo" > "$tmp/check.out" 2>"$tmp/check.err"; then
  echo 'manifest reader ignored a failed --check' >&2
  exit 1
fi
[ ! -s "$tmp/check.out" ]

printf '# mesh-manifest v1\nsource_path\tinstalled_basename\tdomain\tkind\tdeploy_policy\tcadence_policy\tcompatibility_owner\n' > "$tmp/empty.tsv"
if MESH_MANIFEST_FIXTURE_ROWS="$tmp/empty.tsv" mesh_manifest_rows "$repo" > "$tmp/empty.out" 2>"$tmp/empty.err"; then
  echo 'manifest reader accepted an empty inventory' >&2
  exit 1
fi
[ ! -s "$tmp/empty.out" ]
grep -q 'no source rows' "$tmp/empty.err"

# Exercise the actual manifest's deployed comparison for same, different, and missing owners.
parity_repo="$tmp/parity-repo"
mkdir -p "$parity_repo/scripts/sub" "$parity_repo/job"
cp "$root/scripts/mesh-manifest" "$parity_repo/scripts/mesh-manifest"
chmod +x "$parity_repo/scripts/mesh-manifest"
printf '#!/bin/sh\necho shim\n' > "$parity_repo/scripts/mesh-compat"
printf '#!/bin/sh\necho nested\n' > "$parity_repo/scripts/sub/mesh-nested"
printf '#!/bin/sh\necho changed\n' > "$parity_repo/scripts/sub/mesh-different"
printf '[Unit]\n' > "$parity_repo/scripts/sub/mesh-worker.service"
chmod +x "$parity_repo/scripts/mesh-compat" "$parity_repo/scripts/sub/mesh-nested" "$parity_repo/scripts/sub/mesh-different"
cp "$parity_repo/scripts/sub/mesh-nested" "$tmp/bin/mesh-nested"
printf 'different\n' > "$tmp/bin/mesh-different"
MESH_REPO="$parity_repo" MESH_BIN="$tmp/bin" "$parity_repo/scripts/mesh-manifest" --parity > "$tmp/parity.tsv"
grep -q $'^scripts/sub/mesh-nested\tmesh-nested\t.*\tsame$' "$tmp/parity.tsv"
grep -q $'^scripts/sub/mesh-different\tmesh-different\t.*\tdifferent$' "$tmp/parity.tsv"
grep -q $'^scripts/mesh-compat\tmesh-compat\t.*\tmissing$' "$tmp/parity.tsv"
grep -q $'^scripts/sub/mesh-worker.service\t\t.*\tna$' "$tmp/parity.tsv"

sync_out="$tmp/sync.out"
doctor_out="$tmp/doctor.out"

# These consumers must exercise their manifest fixtures from outside the checkout.
(cd "$tmp" && MESH_REPO="$root" "$root/scripts/mesh-sync-tools" --test) >"$sync_out" 2>&1
grep -q 'manifest: checked tool/unit inventory' "$sync_out"

(cd "$tmp" && MESH_GENOME="$root" MESH_REPO="$root" "$root/scripts/mesh-doctor" --test) >"$doctor_out" 2>&1
grep -q 'manifest: checked tool/unit inventory' "$doctor_out"

echo 'mesh manifest consumers: both --test paths passed outside the repository'
