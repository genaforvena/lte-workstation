# Shared, fail-closed reader for scripts/mesh-manifest's typed TSV inventory.
# Source this file; mesh_manifest_rows <repo> emits rows only after validating the whole inventory.

mesh_manifest_rows(){ # <repo> → validated TSV rows without the two header lines
  local repo="$1" manifest listing
  repo="$(cd -- "$repo" 2>/dev/null && pwd -P)" || {
    echo "mesh-manifest-reader: missing repository: $1" >&2
    return 1
  }
  manifest="$repo/scripts/mesh-manifest"
  [ -x "$manifest" ] || {
    echo "mesh-manifest-reader: required checked manifest is not executable: $manifest" >&2
    return 1
  }
  if ! MESH_REPO="$repo" "$manifest" --check >/dev/null; then
    echo "mesh-manifest-reader: manifest check failed: $manifest" >&2
    return 1
  fi
  if ! listing="$(MESH_REPO="$repo" "$manifest" --list)"; then
    echo "mesh-manifest-reader: manifest list failed: $manifest" >&2
    return 1
  fi

  printf '%s\n' "$listing" | awk -F '\t' \
    -v header=$'source_path\tinstalled_basename\tdomain\tkind\tdeploy_policy\tcadence_policy\tcompatibility_owner' '
    function reject(message) {
      if (!bad) print "mesh-manifest-reader: invalid manifest row: " message > "/dev/stderr"
      bad = 1
    }
    NR == 1 {
      if ($0 != "# mesh-manifest v1") reject("missing v1 marker")
      next
    }
    NR == 2 {
      if ($0 != header) reject("unexpected column header")
      next
    }
    {
      if (NF != 7) { reject("expected 7 tab-separated fields at row " NR); next }
      path=$1; basename=$2; domain=$3; kind=$4; policy=$5; cadence=$6; owner=$7
      if (path !~ /^(scripts|job)\// || path ~ /\/\// || path ~ /\/$/ || path ~ /(^|\/)\.\.?($|\/)/)
        reject("source path outside scripts/ and job/: " path)
      if (domain !~ /^(core|communication|integrations|operations|tests|ux)$/)
        reject("unknown domain for " path ": " domain)
      if (kind !~ /^(tool|unit|asset|fixture|library)$/)
        reject("unknown kind for " path ": " kind)
      if (policy !~ /^(install|systemd|none)$/)
        reject("unknown deploy policy for " path ": " policy)
      if (cadence !~ /^(header|unit|none)$/ || owner == "")
        reject("invalid cadence/owner for " path)
      if (policy == "install") {
        n=split(path, parts, "/"); source_name=parts[n]
        if (kind != "tool" || basename == "" || basename != source_name || cadence == "unit")
          reject("invalid installable tool ownership for " path)
        if (basename in installed)
          reject("duplicate installed basename " basename ": " installed[basename] " and " path)
        installed[basename]=path
      } else if (policy == "systemd") {
        n=split(path, parts, "/"); source_name=parts[n]
        if (kind != "unit" || basename != "" || source_name !~ /\.(service|timer)$/ || cadence != "unit")
          reject("invalid systemd unit row for " path)
      } else if (basename != "") {
        reject("non-install row has installed basename: " path)
      }
      rows[++count]=$0
    }
    END {
      if (NR < 2) reject("empty inventory")
      if (count == 0) reject("inventory has no source rows")
      if (bad) exit 1
      for (i=1; i<=count; i++) print rows[i]
    }'
}

mesh_manifest_tool_paths(){ # <repo> → source paths of installable tools
  mesh_manifest_rows "$1" | awk -F '\t' '$4 == "tool" && $5 == "install" { print $1 }'
}

mesh_manifest_unit_paths(){ # <repo> → source paths of systemd units
  mesh_manifest_rows "$1" | awk -F '\t' '$4 == "unit" && $5 == "systemd" { print $1 }'
}

mesh_manifest_orphan_paths(){ # <repo> → legacy direct files plus every installable tool and unit
  mesh_manifest_rows "$1" | awk -F '\t' '
    {
      depth=split($1, parts, "/")
      if (depth == 2 || $5 == "install" || $5 == "systemd") print $1
    }'
}

mesh_manifest_lint_paths(){ # <repo> → source tools, shell entrypoints, and matching non-executable rows
  mesh_manifest_rows "$1" | awk -F '\t' '
    {
      n=split($1, parts, "/"); name=parts[n]
      if (name ~ /^mesh-/ || name ~ /\.sh$/) print $1
    }'
}
