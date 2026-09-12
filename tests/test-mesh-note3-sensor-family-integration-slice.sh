#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
names=(motion prox orient ambient)
tmp=$(mktemp -d -t mesh-note3-sensor-family.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

for name in "${names[@]}"; do
  shim="$repo/scripts/mesh-note3-$name"
  implementation="$repo/scripts/integrations/mesh-note3-$name"
  [ -x "$shim" ] || { echo "Note 3 $name: missing compatibility entrypoint" >&2; exit 1; }
  [ -x "$implementation" ] || { echo "Note 3 $name: implementation is not in integrations/" >&2; exit 1; }

  # Drive the real public shim from a scratch scripts/ tree and prove it reaches the sibling
  # integration implementation with the caller's arguments intact.
  stub_root="$tmp/$name"
  mkdir -p "$stub_root/scripts/integrations"
  cp "$shim" "$stub_root/scripts/mesh-note3-$name"
  cat > "$stub_root/scripts/integrations/mesh-note3-$name" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$MESH_NOTE3_SHIM_CAPTURE"
EOF
  chmod +x "$stub_root/scripts/mesh-note3-$name" "$stub_root/scripts/integrations/mesh-note3-$name"
  MESH_NOTE3_SHIM_CAPTURE="$stub_root/args" "$stub_root/scripts/mesh-note3-$name" --dispatch-probe first second
  printf '%s\n' --dispatch-probe first second > "$stub_root/expected"
  cmp -s "$stub_root/expected" "$stub_root/args" || {
    echo "Note 3 $name: compatibility shim did not dispatch and preserve arguments" >&2
    exit 1
  }

  # A deployed copy lives in ~/.local/bin, so prove its repository fallback resolves too.
  fallback_root="$tmp/$name/fallback-repo/scripts/integrations"
  installed_bin="$tmp/$name/installed-bin"
  mkdir -p "$fallback_root" "$installed_bin"
  cp "$shim" "$installed_bin/mesh-note3-$name"
  cat > "$fallback_root/mesh-note3-$name" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$MESH_NOTE3_SHIM_CAPTURE"
EOF
  chmod +x "$installed_bin/mesh-note3-$name" "$fallback_root/mesh-note3-$name"
  MESH_REPO="$stub_root/fallback-repo" MESH_NOTE3_SHIM_CAPTURE="$stub_root/fallback-args" \
    "$installed_bin/mesh-note3-$name" --deployed-probe third fourth
  printf '%s\n' --deployed-probe third fourth > "$stub_root/fallback-expected"
  cmp -s "$stub_root/fallback-expected" "$stub_root/fallback-args" || {
    echo "Note 3 $name: installed compatibility shim did not resolve MESH_REPO fallback" >&2
    exit 1
  }
done

(cd "$repo" && "$repo/scripts/mesh-manifest" --list) > "$tmp/manifest.tsv"
python3 - "$tmp/manifest.tsv" "$repo/scripts" <<'PY'
import csv
import pathlib
import sys

with open(sys.argv[1], newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader((line for line in stream if not line.startswith("#")), delimiter="\t"))
by_path = {row["source_path"]: row for row in rows}
scripts = pathlib.Path(sys.argv[2])
for name in ("motion", "prox", "orient", "ambient"):
    tool = f"mesh-note3-{name}"
    impl = by_path[f"scripts/integrations/{tool}"]
    shim = by_path[f"scripts/{tool}"]
    assert (impl["domain"], impl["kind"], impl["deploy_policy"]) == ("integrations", "tool", "none"), impl
    assert shim["domain"] == "integrations" and shim["kind"] == "tool", shim
    assert shim["installed_basename"] == tool and shim["deploy_policy"] == "install", shim
    assert shim["cadence_policy"] == "header" and shim["compatibility_owner"] == f"scripts:{tool}", shim
    assert "reflex-cadence:" in (scripts / tool).read_text(encoding="utf-8"), tool
PY

run_read_gate() {
  local name=$1 expected=$2 shim="$repo/scripts/mesh-note3-$1" output rc
  set +e
  output=$("$shim" --test 2>&1)
  rc=$?
  set -e
  if [ "$rc" -eq 0 ] && printf '%s\n' "$output" | grep -Fq "$expected"; then
    return 0
  fi
  if [ "$rc" -eq 2 ] && printf '%s\n' "$output" | grep -Fq 'smoke-test: n/a'; then
    printf 'Note 3 %s: honest unavailable result: %s\n' "$name" "$output"
    return 0
  fi
  printf 'Note 3 %s: real-read gate failed (rc=%s): %s\n' "$name" "$rc" "$output" >&2
  return 1
}

# Each adapter's --test includes a current hardware read; do not replace these with classifier-only
# checks. Run serially because all four share the same ADB device and sensor service.
run_read_gate motion 'LIVE adb read '
run_read_gate prox 'LIVE adb read raw='
run_read_gate orient 'LIVE adb read '
run_read_gate ambient 'LIVE Note3 env:'

echo 'Note 3 sensor family: manifest, compatibility paths, cadence owners, and serial real-read gates pass'
