#!/usr/bin/env bash
set -euo pipefail

root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
tool="$root/scripts/mesh-opbox"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

"$tool" --test
cat >"$td/a.txt" <<'EOF'
2026-09-08T00:00:01Z alpha
2026-09-08T00:00:03Z shared
EOF
cat >"$td/b.txt" <<'EOF'
2026-09-08T00:00:02Z beta
2026-09-08T00:00:03Z shared
EOF

"$tool" export "$td/a.txt" "$td/a.ops"
"$tool" export "$td/b.txt" "$td/b.ops"
"$tool" merge "$td/ab.ops" "$td/a.ops" "$td/b.ops"
"$tool" materialize "$td/ab.ops" "$td/merged.txt"
diff -u <(printf '%s\n' \
  '2026-09-08T00:00:01Z alpha' \
  '2026-09-08T00:00:02Z beta' \
  '2026-09-08T00:00:03Z shared') "$td/merged.txt"

# The convenience path is the same union and remains safe to repeat.
"$tool" sync "$td/repeated.txt" "$td/b.txt" "$td/a.txt"
diff -u "$td/merged.txt" "$td/repeated.txt"
before="$(sha256sum "$td/ab.ops")"
"$tool" merge "$td/ab.ops" "$td/b.ops" "$td/a.ops" "$td/ab.ops"
after="$(sha256sum "$td/ab.ops")"
[[ "$before" == "$after" ]]

echo 'test-mesh-opbox: ok (append-only text ops, union merge, deterministic materialization)'
