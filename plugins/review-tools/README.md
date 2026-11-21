# review-tools

Code review for coding agents.

- **`/open-code-review`** — runs [OpenCodeReview](https://github.com/alibaba/open-code-review) (`ocr`) well and acts on what it finds.
  - **Choosing the run:** commit, branch, workspace, whole-repo scan, or delegation mode (no ocr model needed).
  - **Keeping it cheap and focused:** `--background` listing the owner's deliberate decisions, excludes for mockups and docs, a token budget, JSON to a file.
  - **Reading the results:** the JSON fields, plus a snippet that prints the comments numbered.
  - **Triage:** check each claim in the code, group comments with a shared cause, fix or reject with a reason, and leave a numbered "Fixed / Not changed" record in the fix commit.
  - **References:**
    - `references/setup.md`: one-time install and model setup, with keys kept out of the config file via an environment variable or `api_key_cmd`.
    - `references/experience.md`: an honest field report from real runs (what it caught, what it missed, cost and noise).

## Install

```
/plugin install review-tools --marketplace asafmor/claude-plugins
```

or, once the marketplace is added (`/plugin marketplace add asafmor/claude-plugins`): `/plugin install review-tools@asafmor-plugins`.

## Prerequisites

- Git 2.41 or newer, and the `ocr` CLI (`npm install -g @alibaba-group/open-code-review`). See the skill's `references/setup.md`.
- A model for ocr (an API key or a supported plan sign-in), or none at all in delegation mode.

## Usage

```
/open-code-review review the last two commits separately and fix what's worth fixing
/open-code-review scan android/app/src/main before the release, skip the prototype folder
/open-code-review the quota ran out mid-scan; resume it and report which files were never reviewed
```

It complements the project's own official skills and plugin (`npx skills add alibaba/open-code-review`). Those run the review; this one is about running it well and acting on the results.
