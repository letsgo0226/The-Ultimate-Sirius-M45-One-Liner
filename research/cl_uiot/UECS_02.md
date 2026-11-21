# UECS-02: full restricted certificate Goedel codec
UECS-01 offline CI 44923222997 passed.
Canonical sorted compact ASCII JSON encodes Fraction as tagged
numerator/denominator, tuple as array. Every field of the existing
restricted certificate is preserved, including the tableau.
Base 257 with sentinel 1 and byte+1 digits is injective by repeated
Euclidean division. Decode checks sentinel, digits, size, certificate
validity and exact canonical reserialization. Limit 4096 bytes.
289 instance roundtrips plus byte alphabet, malformed and
noncanonical encodings tested; CI pending. This is not serialization
of Lean proof terms, authentication, or general proof verification.
No merge, deployment or baseline Schumann Machine modification.
