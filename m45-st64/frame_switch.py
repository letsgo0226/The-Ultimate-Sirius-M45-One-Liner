#!/usr/bin/env python3
"""ST64: three-qubit relational frame switching for a finite Z2 symmetry.

Physical labels (a,b,c) have an unobservable simultaneous bit flip.
We work in the +1 global-X invariant sector and encode four relational
amplitudes in A coordinates (b XOR a, c XOR a). Switching to B
coordinates (a XOR b, c XOR b) is a unitary permutation (u,v)->(u,u XOR v).
This is a finite-group toy, NOT a general quantum reference-frame switch.
"""
import argparse
import cmath
import json
import math

def normalize(values):
    if len(values)!=4:
        raise ValueError("exactly four relational amplitudes required")
    try:
        amplitudes=tuple(complex(v) for v in values)
    except (TypeError,ValueError,OverflowError):
        raise ValueError("invalid complex amplitude") from None
    if any(not math.isfinite(z.real) or not math.isfinite(z.imag) for z in amplitudes):
        raise ValueError("amplitudes must be finite")
    n=math.sqrt(sum(abs(z)**2 for z in amplitudes))
    if not n or not math.isfinite(n):
        raise ValueError("nonzero finite norm required")
    return tuple(z/n for z in amplitudes)

def index(u,v):
    return 2*u+v

def switch_a_to_b(psi):
    out=[0j]*4
    for u in (0,1):
        for v in (0,1):
            out[index(u,u^v)]=psi[index(u,v)]
    return tuple(out)

def lift_to_three_qubits(psi):
    # Each relational orbit has two equally weighted representatives.
    full=[0j]*8
    for a in (0,1):
        for b in (0,1):
            for c in (0,1):
                full[4*a+2*b+c]=psi[index(a^b,a^c)]/math.sqrt(2)
    return tuple(full)

def density(psi):
    return tuple(tuple(a*b.conjugate() for b in psi) for a in psi)

def probability_equal_b_c(psi,frame):
    # In A coordinates B XOR C = u XOR v; in B coordinates B XOR C = v.
    return sum(abs(psi[index(u,v)])**2 for u in (0,1) for v in (0,1)
               if ((u^v)==0 if frame=="A" else v==0))

def analyze(amplitudes=("1","1j","2","-1"),phase=0.37):
    if isinstance(phase,bool) or not isinstance(phase,(int,float)) or not math.isfinite(phase) or abs(phase)>1e6:
        raise ValueError("phase must be finite and bounded")
    a=normalize(amplitudes)
    b=switch_a_to_b(a)
    roundtrip=switch_a_to_b(b)
    full=lift_to_three_qubits(a)
    # Global X⊗X⊗X leaves the lifted physical state unchanged.
    symmetry_error=max(abs(full[k]-full[k^7]) for k in range(8))
    # A common global phase has no effect on any density matrix.
    phased=tuple(z*cmath.exp(1j*phase) for z in a)
    phase_error=max(abs(x-y) for r1,r2 in zip(density(a),density(phased))
                    for x,y in zip(r1,r2))
    norm_error=abs(sum(abs(z)**2 for z in full)-1)
    invariant_error=max(abs(probability_equal_b_c(a,"A")-probability_equal_b_c(b,"B")),
                        max(abs(x-y) for x,y in zip(a,roundtrip)),
                        symmetry_error,phase_error,norm_error)
    if invariant_error>1e-10:
        raise AssertionError("relational frame invariance failed")
    encode=lambda psi:[[z.real,z.imag] for z in psi]
    return {
        "protocol":"M45-ST64-Z2-QUANTUM-REFERENCE-FRAME-SWITCH-v1",
        "symmetry":"simultaneous global X bit flip on A,B,C",
        "scope":"global-X-even-sector-only",
        "a_frame_relational_amplitudes_complex_pairs":encode(a),
        "b_frame_relational_amplitudes_complex_pairs":encode(b),
        "lifted_three_qubit_amplitudes_complex_pairs":encode(full),
        "reference_invariant_b_equals_c_probability":probability_equal_b_c(a,"A"),
        "global_phase_shift_radians":phase,
        "max_frame_invariant_error":invariant_error,
        "interpretation":"FINITE_Z2_RELATIONAL_UNITARY_PERMUTATION_NOT_GENERAL_QRF_OR_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amplitudes",nargs=4,default=["1","1j","2","-1"])
    ap.add_argument("--phase",type=float,default=0.37)
    args=ap.parse_args()
    print(json.dumps(analyze(args.amplitudes,args.phase),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
