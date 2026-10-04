# graphify

Turns [graphify](https://github.com/Graphify-Labs/graphify) offline code indexing
into a two-skill workflow for coding agents:

- **`/graphify-init`** — run once per repo to index code into a queryable knowledge
  graph and wire your agents to query it. Each developer opts into their own local
  graph that stays current as code evolves.
- **`/graphify-research`** — run daily to answer architectural questions. Fans out
  3–5 parallel cheap fast `graphify-librarian` subagents across different angles
  of your question, synthesizes their findings, reads key source files for ground
  truth, and delivers a grounded answer. Never miss a relationship that a
  single-query approach would skip.

Both skills are **thin orchestrators**: they sequence graphify's own native
commands and add team conventions. They do not reimplement graphify's pipeline,
so they survive graphify upgrades.

## Prerequisites

None to invoke — the skill auto-installs what it needs:

- **uv** (installed automatically if missing; falls back to Homebrew on macOS)
- **graphify** (`uv tool install graphifyy`, installed automatically if missing)

If neither can be installed, the skill prints one line and exits cleanly — it
never errors your session.

## Usage

### `/graphify-init` — one-time setup

```
/graphify-init            # set up graphify on the current repo
/graphify-init <path>     # set up on a specific repo path
```

### `/graphify-research` — daily research

```
/graphify-research how does the auth flow work?
/graphify-research what depends on the billing module?
/graphify-research trace the request lifecycle from HTTP handler to DB
```

Requires `graphify-out/graph.json` to exist — run `/graphify-init` first.

## What graphify-init does

1. **Auto-installs** uv + graphify (for you, the runner).
2. **Merges ignore entries** into `.gitignore` / `.graphifyignore` (line-by-line,
   no duplicates).
3. **Indexes the code** offline: `graphify extract . --code-only` then clusters
   (skips heavy HTML viz above ~5000 nodes).
4. **Wires your agents** to query the graph: `graphify {claude,codex,opencode}
   install` (missing agents are skipped silently).
5. **Installs local lifecycle hooks**: `graphify hook install` (auto-rebuild on
   commit/checkout), and offers a `git gpull` alias.
6. **Smoke-tests retrieval** with `graphify god-nodes` and one `graphify query`.
7. **Reports** what's committed vs local, with an onboarding note for teammates.

## What graphify-research does

1. **Preflight** — checks `graphify-out/graph.json` exists; reads `GRAPH_REPORT.md`
   for architectural shape.
2. **Decomposes** your question into 3–5 distinct sub-angles (entry points, data
   flow, configuration, error paths, dependencies).
3. **Fans out** one `graphify-librarian` subagent per angle in parallel, each
   running a 7-step graph protocol: BFS query, DFS query, synonym variants,
   `explain` on high-signal nodes, `path` between related node pairs, `affected`
   traversal on central nodes, context-filtered follow-up. Librarians use the
   cheapest fast model available — they do only graph queries, no file reading.
4. **Synthesizes** all findings: deduplicates nodes and relationships, identifies
   gaps, runs targeted follow-up queries (`path`, `explain`) directly.
5. **Reads key source files** (3–5 most critical) to ground the graph topology in
   actual code.
6. **Delivers** a direct answer, architecture diagram, key file list, and
   uncertainties — then saves the result to graphify memory.

## Committed vs local

- **Committed (shared with the team) — wiring only:** the `.gitignore` /
  `.graphifyignore` entries and the agent query-time config (CLAUDE.md /
  AGENTS.md sections plus `.claude/`, `.codex/`, `.opencode/` files), all using
  the bare `graphify` command — no machine-specific absolute paths.
- **Local to each developer (git-ignored, never shared):** the entire
  `graphify-out/` graph and the git hooks. The graph is rebuilt from the
  committed wiring the moment a dev runs `/graphify-init`.

The graph is **per-developer and opt-in**. A teammate who runs `/graphify-init`
gets a local graph kept fresh by their hooks; a teammate who does not has no
graph — no errors, no dirty `git status`, nothing to notice.

## Design & rationale

The full decision record, technical flow, concurrency analysis, and sources are
in [`skills/graphify-init/references/DESIGN.md`](skills/graphify-init/references/DESIGN.md).
