# M45-ST/29 — Doraemon Lab on GitHub Pages

An unofficial Doraemon-inspired computational research interface.

## What is implemented

- Static GitHub Pages website in `m45-st29/site/`.
- Entirely client-side SK combinator evaluation in `sk.js`, using leftmost-outermost reduction.
- Downloadable JSON computation traces.
- Node smoke tests: `node m45-st29/test_sk.cjs`.
- GitHub Actions Pages workflow in `.github/workflows/m45-st29-pages.yml`.

## Publishing

This feature branch is based on `feature/m45-st28-github-tm`, **not main**. Merge the ST28 PR first, then this PR. Enable GitHub Pages with **Source: GitHub Actions** under repository Settings → Pages. The workflow will run on a merge to main touching ST29, or can be started manually. The website URL is provided by the successful deploy job; do not assume it is live before deployment succeeds.

## Important boundaries

- Browser evaluation is JavaScript, not a proven fixed-table universal Turing machine.
- ST28 provides a fixed-table unary-successor machine and GitHub Actions certificate artifacts. ST29 does **not** yet connect the SK evaluator to that fixed transition table.
- Browser certificate downloads are stored by the user, not automatically persisted in GitHub commits. GitHub Actions artifacts are retention-limited.
- GitHub Pages is static; no secret token or privileged server is embedded in the client.
- This is not an AI chat service, not an official Doraemon project, and does not cause a fictional character to exist physically.
