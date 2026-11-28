#!/usr/bin/env bash
# check-context-layout.sh — assert a .context/ directory matches the layout
# spec in .context/META.md section 2.
#
# The spec is identical for every repo, so this is the one implementation of
# it: scripts/validate.py calls this rather than reimplementing the rules, and
# `context-review` runs it as its structural conformance step. Plain sh — no
# python, node or toolchain assumption, so it runs in a consumer repo of any
# language.
#
# Usage:
#   ./scripts/check-context-layout.sh [path-to-.context]   # default .context
#
# Output: one `ERROR: ` or `WARN: ` line per finding.
# Exit:   1 if any ERROR, else 0. Warnings never fail on their own — a caller
#         that wants them fatal (CI) treats any output as failure.

ctx="${1:-.context}"
errors=0

err() { echo "ERROR: $*"; errors=$((errors + 1)); }
warn() { echo "WARN: $*"; }

if [ ! -d "$ctx" ]; then
  err "$ctx does not exist — this is not a structured repo"
  exit 1
fi

# --- Fixed names. overview.md is one name because tooling looks for it; a repo
# --- that calls it project-overview.md reads as uninitialized.
[ -f "$ctx/overview.md" ] || err "missing required file: overview.md"
[ -f "$ctx/project-overview.md" ] &&
  err "project-overview.md is drift — rename to overview.md"

# --- Always present: the spec itself, and the PR format every repo needs.
[ -f "$ctx/META.md" ] || err "missing required file: META.md"
[ -f "$ctx/workflows/pull-requests.md" ] ||
  err "missing required file: workflows/pull-requests.md"

# --- Always folders. An ADR is immutable and cited by number; a retrospective
# --- is one dated entry per task. Collapsing either into a single file
# --- destroys that, so the file form is an error, not a style choice.
for base in decisions retrospectives; do
  [ -f "$ctx/$base.md" ] &&
    err "$base.md is drift — $base must be a folder, one entry per file"
  [ -d "$ctx/$base" ] || err "missing required folder: $base/"
done

# --- Promotable entries: flat file, or a folder once promoted past 300 lines.
# --- Exactly one shape, and a promoted folder needs the entry point agents
# --- read now that the flat file is gone.
for base in standards testing architecture; do
  flat="$ctx/$base.md"
  dir="$ctx/$base"
  if [ -f "$flat" ] && [ -d "$dir" ]; then
    err "$base exists as both $base.md and $base/ — pick one shape"
  elif [ -d "$dir" ]; then
    [ -f "$dir/README.md" ] ||
      err "$base/ has no README.md — a promoted entry needs an entry point, since agents no longer find $base.md"
  elif [ -f "$flat" ]; then
    n=$(wc -l < "$flat" | tr -d ' ')
    [ "$n" -gt 300 ] &&
      warn "$base.md is $n lines (over 300) — promote it to $base/ via context-maintenance"
  else
    warn "missing $base.md"
  fi
done

# --- Retrospectives cap. Archived entries live in retrospectives/archive/ and
# --- are deliberately not counted: that is the stated remedy for going over.
if [ -d "$ctx/retrospectives" ]; then
  n=$(find "$ctx/retrospectives" -maxdepth 1 -name '*.md' \
        ! -name 'README.md' ! -name 'template.md' | wc -l | tr -d ' ')
  [ "$n" -gt 10 ] &&
    err "retrospectives/ has $n entries, max 10 — promote the lessons and git mv them to retrospectives/archive/"
fi

exit $([ "$errors" -gt 0 ] && echo 1 || echo 0)
