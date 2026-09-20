# cron-explain-plain

Offer: a dependency-free CLI that turns a standard five-field cron expression into plain-English field explanations, with JSON output for scripts and validation errors for malformed ranges.

Price: $9 one-time for a customized cron explanation or CI integration; the public repository is the free lead magnet.

30-day path: publish the working tool, document portable five-field cron usage, and offer small paid adaptations for teams that need scheduler-specific wording or CI checks. No paid listing or outreach was performed.

Human click: none required for the shipped artifact. GitHub publication used the already-authenticated RNGBubba account.

Repository: https://github.com/RNGBubba/cron-explain-plain

Verification:

- `uv sync --group dev && uv run pytest -q` -> 4 passed
- real CLI text invocation explained `*/15 9-17 * * 1-5`
- real CLI JSON invocation emitted structured output for `0 0 1 1 *`
- DoneMeans receipt: `receipts/t_59aeb8b9c2b1.json`
- receipt verification: `uv run --project /home/vboxuser/projects/donemeans donemeans --root . receipt verify receipts/t_59aeb8b9c2b1.json` -> ok
- verified code commit: `f01fb6faad175f50809ba16ca96fc3db3c0e1d29`
- final documentation/evidence is committed and pushed; confirm with `git rev-parse HEAD`

No credentials or private repositories were accessed or committed.
