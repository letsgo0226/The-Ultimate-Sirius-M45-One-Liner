#!/usr/bin/env python3
"""ST65: frame-dependent entanglement under finite Z2 relational switching.

A frame uses qubits (B xor A,C xor A). B frame uses (A xor B,C xor B).
The frame switch is CNOT on the relational two-qubit Hilbert space:
(u,v) -> (u,u xor v). Entanglement of the two coordinate factors can
change, while relational physical probabilities are invariant.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load_st64():
    path=Path(__file__).resolve().parent.parent/"m45-st64"/"frame_switch.py"
    spec=importlib.util.spec_from_file_location("m45_st64_frame_switch",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def entropy_binary(p):
    if p<=0 or p>=1:return 0.0
    return -p*math.log2(p)-(1-p)*math.log2(1-p)

def concurrence(psi):
    a,b,c,d=psi
    return min(1.0,2*abs(a*d-b*c))

def entanglement_entropy(psi):
    c=concurrence(psi)
    eigen=(1+math.sqrt(max(0.0,1-c*c)))/2
    return entropy_binary(eigen)

def analyze(amplitudes=("1","0","1","0")):
    st64=load_st64()
    a=st64.normalize(amplitudes)
    b=st64.switch_a_to_b(a)
    back=st64.switch_a_to_b(b)
    invariant_a=st64.probability_equal_b_c(a,"A")
    invariant_b=st64.probability_equal_b_c(b,"B")
    error=max(abs(invariant_a-invariant_b),max(abs(x-y) for x,y in zip(a,back)))
    if error>1e-10:raise AssertionError("frame switch invariance failed")
    encode=lambda v:[[z.real,z.imag] for z in v]
    return {
        "protocol":"M45-ST65-RELATIONAL-ENTANGLEMENT-v1",
        "a_frame_amplitudes_complex_pairs":encode(a),
        "b_frame_amplitudes_complex_pairs":encode(b),
        "a_frame_concurrence":concurrence(a),
        "b_frame_concurrence":concurrence(b),
        "a_frame_entanglement_entropy_bits":entanglement_entropy(a),
        "b_frame_entanglement_entropy_bits":entanglement_entropy(b),
        "reference_invariant_b_equals_c_probability":invariant_a,
        "max_frame_invariant_error":error,
        "interpretation":"FRAME_DEPENDENT_RELATIONAL_TENSOR_FACTORIZATION_NOT_PHYSICAL_ENTANGLEMENT_CREATION"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amplitudes",nargs=4,default=["1","0","1","0"])
    a=ap.parse_args()
    print(json.dumps(analyze(a.amplitudes),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
