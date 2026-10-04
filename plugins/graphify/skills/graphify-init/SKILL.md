---
name: graphify-init
description: "Set up graphify offline code indexing on a repo from scratch — auto-installs prerequisites, indexes code into a local knowledge graph, and wires coding agents (Claude/Codex/OpenCode) to query it. Use when the user says 'set up graphify', 'graphify-init', 'initialize graphify', 'index this repo', or wants agents to query a code knowledge graph instead of grepping. Running this skill is also how a developer opts into their own local, always-fresh graph."
---

# graphify-init — Offline Code Indexing Setup

Set up [graphify](https://github.com/Graphify-Labs/graphify) on a code repo in
one command. This is a **thin orchestrator**: it sequences graphify's own native
commands in an opinionated order and adds team conventions. It does **not**
reimplement graphify's pipeline — graphify owns the mechanics, so this skill
survives graphify upgrades.

The mechanical phases are a deterministic script (`scripts/graphify-init.sh`) —
no per-run interpretation, testable, idempotent. This skill runs it, then does
the two steps that genuinely need judgment: smoke-testing a real query and
reporting what's committed vs local.

Running this skill is also the **onboarding step**: a developer runs it once to
opt into their own local knowledge graph, kept current as code evolves. The graph
is per-developer and git-ignored — teammates who never run it simply have no
graph, with no errors, no dirty `git status`, and nothing to notice.

Read `references/DESIGN.md` for the full rationale, decisions, and sources.

## Arguments

`$ARGUMENTS` — optional path to the repo root. Default: `.` (current directory).

## Golden rules

- **Never error out the session.** The script exits 0 on any missing prerequisite.
- Every step is **idempotent** — re-running the skill is always safe.

---

## Step 1 — Run the mechanical setup script

The script does phases 1–4, 6, 7 deterministically: auto-install uv + graphify
(exits 0 cleanly if impossible), merge team ignore entries line-by-line, index
the code offline (`extract --code-only` + cluster with a node-count viz
threshold), run the default `graphify {claude,codex,opencode} install` and
**de-pin** the machine-specific absolute `graphify` path in the committed agent
configs back to the bare command, install graphify's local git hooks, then make
one deterministic commit of all the wiring (including the `.gitattributes` that
`hook install` writes).

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/graphify-init/scripts/graphify-init.sh" $ARGUMENTS
```

Read the script's output. If it printed a "Skipping" line (prerequisite missing)
or "0 nodes" (no supported source), **stop here** and relay that to the user —
there is nothing to smoke-test. Otherwise continue to Step 2.

> Why a script: the mechanical work is pure shell, so scripting it removes
> per-run LLM drift, runs faster, and is testable. The script self-tests its one
> non-trivial bit — the absolute-path de-pin — via `graphify-init.sh --check`.

## Step 2 — Smoke-test retrieval (agent judgment)

Prove the graph is actually queryable, not just that files exist. Read
`graphify-out/GRAPH_REPORT.md`, pick one of its **Suggested Questions**, and run
it:

```bash
graphify god-nodes --top 5
graphify query "<a suggested question from GRAPH_REPORT.md>"
```

Confirm the query returns a non-empty, on-topic subgraph — an agent judging a
real answer, not just a non-empty check. Then paste the **God Nodes**,
**Surprising Connections**, and **Suggested Questions** sections from
`GRAPH_REPORT.md` into the chat (those three only — keep it concise).

## Step 3 — Report committed vs local

```bash
git status --short   # expect clean; graphify-out/ is ignored, not shown
```

Summarize:

- **Committed (shared with the team):** the `.gitignore` / `.graphifyignore`
  entries and the agent query-time config — CLAUDE.md / AGENTS.md sections plus
  `.claude/settings.json`, `.claude/CLAUDE.md`, `.claude/skills/`, `.codex/…`,
  `.opencode/…`, and `.gitattributes` — all bare `graphify` command, no
  absolute paths.
- **Local to this developer (git-ignored, never shared):** the entire
  `graphify-out/` graph (graph.json, cache, manifest, report, viz, sidecars)
  plus the git hooks + merge-driver registration (`.git/`). The graph is rebuilt
  from the committed wiring the moment any dev runs `/graphify-init`.
- **Push:** one clean commit — `git push` shares the wiring; teammates who run
  `/graphify-init` then build their own local graph from it.
- **Onboarding:** the graph is strictly opt-in and per-developer. A teammate who
  runs `/graphify-init` gets a local graph (kept fresh by their hooks); a teammate
  who does not has no graph — and no errors, no dirty tree, nothing to notice.

If `git status --short` shows anything unexpected, name it and why.

## Quality checklist

- [ ] Script ran; session never errored, even when a prerequisite was missing
- [ ] Ignore entries merged without duplicates, existing lines untouched
- [ ] `graphify-out/` fully git-ignored — graph never tracked, `git status` clean
- [ ] `graph.json` generated locally (code-only, offline); query works
- [ ] Agent wiring de-pinned to bare `graphify` (no absolute paths in committed config)
- [ ] Agent wiring attempted for all three; missing agents skipped silently
- [ ] `graphify hook install` ran; local hooks active
- [ ] `.gitattributes` from hook install committed with the wiring (one commit, deterministic)
- [ ] Smoke query returned a non-empty, on-topic result
- [ ] Ended with one clean commit ready to push; `git status` clean
