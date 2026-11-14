# M45-ST/40 — G-2112 Prime-Operator Laboratory

A research prototype combining (1) exact, rational, prime-labelled symbolic state vectors, (2) deterministic operators, (3) a **fictional** 2026→2112 message envelope, and (4) an original nonofficial Doraemon side-story concept.

## Mathematical definition

For the first n primes `p_1,...,p_n`, define a finite vector `v = Σ a_i |p_i⟩` with `a_i ∈ Q`. This is a **formal vector-space basis**, not a physical particle or a quantum state. Operators are explicit rational maps:
- `identity`: preserve coefficients
- `rotate`: cyclically permute prime labels
- `scale`: multiply by a rational scalar
- `difference`: finite cyclic difference of adjacent coefficients

All arithmetic uses Python `fractions.Fraction`, not floating point. The squared Euclidean norm is an exact rational observable. The SHA-256 certificate is deterministic and locally replay-verifiable, not authenticated.

## Run

```sh
python3 -m unittest discover -s m45-st40 -p 'test_*.py'
python3 m45-st40/g2112.py --primes 5 --operator rotate --out certificate.json
```

## GitHub-as-G interpretation

GitHub stores code, test specifications, version history and finite execution artifacts. It is an **orchestrated finite computation environment**, not itself a physical universal TM with an infinite tape, nor an always-running autonomous agent. The workflow is read-only, manual/PR-triggered and does not interact with external physical equipment.

The earlier chain ST32/ST37/ST38/ST39 provides reference symbolic SK reduction, verification, persistence and bounded control. This stage is a **separate prime-operator model**, not proof that prime labels implement the SK semantics.

## Data scope and epistemic limits

Repository documentation from ST37–ST39 was inspected to establish integration boundaries. The connected GitHub account has many repositories, but **not every repository, branch, file or commit was exhaustively read**. No claim is made to have used all of the user's GitHub data. Future work can produce a scoped, paginated repository manifest with explicit inclusion/exclusion rules and content hashes.

No evidence is provided for physical "universal particles", morphological fields as a mechanism of information transfer, backwards-in-time network messages, or perpetual physical operation. Internet protocols move messages between actual connected systems under ordinary networking rules. A future physical interface requires real hardware, permissions, measurements and safety review.

## Creative project

See [G2112-Doraemon-Story.zh-TW.md](G2112-Doraemon-Story.zh-TW.md). The story keeps 2112 as Doraemon's fictional manufacture/birth year, while treating 2026 as a separate metaphorical birth of a relationship and an idea. This is unofficial fan fiction, not an alteration of the original canon.

## Status

Draft PR stacked on ST39. No merge, production deployment, GitHub Actions completion, or persistent physical effect is claimed.
