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

# --- The spec itself, at every node.
[ -f "$ctx/META.md" ] || err "missing required file: META.md"

# --- Context shape decides which rule set applies below. It is declared in
# --- overview.md rather than inferred from which files are present, because
# --- inferring it would mean deriving the rule from the thing the rule exists
# --- to check — a node missing standards.md would read as "aggregate" and
# --- stop being asked for it. Absent means project: that is what every
# --- standalone repo is, so only non-project nodes carry a key.
shape=project
if [ -f "$ctx/overview.md" ]; then
  declared=$(sed -n 's/^context_shape:[[:space:]]*\([A-Za-z]*\).*/\1/p' \
               "$ctx/overview.md" | head -1)
  [ -n "$declared" ] && shape="$declared"
fi
case "$shape" in
  project|aggregate) ;;
  *)
    # Not a silent fall back to the default: a typo must not quietly buy the
    # wrong rule set, which would make every check below meaningless.
    err "unrecognized context_shape '$shape' in overview.md — expected project or aggregate"
    exit 1
    ;;
esac

# --- workflows/ follows the git repository boundary, not the context shape.
# --- PR format, branching strategy and CI are properties of a repository: a
# --- grouping directory inside a monorepo has none of its own, and a workspace
# --- root is a folder of repositories rather than a repository. So the folder
# --- and its required pull-requests.md are both asked for exactly where a .git
# --- begins — which is also what stops a package in a monorepo from being
# --- told to restate the root's PR format.
# ---
# --- Tested with -e, not -d, because a worktree and a submodule both use a
# --- .git file rather than a directory.
if [ -e "$(dirname "$ctx")/.git" ]; then
  [ -d "$ctx/workflows" ] || err "missing required folder: workflows/"
  [ -f "$ctx/workflows/pull-requests.md" ] ||
    err "missing required file: workflows/pull-requests.md"
fi

# --- decisions/ is a folder at both shapes. A cross-project decision is an ADR
# --- with a wider blast radius, not a different kind of artifact: still
# --- immutable once accepted, still cited by number, so still one file each.
[ -f "$ctx/decisions.md" ] &&
  err "decisions.md is drift — decisions must be a folder, one ADR per file"
[ -d "$ctx/decisions" ] || err "missing required folder: decisions/"

# --- retrospectives/ and tasks/ are project-only: both belong to the node the
# --- work actually happened in, not to one describing what its children share.
if [ "$shape" = project ]; then
  [ -f "$ctx/retrospectives.md" ] &&
    err "retrospectives.md is drift — retrospectives must be a folder, one dated entry per file"
  [ -d "$ctx/retrospectives" ] || err "missing required folder: retrospectives/"

  # Archived entries live in retrospectives/archive/ and are deliberately not
  # counted: that is the stated remedy for going over.
  if [ -d "$ctx/retrospectives" ]; then
    n=$(find "$ctx/retrospectives" -maxdepth 1 -name '*.md' \
          ! -name 'README.md' ! -name 'template.md' | wc -l | tr -d ' ')
    [ "$n" -gt 10 ] &&
      err "retrospectives/ has $n entries, max 10 — promote the lessons and git mv them to retrospectives/archive/"
  fi
else
  for base in retrospectives tasks; do
    if [ -e "$ctx/$base" ] || [ -e "$ctx/$base.md" ]; then
      warn "$base at an aggregate node — it belongs to the project the work happened in"
    fi
  done
fi

# --- Promotable entries: flat file, or a folder once promoted past 300 lines.
# --- Exactly one shape, and a promoted folder needs the entry point agents
# --- read now that the flat file is gone.
# ---
# --- architecture applies at both shapes; standards and testing are
# --- project-only, because code style and test setup belong to the node that
# --- has the code. An aggregate node that grows them is describing its
# --- children instead of what they share.
if [ "$shape" = project ]; then
  promotable="standards testing architecture"
else
  promotable="architecture"
fi

for base in $promotable; do
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

if [ "$shape" = aggregate ]; then
  for base in standards testing; do
    if [ -e "$ctx/$base" ] || [ -e "$ctx/$base.md" ]; then
      warn "$base at an aggregate node — code style and test setup belong to the project with the code"
    fi
  done
fi

exit $([ "$errors" -gt 0 ] && echo 1 || echo 0)
