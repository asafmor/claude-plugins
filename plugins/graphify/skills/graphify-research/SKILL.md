---
name: graphify-research
description: "Multi-agent deep research into a codebase knowledge graph. Auto-activate when graphify-out/graph.json exists and the user asks an architectural question: 'how does X work', 'explain the architecture of Y', 'trace the flow of Z', 'what depends on W', 'where is X implemented', or any question about codebase structure, relationships, or design. Requires graphify-out/graph.json (run /graphify-init first if missing). Fans out 3–5 parallel cheap fast librarian agents, then synthesizes with targeted file reading for a grounded answer."
---

# graphify-research — Multi-Agent Codebase Research

Deep research workflow for architectural questions. A fleet of cheap fast `graphify-librarian` agents fans out across the graph in parallel; you consolidate, fill gaps, read key source files, and deliver a grounded answer.

Research question: `$ARGUMENTS`

## Preflight

```bash
graphify god-nodes --top 10 --json
```

If this errors ("graph not found" or similar): stop, tell the user to run `/graphify-init` first, exit.

If it succeeds: Read `graphify-out/GRAPH_REPORT.md`. Skim Suggested Questions and Community Structure — this gives the architectural shape and which clusters are relevant to `$ARGUMENTS`.

## Step 1 — Decompose into sub-angles

Break `$ARGUMENTS` into **3–5 distinct research angles**. Decide count based on question scope: 3 for narrow/focused questions, 5 for broad architectural questions. Each angle must:
- Address a different aspect (entry points, data flow, configuration, error paths, dependencies — pick what applies)
- Be phrased as a standalone question a librarian can investigate independently
- Cover different vocabulary (so synonym queries across librarians hit different graph regions)

Document the angles explicitly before spawning agents.

Example decomposition for "how does auth work":
- Angle 1: What are the authentication entry points and handler functions?
- Angle 2: How are tokens or sessions created, validated, and expired?
- Angle 3: What middleware or interceptors enforce auth checks?
- Angle 4: What configuration or environment variables control auth behavior?
- Angle 5: What error paths and failure modes exist in the auth flow?

## Step 2 — Spawn librarians in parallel

Spawn one `graphify-librarian` agent per angle, all **in parallel** (single Agent tool call with multiple sub-agents).

For each librarian:
- **model**: the cheapest and fastest model available on your platform (e.g. Haiku for Anthropic, Luna for OpenAI) — required, not optional. These are read-only graph queries; no deep reasoning needed.
- **agent**: `graphify-librarian`
- **prompt**: the angle as the topic, plus this instruction verbatim:

  > Follow the full graphify-librarian research protocol: BFS query, DFS query, 2–3 synonym variants, explain high-signal nodes, path queries between related node pairs, affected traversal on central nodes. Use --budget 4000 on every query. Return your LIBRARIAN_FINDINGS block.

Collect all LIBRARIAN_FINDINGS blocks before proceeding to Step 3.

## Step 3 — Synthesize and gap analysis

**Deduplicate across all findings:**
- Unified node list (same label = same node)
- Unified relationship list (deduplicate by from+to+edge_type)
- Flag nodes that appeared across 3+ librarians (high confidence)

**Identify gaps:**
- Topics in `gaps` across multiple librarians (systematic blind spots)
- Nodes in `high_degree_nodes_unexplained` not yet explained
- Node pairs in `suggested_paths` not yet explored
- Contradictions between librarians (same node, different relationships claimed)

**Run targeted follow-ups directly** (you, not the librarians):

```bash
# For each suggested path not yet explored:
graphify path "<node A>" "<node B>"

# For each high-degree unexplained node:
graphify explain "<node label>"

# For systematic gaps a context filter might resolve:
graphify query "<specific question>" --context <edge-type> --budget 4000
```

Stop when follow-ups produce diminishing returns (2 consecutive queries return nothing new).

## Step 4 — Ground truth from source files

The graph gives topology. Source files give truth.

For the **3–5 most critical files** identified (highest node appearances, most relationships, entry points or hubs): use the Read tool to read the relevant sections — the functions or blocks the graph pointed to, not the whole file.

Do not read exhaustively. The graph told you where to look; read those places.

## Step 5 — Consolidated answer

**Direct answer** — answer `$ARGUMENTS` in 2–4 sentences up front. No preamble.

**Architecture** — ASCII or Mermaid diagram of key nodes and relationships. Required if more than 2 nodes are involved. Annotate with file paths where known.

**Key files** — 3–5 files that matter most, one sentence each on why.

**Uncertainties** — what graph + files did not resolve. Be specific: name the nodes or relationships that remain unclear.

**Save to memory:**
```bash
graphify save-result \
  --question "$ARGUMENTS" \
  --answer "<2-sentence summary>" \
  --type query \
  --nodes <node1> <node2> <node3> \
  --outcome useful
```

Use the 3–5 most central nodes from your unified list.

## Quality bar

- Never answer from the graph alone — read at least one source file to ground the answer.
- If fewer than 2 librarians returned useful findings, caveat the answer explicitly.
- If the graph has no nodes relevant to the question, say so and suggest re-indexing with `/graphify-init`.
- The architecture diagram is required unless the question is trivially simple.
