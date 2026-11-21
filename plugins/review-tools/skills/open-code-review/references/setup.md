# One-time setup for `ocr`

Source: the project's README and its docs (`pages/src/content/docs/en/{installation,configuration,integrations/delegate}.md` in github.com/alibaba/open-code-review), read November 2026 at v1.14.x. Re-check `ocr --help` if something differs.

## 1. Prerequisites

- **Git 2.41 or newer** (`git --version`). ocr relies on Git for diffs, search and repository operations.
- **Node and npm** for the recommended install. Homebrew, the install script or a release binary avoid Node.

## 2. Install (pick one)

```bash
npm install -g @alibaba-group/open-code-review           # recommended; pin with @<version>
brew install open-code-review                            # macOS / Linux
curl -fsSL https://open-codereview.ai/install.sh | sh    # read the script before piping it to sh
# or download a release binary (opencodereview-<os>-<arch>) and check it against sha256sum.txt
ocr version                                              # verify
```

- **Auto-update:** the npm install updates itself in the background. Set `OCR_NO_UPDATE=1` to turn that off, for example to keep a pinned version.
- **Uninstall:** `npm uninstall -g @alibaba-group/open-code-review`.

## 3. Decide who runs the model

| | Native mode | Delegation mode |
|---|---|---|
| Who reviews | ocr's own review agent and pipeline | You, the host coding agent, inside ocr's file selection and rules |
| Needs | An LLM provider configured in ocr | Nothing beyond the CLI |
| Commands | `ocr review`, `ocr scan` | `ocr delegate preview`, then `ocr delegate rule` |
| Pick it when | The user has an API key or a supported plan sign-in for ocr | There's no separate key, or the provider quota is used up |

A coding-agent subscription (for example Claude Pro or Team) is **not** an API credential for native mode. Native mode uses only ocr's own provider configuration.

### Native mode: configure a provider once

The config lives in `~/.opencodereview/config.json`.

**Interactive (recommended).** It picks a provider, asks for a key, chooses a model, then runs `ocr llm test`. Being interactive, the user should run it themselves, e.g. `! ocr config provider`:

```bash
ocr config provider
ocr config model        # switch model later
```

**ChatGPT plan sign-in (preview, no API key).** The sign-in carries an expiry (see `ocr auth status`). Plan usage limits can stop a long run partway (`subscription_sharing_usage_limit_exceeded`); resume it later.

```bash
ocr auth login --provider chatgpt    # interactive: ask the user to run it
ocr auth status
```

**API key without writing the secret to disk.** Prefer these two routes:

```bash
# a) per run: built-in providers fall back to their environment variable when no key is configured
ANTHROPIC_API_KEY="$(pass <path-to-key>)" ocr review -c <sha> ...
#    (OPENAI_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY, … one per built-in provider)

# b) persistent, keeping the key in a secret manager: ocr stores the command, not the key
ocr config set providers.anthropic.api_key_cmd "pass <path-to-key>"
```

- **How `api_key_cmd` behaves:** it runs once per `ocr` invocation and must print exactly one line within 60 seconds. Any failure is a hard error; there is no silent fallback.
- **Precedence:** a static `api_key` beats `api_key_cmd`, which beats the environment variable.
- **Avoid** `ocr config set providers.<name>.api_key <secret>`. It writes the key in plain text into `config.json`. Do it only if the user explicitly wants that.
- **Never** paste or echo a key in chat or logs.

**Non-interactive (CI) setup** and a connectivity check:

```bash
ocr config set provider anthropic
ocr config set model <model-id>
ocr llm test
```

**Long requests:** `OCR_LLM_TIMEOUT=<seconds>` (default 300 per request) overrides the per-request timeout, independently of `--timeout`, which caps the whole run in minutes.

### Delegation mode: nothing to configure

Use the same range flags on both commands:

```bash
ocr delegate preview [-c <sha> | --from <ref> [--to <ref>]] [--exclude <patterns>]
ocr delegate rule    [same flags] <path1> <path2> ...    # rules grouped by content
```

Then get each file's diff, review every previewed file, and mark it `reviewed` or `skipped` with a reason. Report `total_files`, `reviewed_files`, `skipped_files` and `coverage_rate`, plus your findings by severity.

## 4. Optional: the project's official agent integrations

- **Official skills:** `npx skills add alibaba/open-code-review` installs `open-code-review` (native) and `open-code-review-delegate`.
- **Claude Code plugin:** it adds `/open-code-review:review` and `/open-code-review:delegate-review`. See `plugins/open-code-review/README.md` in the project.

This skill complements them: it covers choosing the run, controlling cost and noise, and triaging findings. A plugin's skills are namespaced, so both can be installed side by side.

## 5. First-run check

```bash
cd <repo>
ocr review -p            # preview the files; no LLM call
ocr review -c HEAD --format json --audience agent -o /tmp/ocr-first.json
```
