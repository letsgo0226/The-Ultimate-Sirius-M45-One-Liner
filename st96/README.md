# ST96 — Sewashi × DARC-Net Continuity Bridge (research draft)

Status: **offline prototype; NOT deployed; NOT independently reviewed**.

## Scope

This stage links synthetic Sewashi venture-research notes and DARC-Net authorized research-state records through a strict common envelope. It is **not** an investing agent, actual cross-provider AI continuity mechanism, or a deployed service.

The Python demonstration:
- requires an explicit `approved_for_transfer: true` marker in the synthetic input;
- accepts only known record kinds, fixed sources and bounded payloads;
- rejects known sensitive field names recursively and explicitly prohibited actions;
- computes a SHA-256 digest and HMAC-SHA256 over deterministic JSON;
- tests three independent **in-memory** synthetic copies and rejects a mutated copy;
- uses a clearly public, fixed **test-only** key; this is NOT security-grade authentication.

## Known limitations / threat model

1. Field-denylisting is not content scanning or a substitute for data classification and human approval. No real data should be provided.
2. The fixed HMAC test fixture provides no identity authentication against attackers who know the key. Actual key management is deliberately out of scope.
3. A boolean authorization flag in an object is NOT authoritative external permission. Do not use the prototype on user records.
4. Three-node simulation is local only: no distributed consensus, synchronization, network isolation guarantee, or durable recovery has been proven.
5. The CI workflow consumes hosted GitHub Actions resources on PR runs. It has a 5-minute job timeout and `contents: read`, with no scheduled trigger, service deployment, payments, secrets or write token.
6. No claim of consciousness continuity, infinite computation, zero-entropy physical reality, metaphysical truths, or autonomous scientific discovery follows.

## Validation

Run: `python3 -B -m unittest discover -s st96 -p 'test_*.py' -v`

Acceptance requires CI evidence, independent human review and an explicit authorization decision for any future staging deployment. Do not merge, approve, deploy, trigger billing, or use/change secrets automatically.

## Next gates

1. Independent review of schema, unsafe payload handling and CI.
2. Expand synthetic negative tests (unknown kinds/sources, malformed envelopes, oversized inputs and nested prohibited actions).
3. Design authenticated authorization and durable persistence **on paper** before any protected integration.
4. Only after a separate user authorization, consider an isolated, no-production-traffic staging proof of concept with verified resource costs.
