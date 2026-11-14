# M45-ST/87 — Academic Priority Research Audit

Daily GitHub Actions audit of ST86 Python and JavaScript assignment guards,
plus an on-demand and PR-triggered check. The job is read-only, with checkout
credentials disabled and no production secrets. It emits a JSON evidence
artifact, including per-check pass/fail and output SHA-256, and fails closed.

The daily cron uses UTC (19:17 UTC = 03:17 Asia/Taipei).
GitHub scheduled workflows normally run from the repository's default branch;
this draft PR will not activate the schedule until the workflow is merged.
GitHub schedule timing may be delayed. This is **not** an AI coding agent,
automatic code repair, or actual online deployment. Production deployment,
merges, and independent approvals remain disabled. ST86's event-driven
assignment workflow likewise requires integration into the default branch
for reliable event activation.
