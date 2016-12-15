# Roadmap

No dates, and nothing here is promised. The order reflects what an operator
running this weekly would ask for next.

## Report shape

- A `--summary` mode printing only the totals, for dashboards and CI logs.
- Per-owner deficit as a column in the owner summary, not only a count.
- A comparison mode that takes two JSON reports and prints what changed,
  instead of requiring `git diff` on the rendered text.

## Rates

- A `--rate-schedule` command that prints the SIMD-0437 step table from
  `docs/RATE_SCHEDULE.md` in machine-readable form, so tooling can pin a step
  without parsing documentation.
