# Doraemon Lab — M45-ST/27

An **unofficial** future-technology / SK combinator experiment. This is not affiliated with the owners of Doraemon and uses no official character artwork or voice.

## Features

- Prefix SK expressions: `@` = application, `S` and `K` = combinators.
- Leftmost-outermost reduction, up to 100 steps.
- Human-readable reduction trace and bounded execution.
- Python 3 **standard library only**; no external AI service and no API keys.

## Local use

```sh
cd doraemon-lab
python3 app.py
# Open http://localhost:8000/
```

API example:

```sh
curl -s http://localhost:8000/api/sk -H 'Content-Type: application/json' -d '{"expression":"@@@SKKS","budget":20}'
```

Expected reduction trace: `@@@SKKS → @@KS@KS → S`.

## Deploy on Render

This repository includes `render.yaml` in its root. Create a Render Blueprint against this branch, or create a Python Web Service with:

- Root directory: `doraemon-lab`
- Build command: `echo ready`
- Start command: `python3 app.py`
- Health endpoint: `/health`

GitHub Pages alone cannot run this Python API; Render or another Python hosting platform is needed.

## Status

M45-ST/27 is a **Python SK evaluator**, not a demonstrated single fixed transition-table Turing machine; it does not make fictional characters physically real.
