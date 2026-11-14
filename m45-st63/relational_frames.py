#!/usr/bin/env python3
"""ST63: relational phase under a shared U(1) reference-frame uncertainty.

Two qubits A (reference) and B (system) start in equatorial states with
phases alpha,beta. A global U(1) twirl removes coherence between different
total excitation-number sectors, while preserving coherence in the
one-excitation sector. The relative phase beta-alpha is gauge invariant.

This is a limited U(1) relational model, not a full QRF transformation.
"""
import argparse
import cmath
import json
import math

def validate(alpha,beta):
    for name,v in (("alpha",alpha),("beta",beta)):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>1e6:
            raise ValueError(name+" must be finite and bounded")

def amplitudes(alpha,beta):
    return (0.5,
            0.5*cmath.exp(1j*beta),
            0.5*cmath.exp(1j*alpha),
            0.5*cmath.exp(1j*(alpha+beta)))

def density(psi):
    return [[a*b.conjugate() for b in psi] for a in psi]

def twirl(rho):
    # |00>,|01>,|10>,|11> have total excitation numbers 0,1,1,2.
    sectors=(0,1,1,2)
    return [[rho[i][j] if sectors[i]==sectors[j] else 0j
             for j in range(4)] for i in range(4)]

def trace(rho):
    return sum(rho[i][i] for i in range(len(rho)))

def purity(rho):
    return sum(abs(v)**2 for row in rho for v in row)

def analyze(alpha=0.2,beta=1.1,shared_shift=0.7):
    validate(alpha,beta)
    validate(shared_shift,0)
    original=density(amplitudes(alpha,beta))
    shifted=density(amplitudes(alpha+shared_shift,beta+shared_shift))
    reduced=twirl(original)
    shifted_reduced=twirl(shifted)
    invariant_error=max(abs(reduced[i][j]-shifted_reduced[i][j])
                        for i in range(4) for j in range(4))
    if invariant_error>1e-10:raise AssertionError("collective phase invariance failed")
    # rho[01,10] = exp(i(beta-alpha))/4. It is a relational coherence.
    relational_coherence=reduced[1][2]
    # Conditional normalized state on total-excitation sector 1, prob=1/2.
    conditioned=[[2*reduced[i][j] for j in (1,2)] for i in (1,2)]
    # Interference observable 2 Re rho[01,10] = cos(beta-alpha)/2.
    relative_x_expectation=4*relational_coherence.real
    encode=lambda matrix:[[[v.real,v.imag] for v in row] for row in matrix]
    return {
        "protocol":"M45-ST63-RELATIONAL-U1-REFERENCE-FRAMES-v1",
        "parameters":{"reference_phase_alpha":alpha,"system_phase_beta":beta,
                      "common_phase_shift":shared_shift},
        "twirled_joint_density_complex_pairs":encode(reduced),
        "one_excitation_conditional_density_complex_pairs":encode(conditioned),
        "one_excitation_probability":0.5,
        "relational_coherence_complex_pair":[relational_coherence.real,relational_coherence.imag],
        "relative_phase_cosine":relative_x_expectation,
        "trace":trace(reduced).real,
        "global_purity_before_twirl":purity(original),
        "global_purity_after_twirl":purity(reduced),
        "collective_phase_invariance_max_error":invariant_error,
        "interpretation":"U1_RELATIONAL_PHASE_INVARIANCE_NOT_GENERAL_QUANTUM_REFERENCE_FRAME_SWITCH"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--alpha",type=float,default=0.2)
    ap.add_argument("--beta",type=float,default=1.1)
    ap.add_argument("--shift",type=float,default=0.7)
    a=ap.parse_args()
    print(json.dumps(analyze(a.alpha,a.beta,a.shift),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
