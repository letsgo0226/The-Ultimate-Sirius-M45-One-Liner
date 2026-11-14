# M45-ST/28 — GitHub-native Turing Machine prototype

This prototype stores a **fixed finite transition table** (`delta.json`), a deterministic tape simulator (`machine.py`), and a manual GitHub Actions workflow (`.github/workflows/m45-st28.yml`).

The included machine is deliberately narrow: **unary successor** (`111 → 1111`). It is a genuine transition-table machine but **not** a universal Turing machine and **not** an SK evaluator. Its purpose is to validate the GitHub execution/checkpoint architecture before integrating M45-ST SK semantics.

## Run locally

```sh
python3 m45-st28/machine.py --tape 111 --steps 100 --out certificate.json
python3 m45-st28/machine.py --verify certificate.json
python3 -m unittest discover -s m45-st28 -p 'test_*.py'
```

## Run on GitHub

After merging this PR, visit **Actions → M45 ST28 GitHub Native TM → Run workflow**, supply a unary tape and maximum step count. Download the `m45-st28-certificate` artifact from the completed run.

## Design boundaries

- GitHub Actions runs finite batches, not continuously.
- Each run currently exports a checkpoint as an **artifact**, not an automatically committed new state. Resume is supported locally with `--resume`.
- The certificate contains a table hash, a step trace, and a self-checking digest. The current verifier checks the digest and each individual rule but does **not** independently prove the complete trace chain from an authenticated starting configuration. This is a future hardening task.
- No repository-wide autonomous write access is enabled; workflow uses `contents: read`.
- No GitHub Pages site is enabled in this version.
- The system is entirely GitHub-hostable once the workflow is merged and executed, but no GitHub workflow has been run at the time of publication.
