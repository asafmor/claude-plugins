#!/usr/bin/env bash
# graphify-init — deterministic setup for graphify offline code indexing.
#
# Runs the mechanical phases (install, ignore merge, index, agent wiring + abs-path
# de-pin, commit, hooks). The agent handles the smoke-test query and the final
# committed-vs-local report — see SKILL.md.
#
# Thin orchestrator: calls graphify's native commands; never reimplements them.
# Never errors the session — if a prerequisite can't be installed it prints one
# line and exits 0. Every phase is idempotent; re-running is always safe.
#
# Usage:  graphify-init.sh [REPO_PATH]     (default: current directory)
#         graphify-init.sh --check         (self-test the de-pin logic, no side effects)

set -uo pipefail

# ---- de-pin helper: rewrite absolute ".../graphify" -> bare "graphify" --------
# Kept as a function so --check can test it in isolation. Matches an absolute path
# ending in /graphify on a quote-or-whitespace boundary; leaves already-bare refs
# and non-graphify paths untouched.
depin_file() {  # depin_file <path>
  [ -f "$1" ] || return 0
  perl -i -pe 's{(["\s])(/[^"\s]*/)?graphify(?=["\s])}{$1graphify}g' "$1"
}

# ---- --check: self-test, no repo side effects --------------------------------
if [ "${1:-}" = "--check" ]; then
  tmp=$(mktemp)
  printf '{"a":"/Users/x/.local/bin/graphify hook-guard read","b":"/opt/uv/tools/graphifyy/bin/graphify search","c":"graphify bare","d":"/usr/bin/notgraphify keep"}' > "$tmp"
  depin_file "$tmp"
  got=$(cat "$tmp"); rm -f "$tmp"
  want='{"a":"graphify hook-guard read","b":"graphify search","c":"graphify bare","d":"/usr/bin/notgraphify keep"}'
  # idempotency: second pass must be a no-op
  tmp2=$(mktemp); printf '%s' "$got" > "$tmp2"; depin_file "$tmp2"; got2=$(cat "$tmp2"); rm -f "$tmp2"
  if [ "$got" = "$want" ] && [ "$got2" = "$got" ]; then
    echo "de-pin self-test: PASS"; exit 0
  else
    echo "de-pin self-test: FAIL"; echo " got:  $got"; echo " want: $want"; exit 1
  fi
fi

REPO="${1:-.}"
cd "$REPO" || { echo "graphify-init: cannot cd to '$REPO'. Skipping."; exit 0; }

# ---- Phase 1 — preflight & auto-install (silent opt-out) ---------------------
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv…"
  curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null \
    || brew install uv 2>/dev/null \
    || { echo "graphify-init: could not install uv (https://docs.astral.sh/uv/). Re-run later. Skipping."; exit 0; }
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v graphify >/dev/null 2>&1; then
  echo "Installing graphify…"
  uv tool install graphifyy 2>&1 | tail -2
  uv tool update-shell 2>/dev/null || true
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v graphify >/dev/null 2>&1; then
  echo "graphify-init: graphify not on PATH after install. Open a new terminal (or run 'uv tool update-shell') and re-run. Skipping."
  exit 0
fi
graphify --version

# ---- Phase 2 — ignore files (entry-by-entry merge, never dupe/clobber) -------
add_line() {  # add_line <file> <exact-line>
  local file="$1" line="$2"
  [ -f "$file" ] || : > "$file"
  if ! grep -qxF "$line" "$file" 2>/dev/null; then
    [ -s "$file" ] && [ -n "$(tail -c1 "$file")" ] && printf '\n' >> "$file"
    printf '%s\n' "$line" >> "$file"
  fi
}

for l in "graphify-out/" "*.graphify-bak"; do
  add_line .gitignore "$l"
done
for l in ".claude" ".codex" ".opencode" "CLAUDE.md" "AGENTS.md"; do
  add_line .graphifyignore "$l"
done

# ---- Phase 3 — first index (code-only, offline) ------------------------------
graphify extract . --code-only --no-cluster

node_count=$(python3 -c "import json; g=json.load(open('graphify-out/graph.json')); print(len(g.get('nodes', g.get('elements', []))))" 2>/dev/null || echo 0)
if [ "$node_count" -eq 0 ]; then
  echo "graphify-init: extraction produced 0 nodes — no supported source files? Stopping before wiring."
  exit 0
fi

if [ "$node_count" -lt 5000 ]; then
  graphify cluster-only . --no-label
else
  graphify cluster-only . --no-label --no-viz
fi

# ---- Phase 4 — agent wiring (default install) + de-pin abs path --------------
graphify claude install   2>/dev/null || echo "  (claude wiring skipped)"
graphify codex install    2>/dev/null || echo "  (codex wiring skipped)"
graphify opencode install 2>/dev/null || echo "  (opencode wiring skipped)"

# The default install pins this machine's absolute graphify path into the shared,
# committed configs. Rewrite it back to the bare command so it's portable.
for f in .claude/settings.json .codex/hooks.json; do
  depin_file "$f"
done

if grep -rIl '/graphify' .claude .codex 2>/dev/null | grep -q .; then
  echo "graphify-init: WARNING — absolute /graphify path still present in agent config after de-pin:"
  grep -rIn '/graphify' .claude .codex 2>/dev/null
fi

# ---- Phase 6 — lifecycle hooks (local) ---------------------------------------
# Install hooks BEFORE the commit. hook install writes local hooks into
# .git/hooks (never committed) AND a committed .gitattributes
# (graphify-out/graph.json merge=graphify). Doing it before the commit means the
# .gitattributes is staged and committed deterministically in the single wiring
# commit below — nothing left dangling for a human or agent to clean up.
graphify hook install

# ---- Phase 7 — commit the wiring (one deterministic commit) ------------------
# graphify-out/ is git-ignored, so the graph is never committed. We commit only
# the shareable wiring: ignore rules, agent query-time config (bare command,
# de-pinned), and the .gitattributes from hook install. The post-commit hook now
# exists and will fire once on this commit — a harmless background rebuild of the
# git-ignored graph, leaving git status clean.
for p in .gitignore .graphifyignore .gitattributes CLAUDE.md AGENTS.md \
         .claude/settings.json .claude/CLAUDE.md .claude/skills \
         .codex .opencode; do
  [ -e "$p" ] && git add "$p"
done

if ! git diff --cached --quiet; then
  git commit -m "chore: wire up graphify (agent query-time config, ignores, merge attribute)"
  echo "Committed graphify wiring — ready to push."
else
  echo "Nothing new to commit — graphify already wired."
fi

cat <<'EOF'

Recommended: keep your local graph in sync after pulls with a git alias —
  git config --global alias.gpull '!git pull && graphify update .'
Then use `git gpull` instead of `git pull`. Otherwise run `graphify update .`
manually after each pull/merge.

--- graphify-init: mechanical phases done. ---
Next (agent): read graphify-out/GRAPH_REPORT.md, run one `graphify query` from a
Suggested Question to smoke-test retrieval, then report committed-vs-local.
EOF
