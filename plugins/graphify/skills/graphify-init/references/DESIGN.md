# The story behind graphify-init

This is the "why" file. If you want the "what" and "how," read
[`SKILL.md`](../SKILL.md) and the script it runs,
[`scripts/graphify-init.sh`](scripts/graphify-init.sh) — they are the source of
truth for every command. What follows is the reasoning that shaped them, so the
next person to touch this skill knows which walls we already walked into.

## What we set out to build

A team has a repo. They want their coding agents — Claude Code, Codex, OpenCode —
to answer "where is this called?" and "how does auth flow through here?" by
walking a knowledge graph of the code instead of grepping and guessing.
[graphify](https://github.com/Graphify-Labs/graphify) already builds that graph:
a local, AST-derived map of the codebase with god nodes, communities, and
`query` / `path` / `explain` tools on top.

So the skill isn't a graph engine. It's the thing that sets graphify up *well* —
one command, sane defaults, wired into whichever agents you actually use — and
does it the same way across the dozens of repos a team owns. Run it once and you
have opted in: your own graph, kept fresh as you work. Never run it, and nothing
breaks; you just don't have a graph. That "gradual, no-pressure opt-in" is the
whole posture, and most of the decisions below fall out of taking it seriously.

## Ride graphify, don't rebuild it

The first temptation was to own the pipeline — call the parsers ourselves, do
our own clustering, write our own hooks. We didn't, and the reason is simple:
graphify already ships all of it, and it *warns you* when a bundled skill drifts
from its package version. Anything we hand-rolled would rot on the next upgrade
and we'd be chasing their internals forever.

So the skill is a thin orchestrator. It calls graphify's own commands in an
opinionated order and adds only the things graphify's generic installer has no
opinion about: which files to keep out of the graph, an offline-by-default index,
wiring for three agents instead of one, and the onboarding framing. graphify owns
the mechanics; we own the taste. When graphify changes how it parses or clusters,
we get that for free.

## Offline, deterministic, and quiet about it

The index is code-only by default: `graphify extract --code-only`, pure AST, no
LLM, no API key, nothing leaving the machine. That's the data-residency-safe
choice, but it earns a second, quieter payoff — determinism. The same commit
always produces the same graph. That one fact makes the next decision possible.

## The graph is yours, not the repo's

The longest argument was about where the graph lives. The obvious idea is to
commit `graph.json` so the whole team shares one graph. We tried it and it fought
back. graphify's post-commit hook rebuilds the graph in the background and leaves
it unstaged, so a committed `graph.json` shows up as *modified* after nearly
every commit — it always trails HEAD by one. Your `git status` is never clean.
Fixing that with a blocking pre-commit restage was too slow, and concurrent
branches could still collide on the same file.

So we stopped sharing it. The entire `graphify-out/` tree is git-ignored. Each
developer builds and keeps their own graph locally. `git status` stays clean, two
people can never conflict on the graph, and there's nothing tracked to merge. The
cost is honest: git doesn't hand you a graph, you build one by running the skill.
And because the index is deterministic, the graph you build from a given commit
is the same one your teammate builds from it. Opt-in, but not fragmented.

One loose end here: `graphify hook install` writes a `.gitattributes` line —
`graphify-out/graph.json merge=graphify`, registering a union merge driver. Since
`graphify-out/` is git-ignored, that driver never fires and the line does nothing.
We commit it anyway, deterministically, in the same wiring commit. `.gitattributes`
is shared team config used for far more than graphify, so we don't want to strip
or ignore it, and leaving it untracked would either dirty `git status` or invite
whoever ran the skill to improvise an extra commit. Committing it is the boring,
predictable choice — an inert entry that lives with the rest of the wiring.

Your graph shows up the moment you run `/graphify-init`, then stays fresh on its
own: the post-commit and post-checkout hooks rebuild it as you work, and
`graphify update .` catches it up after a pull.

## The filesystem-leak trap

Wiring the agents is where we got bitten. Running `graphify claude install` (and
the codex/opencode equivalents) writes the graph-query hooks into
`.claude/settings.json`, `.codex/hooks.json`, and friends. Those files are shared,
committed team config — people use them for far more than graphify — so they
have to be committable.

The problem: the default install pins the *absolute path of your graphify binary*
into them, something like `/Users/you/.local/bin/graphify`. Commit that and
you've leaked your home directory into the repo and broken the config on every
other machine.

graphify has a `--project` flag that emits the bare `graphify` command instead,
and we used it for a while. But we ended up preferring the plain default install
plus a small, deterministic cleanup: after installing, a one-line `perl` rewrite
turns any absolute `…/graphify` path back into the bare command — PATH-resolved
per machine, like `git` or `node`. Already-bare references and unrelated paths are
left alone, and running it twice changes nothing. It's the graphify-native install
path with the leak sanded off, and the script self-tests that rewrite with
`graphify-init.sh --check`.

## Everyone opts in for themselves

The hooks that keep your graph fresh live in `.git/hooks`, and git deliberately
never commits those. We could have forced them on every clone with a committed
`.githooks/` directory and `core.hooksPath` — the husky trick — but that's exactly
the kind of magic this skill is meant to avoid. Running the
skill installs your own hooks. Not running it installs nothing. No bootstrap, no
surprises, and the auto-install of `uv` and `graphify` only ever happens for the
person actually running the setup — cloning the repo installs nothing on anyone.

## What this means when the team is mixed

Because the graph is per-developer and the wiring is idempotent, a repo with some
onboarded devs and some not just works:

| Thing | Shared how | Can it conflict? |
|---|---|---|
| CLAUDE.md / AGENTS.md query sections | committed | No — idempotent marker writes; re-running is a no-op |
| `.gitignore` / `.graphifyignore` entries | committed | No — added line by line, only if missing |
| agent config (`.claude/settings.json`, `.codex/hooks.json`, …) | committed | No — bare command after de-pin; idempotent writes |
| `.gitattributes` merge attribute | committed | No — inert (graph is git-ignored, driver never fires); committed once with the wiring |
| git hooks + merge-driver registration | local `.git/` | No — per developer |
| the whole `graphify-out/` graph | git-ignored | No — never tracked, so no dirty tree and nothing to merge |

A teammate who never ran the skill commits and pushes normally, sees a clean
`git status`, and simply has no local graph. No errors, nothing to notice. If they
ever want in, they run `/graphify-init` once.

## Where it ships

The skill ships as part of the `graphify` plugin in this marketplace: registered
in `.claude-plugin/marketplace.json` and validated with `claude plugin validate .`
before each release.

## Sources

Each link backs a specific claim above.

- **graphify** — <https://github.com/Graphify-Labs/graphify>. Install and the
  `graphify <agent> install` commands (the package is `graphifyy`, the command is
  `graphify`); team setup, `graphify hook install`, and the `git pull` alias
  (we diverge from its "commit `graphify-out/`" suggestion, for the reasons
  above); `.graphifyignore` syntax and how it merges with `.gitignore`; the
  privacy model (local tree-sitter parsing, no API key, `--code-only` skips the
  LLM pass); and the full command reference for `extract`, `cluster-only`,
  `update`, `god-nodes`, and `query`.
- **graphify on PyPI** — <https://pypi.org/project/graphifyy/>. Confirms the
  package name is `graphifyy` (double-y).
- **uv** — <https://docs.astral.sh/uv/>. `uv tool install` isolation and
  `uv tool update-shell` for PATH setup.
- **git gitattributes / merge drivers** —
  <https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver>. Why a
  committed `merge=` attribute needs a driver defined in every clone. We commit
  the attribute `graphify hook install` writes, but since we git-ignore the graph
  the driver never fires — an inert line, no warnings for anyone.
- **git hooks** — <https://git-scm.com/docs/githooks>. Hooks live in
  `$GIT_DIR/hooks` and aren't versioned; sharing them would need `core.hooksPath`.
  This is the husky bootstrap we rejected.
- **Claude Code plugins & skills** —
  <https://docs.claude.com/en/docs/claude-code>. Plugin/skill layout and the
  strict `plugin.json` manifest.
