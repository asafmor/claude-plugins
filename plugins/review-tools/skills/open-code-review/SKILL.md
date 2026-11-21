---
name: open-code-review
description: How to run the `ocr` CLI (OpenCodeReview, github.com/alibaba/open-code-review) well, and how to act on what it finds. It covers choosing between commit, branch, workspace and whole-repo review; flags that keep the run cheap and focused; reading its JSON; and triaging findings into fixes and reasoned rejections. Use it whenever the user mentions ocr, "open code review", OpenCodeReview, an external or AI code review of a commit, branch, PR or the whole repo, or asks to review recent work and act on the findings, even if they only say "run ocr" or "get a second review". Also use it before re-running ocr after fixes, resuming a cut-off ocr session, or comparing two reviews.
---

# open-code-review (`ocr`)

`ocr` sends a diff, or whole files, to an LLM agent. The agent also explores the repository itself (it reads files and runs code searches), then returns review comments. Each comment has a file, a line range, a severity and a suggestion. Written against **v1.14.0**; run `ocr --help` and `ocr <cmd> --help` if flags look different.

- **`references/setup.md`:** the one-time install and model setup. Read it when `ocr` is missing or no provider is configured.
- **`references/experience.md`:** an honest field report on what it caught, what it missed, cost, and noise. Read it before planning a large review or deciding how much to trust a finding.

## 1. Preflight (one minute, saves a failed run)

**Not installed, or no model configured yet?** Read `references/setup.md`. It covers installing, configuring a provider once (ChatGPT sign-in, or an API key through an environment variable or `api_key_cmd`, never pasted into the config), and delegation mode, which needs no ocr model at all.

```bash
ocr version
ocr auth status        # ChatGPT-plan sign-in shows an expiry time (about an hour ahead when I checked)
ocr review -c <sha> -p # --preview: the files it will review, no LLM call
```

- **Expired or signed out:** ask the user to run `! ocr auth login`. It's interactive; don't try to automate it.
- **Provider keys:** `ocr config set providers.<name>.api_key ...` writes the key in plain text to `~/.opencodereview/config.json`. Prefer a per-run environment variable or `api_key_cmd` (see `references/setup.md`). Ask the user how they keep their keys.
- **Check the preview for noise:** prototypes, mockups, generated files, research notes, lockfiles and vendored code. Exclude them (see §3). On one repo, a frozen HTML prototype produced 44 of about 160 scan comments, all useless.

## 2. Pick the mode

| You want to review | Command | Notes |
|---|---|---|
| One commit (best signal) | `ocr review -c <sha>` | Compares with the parent. Ideal when work is one commit per feature: run one review per commit, in parallel. |
| A branch or range | `ocr review --from main [--to <ref>]` | Merge-base mode. `--to` defaults to `HEAD`. |
| Uncommitted work | `ocr review` | Staged, unstaged and untracked files. |
| Existing code, no diff | `ocr scan [--path dir,file]` | Whole files. Many comments and a high triage cost; scope it with `--path`. |
| Review it yourself with ocr's rules (no LLM spend) | `ocr delegate preview ...`, then `ocr delegate rule <files>` | Prints the files and resolved rules for you, the host agent, to apply. Useful when the provider quota is gone. |

Prefer `review -c` or `review --from` over `scan` whenever there is a diff. Diff reviews were faster and far more actionable: 76% and 89% of comments led to a fix in two commit reviews, against about 22% for a whole-repo scan (see the reference).

## 3. The command to reach for

```bash
ocr review -c <sha> \
  --format json --audience agent \
  --exclude '.impeccable/**,docs/research/**,**/generated/**' \
  --background "<what this change does and why; the product decisions that are deliberate>" \
  --max-tokens-budget 1500000 \
  -o /tmp/ocr-<feature>.json
```

- **`--format json --audience agent`:** machine-readable output with no progress noise. `-o` writes the file directly; with `>` redirection, send stderr elsewhere.
- **`--background`:** the strongest lever on noise. State the user's deliberate decisions in plain words, for example "both the app and the widget show one shared 'as of' time on purpose" or "yields are labelled before tax on the plate only, by the owner's choice". The reviewer can't know product intent otherwise, and will flag it. `--background-file docs/requirements.md` works for longer context.
- **`--exclude`:** gitignore-style patterns, merged with any excludes in `rule.json`.
- **`--max-tokens-budget`:** cost control. The reviewer explores the repo freely. One 9-file commit used 2.3 M tokens (43 file reads, 26 code searches), so set a budget on large or repeated runs. If the budget runs out, the run stops and returns whatever it has found so far.
- **Time:** expect 3–6 minutes per feature-sized commit, and longer for scans. Run it in the background (for example `run_in_background`) and keep working. `--timeout` (default 15 min) caps the whole run, so raise it for big scans.
- **Other knobs:** `--effort low|medium|high` trades depth against cost; `--provider` and `--model` override the configured LLM for one run; `--no-filter` keeps comments the post-filter would drop (rarely worth it).

## 4. Read the result

```bash
python3 - <<'EOF'
import json, collections
d = json.load(open('/tmp/ocr-<feature>.json'))
print(d['status'], d['llm'], d['summary'])  # files_reviewed, comments, tokens, elapsed
print(collections.Counter(c['severity'] for c in d['comments']))
for i, c in enumerate(d['comments'], 1):
    print(f"#{i} [{c['severity']}/{c.get('category')}] {c['path']}:{c['start_line']}-{c.get('end_line')}\n   {c['content']}\n")
EOF
```

- **Top-level keys:** `status`, `llm`, `message`, `summary`, `tool_calls` (`total`, `by_tool`), `comments`, `groups`, `session_id`, `manifest`.
- **Comment keys:** `path`, `start_line`, `end_line`, `severity` (low, medium, high), `category` (mostly `bug`), `content` (the finding and its suggested fix), `existing_code`.
- **Numbering:** number the comments in output order (#1, #2, …) and keep those numbers. They become the IDs in your triage and in the fix commit message.

## 5. Triage: act on findings without obeying them

The reviewer is usually right about mechanics: races, identity, state, cancellation, encoding. It is weaker on product intent, and it can't run anything. Treat every comment as a claim to check.

1. **Open the code at each location before deciding.** Confirm the failure scenario is real in this codebase, not just plausible in general.
2. **Group comments that share a root cause.** For example, "the app overwrites the widget's quotes" and "the widget's merge isn't atomic" were one fix: a single locked newest-wins merge. Fix it once, where every caller goes through.
3. **Decide on each comment:**
   - **Fix** when the failure is real, or the fix is cheap and strictly better.
   - **Reject, with a reason,** when it contradicts a decision the user made, is a sub-frame race with a harmless outcome, adds machinery for a scenario the product doesn't have, or misreads the domain. A user-approved product or UX decision outranks the reviewer; cite the decision.
   - **Fix part of it** when only part is right. Say which part you fixed and why.
4. **Verify like any change:** tests, plus running the app or the affected path. Static review misses runtime-only failures (see the reference), so device or manual checks still matter.
5. **Write the audit trail in the fix commit:** one fix commit per reviewed commit, listing "Fixed: #n …" and "Not changed: #n — reason". The user can then see that every comment was considered. Also tell them, briefly, what was rejected and why.
6. **Optionally, re-review the fix commit** (`ocr review -c <fix-sha>`), or compare sessions, to make sure the fixes didn't introduce new findings.

Don't silently "fix" everything. About 10–25% of comments in a good diff review deserve a reasoned rejection. Applying them all usually over-engineers the code or overrides the owner's choices.

## 6. Sessions, resume, rules

```bash
ocr session list                  # every run for this repo: mode, range, files, comments, status
ocr session comments <id>         # re-read one run's comments without re-running
ocr session compare <id-a> <id-b> # what changed between two reviews
ocr session export <id>           # one self-contained HTML file to share
ocr scan --resume <id>            # or: ocr review ... --resume <id>, after a quota cut-off or timeout
ocr rules check <file>            # which built-in or custom rule applies to a path
ocr review --rule rules.json ...  # custom system rules and excludes
```

A status such as `legacy (15 fail)` in `session list` means part of the run failed: 15 subtasks, in that case, after a ChatGPT plan quota error (`subscription_sharing_usage_limit_exceeded`). Tell the user which files went unreviewed, and resume once the quota resets. Don't present a partial run as complete.

## 7. Pitfalls seen in practice

- **Commit mode reviews only what was committed.** Commit first, or use plain `ocr review` for uncommitted work.
- **Order with releases:** reviewing before tagging catches issues pre-release. If the user asks for release-then-review, follow it, and ship the fixes as the next version.
- **It can't see screens or run code.** Platform behaviour, layout and visual quality need on-device checks. Examples: Android RemoteViews refusing a class, launcher quirks, and a font-rendering bug that showed only on one startup path.
- **Severity is only roughly calibrated.** Read every medium; "high" has been right.
- **Token use scales with how much it explores, not with diff size.** Budget accordingly, and say so to the user if they pay per token.
- **Parallel runs on different commits work fine,** and each gets its own session.
