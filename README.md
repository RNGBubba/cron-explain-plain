# cron-explain

`cron-explain` is a small, dependency-free command-line tool for explaining standard five-field cron expressions in plain language. It validates field ranges and can emit either readable text or JSON for scripts.

## Usage

```bash
uv run cron-explain '*/15 9-17 * * 1-5'
uv run cron-explain --json '0 0 1 1 *'
```

The supported fields are minute, hour, day of month, month, and day of week. This intentionally focuses on the portable five-field format; it does not claim to implement every scheduler's extensions.

## Development

```bash
uv sync --group dev
uv run pytest -q
```

Released under the MIT license.
