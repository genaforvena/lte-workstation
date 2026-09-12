#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d -t mesh-manifest-install.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

repo="$tmp/repo"
bin="$tmp/home/.local/bin"
units="$tmp/home/.config/systemd/user"
mkdir -p "$repo/scripts/nested" "$repo/scripts/tests" "$repo/scripts/assets" "$repo/job" "$bin" "$units"
cp "$root/scripts/mesh-manifest" "$repo/scripts/mesh-manifest"
chmod +x "$repo/scripts/mesh-manifest"
printf '#!/usr/bin/env bash\necho direct\n' > "$repo/scripts/mesh-direct"
printf '#!/usr/bin/env bash\necho nested\n' > "$repo/scripts/nested/mesh-nested"
printf '#!/usr/bin/env bash\necho compatibility\n' > "$repo/scripts/mesh-compat"
printf '#!/usr/bin/env bash\necho canonical\n' > "$repo/scripts/nested/mesh-compat"
printf '#!/usr/bin/env bash\necho legacy\n' > "$repo/scripts/legacy-hook.sh"
printf '[Service]\nExecStart=%%h/.local/bin/mesh-direct\nExecStartPost=%%h/.local/bin/legacy-hook.sh\n' > "$repo/scripts/demo.service"
printf '#!/usr/bin/env bash\necho lane\n' > "$repo/job/mesh-lane-tool"
printf 'fixture\n' > "$repo/scripts/tests/sample.fixture"
printf 'asset\n' > "$repo/scripts/assets/readme.txt"
chmod +x "$repo/scripts/mesh-direct" "$repo/scripts/nested/mesh-nested" \
  "$repo/scripts/mesh-compat" "$repo/scripts/nested/mesh-compat" \
  "$repo/scripts/legacy-hook.sh" "$repo/job/mesh-lane-tool"

export MESH_REPO="$repo" MESH_BIN="$bin" MESH_SYSTEMD_DIR="$units"
"$repo/scripts/mesh-manifest" --check
"$root/scripts/mesh-manifest-install" tools
"$root/scripts/mesh-manifest-install" legacy-bin legacy-hook.sh
"$root/scripts/mesh-manifest-install" units demo.service

test -L "$bin/mesh-direct"
test -L "$bin/mesh-nested"
test -L "$bin/mesh-lane-tool"
test -L "$bin/mesh-compat"
test "$(readlink -f "$bin/mesh-compat")" = "$repo/scripts/mesh-compat"
test -f "$bin/legacy-hook.sh" && test ! -L "$bin/legacy-hook.sh"
test -f "$units/demo.service"
test ! -e "$bin/sample.fixture"
test ! -e "$bin/readme.txt"

MESH_BIN="$bin" "$repo/scripts/mesh-manifest" --parity > "$tmp/parity.tsv"
! rg -q $'\tmissing$|\tdifferent$' "$tmp/parity.tsv"
while IFS= read -r executable; do
  test -x "$bin/$executable"
done < <(sed -n 's|^ExecStart\(Post\)\?=%h/\.local/bin/||p' "$units/demo.service")

# Roll back only manifest-owned links and the explicitly selected copied entries.
"$root/scripts/mesh-manifest-install" rollback-tools
"$root/scripts/mesh-manifest-install" rollback-legacy-bin legacy-hook.sh
"$root/scripts/mesh-manifest-install" rollback-units demo.service
test ! -e "$bin/mesh-direct"
test ! -e "$bin/mesh-nested"
test ! -e "$bin/mesh-lane-tool"
test ! -e "$bin/legacy-hook.sh"
test ! -e "$units/demo.service"

echo 'mesh manifest installer: fixture deployment, parity, service resolution, and rollback pass'
