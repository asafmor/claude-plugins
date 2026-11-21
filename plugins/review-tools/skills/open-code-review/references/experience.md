# Field report: three real `ocr` runs, honestly

Written by the coding agent that ran these reviews, so future agents can calibrate trust and cost. The project was a Kotlin and Jetpack Compose Android app (a Hebrew, right-to-left market watchlist). It has no backend; it pulls data from public endpoints, with a home-screen widget and a fund-comparison feature. All runs used `ocr` v1.14.0 with the `chatgpt` provider, model `gpt-6.2-sol`, on the user's ChatGPT plan (November 2026).

## The runs

| Run | Command shape | Files | Comments | Tokens | Time | Acted on |
|---|---|---|---|---|---|---|
| Whole-repo scan | `ocr scan` (no excludes) | 27 (15 subtasks failed) | about 160 | n/a | long; stopped by the plan quota | about 35 fixed (about 22%) |
| Widget commit | `ocr review -c <sha> --format json --audience agent --exclude … --background …` | 11 | 17 (1 high, 13 medium, 3 low) | 0.60 M | 3 m 36 s | 13 fixed, 4 rejected with reasons |
| Check-up commit | same | 9 | 18 (14 medium, 4 low) | 2.28 M | 5 m 46 s | 16 fixed (one partly), 2½ rejected |

**The headline:** commit reviews with `--background` and excludes were worth it. Most comments were real, and several were bugs I had missed. The unscoped whole-repo scan cost a lot of triage for a much lower hit rate, and it ran out of quota partway.

## What it was genuinely good at

**Concurrency and shared state.** This was its best category. It found:
- **A cross-writer race (the high finding):** the app's ViewModel saved its in-memory price map over prices the widget's background worker had just stored, and the worker's read-merge-write wasn't atomic either. Both were fixed with a single locked newest-wins merge.
- **A "ready" flag set too early:** the flag was set at the start of the load, before parsing finished, so a failed first load looked like a completed one forever.
- **A file that could be read half-written:** a JSON file was written in place while another component could be reading it.
- **Redraws publishing out of order:** concurrent widget redraws could finish in the wrong order, leaving a stale list on screen.

**Platform semantics that are easy to get wrong.** It caught that:
- `withTimeoutOrNull` around a blocking OkHttp `execute()` does not interrupt it, so a broadcast receiver could outlive its time limit;
- PendingIntents that differ only in extras collapse into one, and keying tap targets by row instead of by asset can open the wrong item after a reorder;
- a widget bitmap needs a pixel bound, not just a density cap.

**Logic and counting.** It found a real bug I wrote and didn't notice. "Compared with 41 similar funds" and "beat 24 of 31" both counted the fund among its own peers. Its explanation was concrete ("in a three-fund group, a fund that beats both alternatives is shown as beating two of three").

**Overclaiming in UI text.** It flagged wording that promised more than the data supports:
- "Charged less last year" was built from current fees and trailing returns.
- Tax and payout timing were stated as guarantees for every fund.

For a finance-adjacent app this is valuable and easy to overlook.

**Domain and freshness details:**
- **Hebrew text order:** a date and time placed inside right-to-left Hebrew text without a Unicode isolate can render in reversed order. It even pointed to the existing helper that solves it.
- **A ticker rename:** SPLG now trades as SPYM. It cross-checked that against the repo's own research notes, which it found through its file search.

**Data hardening:** `toDoubleOrNull()` accepting "NaN" and "Infinity"; duplicate IDs breaking `LazyColumn` keys; a blank classification grouping unrelated funds; a required CSV column that nothing used.

**From the earlier scan:** a time-less quote stamped "now", which outranked newer delayed trades in a newest-wins merge and froze prices. Also one malformed item failing a whole batch, failures cached for an hour, and a search filter applied after the result cap.

## Where it fell short

**Runtime-only failures.** It is static: it reads code, it doesn't run it. None of these surfaced in review; each was found on the emulator:
- Android's widget host refusing a plain `<View>` ("Class not allowed to be inflated"), which crashed the widget on first placement;
- a Compose variable-font bug where a shared `Paint` skipped an identical font-variation string, so bold text rendered regular on one startup path;
- force-stopping an app cancels its widget PendingIntents.

**Product intent.** Even with `--background`, it flagged deliberate, owner-approved decisions as defects:
- the app and the widget sharing one "as of" clock;
- an hourly fetch while markets are closed (for closing prices and NAVs);
- "before tax" shown on one plate and not in table headers;
- blank widget rows opening the app.

These are reasoned rejections, not bugs, so expect a few in every run.

**Speculative or low-value findings rated "medium":**
- a navigation state-key race that needs a pop and a reopen within one frame, with a harmless worst case;
- landscape widget layouts for phones whose home screens are portrait;
- per-row valuation dates for a table that comes from one daily file.

**Over-engineered suggestions.** Its fixes are sometimes heavier than needed: separate timestamps per component, size-specific layout maps, per-row metadata. The diagnosis was often right while a smaller fix was enough.

**Right problem, wrong fix (scan).** For the frozen-price bug, the obvious fix (stamp time-less quotes at the start of the day) would have made the closing price lose to intraday ticks. The correct fix was different: stamp the session's close once it has passed, and the start of day before then. Verify the suggested fix as carefully as the diagnosis.

**Cost and scope.**
- **Token use tracks exploration, not diff size.** 2.28 M tokens for a 9-file diff: it made 85 tool calls, including 43 file reads and 26 code searches. That's good context and an expensive habit; use `--max-tokens-budget`.
- **The whole-repo scan with no excludes reviewed a frozen HTML prototype.** That produced 44 comments of pure noise, plus accessibility-only and font-scale items the owner had deferred.
- **The ChatGPT plan quota ended the scan partway.** 15 subtasks failed; the session list shows it as `legacy (15 fail)`. Some files were never reviewed until resumed.

**Architecture and UX.** It rarely questioned scope or design, for example downloading a 0.8 MB CSV once per process, or whether a screen is understandable. It works line by line. Use a human or a design review for those.

## How much to trust it

- **"High":** the one I saw was real. Act on it.
- **"Medium":** a mix of real bugs and theoretical edge cases. Read each one against the code; 23 of 27 (85%) were worth fixing across the two commit reviews.
- **"Low":** cheap polish, often worth taking (accessibility labels, formatting consistency).
- **Its diagnosis is more reliable than its proposed fix.** Re-derive the fix yourself.

## What I'd do differently next time

1. **Never run `scan` unscoped.** Use `--path` plus excludes for prototypes, mockups and docs, or prefer `review --from <base>`.
2. **Write `--background` as a list of deliberate decisions,** not just a description of the change. It's the cheapest way to cut false positives.
3. **Use `-o file` and `--max-tokens-budget`,** and check `ocr auth status` first, because the plan sign-in expires and quotas end runs.
4. **Review each feature commit right after it lands,** in parallel and in the background, before tagging a release. Shipping fixes as the next version works, but it's second best.
5. **Keep the numbered audit trail** ("Fixed: #n" / "Not changed: #n — reason") in the fix commit. Users noticed and valued it, and it made re-checking simple.

## Bottom line

As a second reviewer on a focused diff, `ocr` is worth its few minutes. It is consistently strong on concurrency, platform semantics, identity and keys, counting logic and overclaiming text, and it found real bugs that tests and my own review missed. It isn't a substitute for running the software, it doesn't know the product owner's intent, and an unscoped whole-repo scan is expensive and noisy. Trust its diagnoses, check its fixes, and own the rejections.
