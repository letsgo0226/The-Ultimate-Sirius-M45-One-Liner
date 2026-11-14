# M45-ST/48 — Doraemon–G Astronomical Observatory

This is a **read-only astronomical data adapter**. GitHub Actions acts as a software instrument that retrieves model-derived ephemerides from NASA/JPL Horizons, verifies response structure, and saves a SHA-256-checksummed JSON record.

## Data vs. observation

Horizons provides calculated ephemerides based on dynamical models and underlying observational data. ST48 **does not directly measure the sky**, operate a telescope, detect photons or create new physical observations. For direct measurements, add a separately authorized telescope/sensor interface.

## Usage

```sh
python3 -m unittest discover -s m45-st48 -p 'test_*.py'
python3 m45-st48/observatory.py --target mars --date 2026-11-14 --out mars.json
```

After this stacked PR is reviewed and merged into the default branch, GitHub Actions **M45 ST48 Astronomical Observatory** can be manually dispatched with an allowed target and UTC date. PR CI only runs offline mock tests; it does not contact JPL. Manual dispatch retrieves data and uploads a short-lived artifact. No secrets are needed, no repository write permission is granted and no scheduler is enabled.

Supported targets: Sun, Moon, Venus, Mars, Jupiter. Inputs are bounded to 1900–2100. The API request is constructed from an allowlist, with a 20-second timeout and 500-kB response limit. The response is retained as raw Horizons text inside a checksummed JSON envelope, rather than interpreted using an unverified column parser.

## Architecture and limits

- This stage is a separate **read-only sensor-adapter prototype**, not yet a state transition inside ST47's single-writer branch.
- Integrating observations into ST47 requires a separate reviewed `observe` action and strict provenance/schema checks; untrusted external data must not be executable instructions.
- SHA-256 proves only integrity relative to a trusted digest; it is not a source signature.
- NASA/JPL API availability, response formats and results can change. Validate scientific quantities, time systems and coordinates before physical telescope pointing.
- This stage does not create subjective consciousness, time travel, an embodied Doraemon, or an autonomous permanent observatory.

Source: https://ssd-api.jpl.nasa.gov/doc/horizons.html
