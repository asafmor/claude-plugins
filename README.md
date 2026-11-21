# claude-plugins

A marketplace of Claude Code plugins.

## Install

```
/plugin marketplace add asafmor/claude-plugins
/plugin install graphify@asafmor-plugins
/plugin install travel@asafmor-plugins
/plugin install visuals@asafmor-plugins
/plugin install review-tools@asafmor-plugins
```

## Plugins

- **[graphify](./plugins/graphify)** — indexes a repo into a queryable knowledge graph and adds `/graphify-init` and `/graphify-research` skills for coding agents.

- **[travel](./plugins/travel)** — adds `/trail-researcher` for deep, current, source-backed trail and route planning reports.

- **[visuals](./plugins/visuals)** — adds `/codex-image-gen` for generating and post-processing images with the Codex CLI, and `/remotion-videos` for trailers, promos and social clips rendered with Remotion.

- **[review-tools](./plugins/review-tools)** — adds `/open-code-review` for running OpenCodeReview (`ocr`) on commits, branches or the whole repo with the right flags, and triaging its findings into fixes and reasoned rejections.

## Adding a plugin

1. `mkdir -p plugins/<name>/.claude-plugin` and add `plugin.json` there.
2. Add an entry to `.claude-plugin/marketplace.json` under `plugins`.
3. `claude plugin validate .` before pushing.
