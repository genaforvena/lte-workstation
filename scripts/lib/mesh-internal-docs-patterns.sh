#!/usr/bin/env bash
# mesh-internal-docs-patterns.sh — THE ONE pattern table for internal docs.
#
# INTERNAL DOCS NEVER LAND IN GIT (2026-09-17). Node-local triage/health-warning
# write-ups, health-observation analyses, and pub note drafts are operator-private evidence,
# not repo material.
#
# Sourced by BOTH scripts/mesh-land (is_internal_evidence deny-list) and
# scripts/mesh-repo-hygiene (repo scan). One table, two readers — a pattern added
# here binds both guards, and a pattern removed here opens both. Never duplicate
# these patterns inline anywhere else.
#
# Each entry is a case-pattern matched against the repo-RELATIVE path
# ("${path#"$REPO"/}"), so absolute and relative callers agree.

# shellcheck disable=SC2034
INTERNAL_DOCS_PATTERNS="docs/health-warning-* health-warning-* */docs/health-warning-* */health-warning-* docs/health-observation-analysis-* health-observation-analysis-* */docs/health-observation-analysis-* */health-observation-analysis-* docs/pub-*-note-* pub-*-note-* */docs/pub-*-note-* */pub-*-note-* *.findings.json */*.findings.json"

# is_internal_evidence <path> — rc 0 iff the path is internal evidence.
# Accepts repo-absolute or repo-relative paths; strips a leading "$REPO/".
is_internal_evidence(){
  local _rel="${1#"$REPO"/}"
  case "$_rel" in
    docs/health-warning-*|health-warning-*|*/docs/health-warning-*|*/health-warning-*|docs/health-observation-analysis-*|health-observation-analysis-*|*/docs/health-observation-analysis-*|*/health-observation-analysis-*|docs/pub-*-note-*|pub-*-note-*|*/docs/pub-*-note-*|*/pub-*-note-*|*.findings.json|*/*.findings.json) return 0 ;;
    *) return 1 ;;
  esac
}
