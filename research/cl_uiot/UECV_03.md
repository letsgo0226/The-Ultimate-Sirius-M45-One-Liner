# UECV-03: encoding integrity audit
UECV-02 offline CI 44926137207 passed. Audit of the existing 257-base
sentinel codec: by Euclidean division, each final digit uniquely
determines the last byte and predecessor. Induction gives D(G(b))=b
for bounded bytes and G(D(n))=n for accepted codes. Injectivity follows.
Tests exhaust all 65793 strings of length 0..2, check integer-domain
roundtrips, 4096-byte boundary, invalid sentinel/digits/types, noncanonical
JSON and equivalent nonreduced rationals. A valid replacement certificate
is still accepted: canonical encoding is not authentication.
No codec behavior changed. This is mathematical reasoning and bounded
testing, not a Lean proof of the Python codec. CI pending. No merge,
deployment or baseline change.
