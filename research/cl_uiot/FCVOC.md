# Fourier–Chiral Virtual Operator Computer (prototype 1)
Four-cell integer cyclic tape. J maps index k to -k modulo 4. S_d
moves each value by d. D is the unnormalized four-point DFT over Gaussian
integers. D inverse uses conjugate roots and division by four.
J S_d J = S_{-d}; D J = J D; D S_d = diag(exp(-2 pi i k d/4)) D.
These identities follow by substitution of summation indices.
Tests exhaust 625 tapes with entries -2 through 2, not all integer tapes.
Pure local transformations only, no execution of encoded tape, network,
replication, credentials, biological experiment or deployment.
This models tape translation, not a universal Turing machine or permanent
execution. No hardware independence or speed advantage established.
GCAPO base lemmas passed Lean run 44908402703; FCVOC is separate and not
yet formally checked in Lean. FFPCO remains pending.
