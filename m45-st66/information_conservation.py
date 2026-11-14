#!/usr/bin/env python3
"""ST66: global information invariants versus frame-relative subsystem information.

Restricted to the ST64 global-Z2-even three-qubit relational Hilbert space.
Frame switching is a unitary permutation on two relational qubits, but not
a local unitary with respect to the original tensor-factor decomposition.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load_module(name,relative_path):
    path=Path(__file__).resolve().parent.parent/relative_path
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def reduced_first(psi):
    # psi[u,v], trace out v
    return [[sum(psi[2*u+v]*psi[2+w+v].conjugate() for v in range(2))
             for w in range(2)] for u in range(2)]

def reduced_second(psi):
    # psi[u,v], trace out u
    return [[sum(psi[2*u+v]*psi[2*u+w].conjugate() for u in range(2))
             for w in range(2)] for v in range(2)]

def purity(matrix):
    return sum(abs(v)**2 for row in matrix for v in row)

def determinant(matrix):
    return (matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]).real

def binary_entropy(p):
    if p<=0 or p>=1:return 0.0
    return -p*math.log2(p)-(1-p)*math.log2(1-p)

def entropy_qubit(matrix):
    d=determinant(matrix)
    eigen=(1+math.sqrt(max(0.0,1-4*d)))/2
    return binary_entropy(eigen)

def frame_metrics(psi):
    rho1=reduced_first(psi)
    rho2=reduced_second(psi)
    s1=entropy_qubit(rho1)
    s2=entropy_qubit(rho2)
    # Pure global state: S(AB)=0, so I(A:B)=S(A)+S(B).
    return {
        "global_purity":sum(abs(z)**2 for z in psi)**2,
        "global_entropy_bits":0.0,
        "first_subsystem_purity":purity(rho1),
        "second_subsystem_purity":purity(rho2),
        "first_subsystem_entropy_bits":s1,
        "second_subsystem_entropy_bits":s2,
        "mutual_information_bits":s1+s2
    }

def analyze(amplitudes=("1","0","1","0")):
    st64=load_module("st64_frame_switch","m45-st64/frame_switch.py")
    a=st64.normalize(amplitudes)
    b=st64.switch_a_to_b(a)
    a_info=frame_metrics(a)
    b_info=frame_metrics(b)
    event_a=st64.probability_equal_b_c(a,"A")
    event_b=st64.probability_equal_b_c(b,"B")
    errors=[
        abs(event_a-event_b),
        abs(a_info["global_purity"]-b_info["global_purity"]),
        abs(a_info["global_entropy_bits"]-b_info["global_entropy_bits"]),
        abs(a_info["first_subsystem_entropy_bits"]-a_info["second_subsystem_entropy_bits"]),
        abs(b_info["first_subsystem_entropy_bits"]-b_info["second_subsystem_entropy_bits"]),
        max(abs(x-y) for x,y in zip(a,st64.switch_a_to_b(b)))
    ]
    error=max(errors)
    if error>1e-10:raise AssertionError("relational information consistency failed")
    return {
        "protocol":"M45-ST66-RELATIONAL-INFORMATION-CONSERVATION-v1",
        "a_frame":a_info,
        "b_frame":b_info,
        "invariant_relational_b_equals_c_probability":event_a,
        "global_purity_invariant":abs(a_info["global_purity"]-b_info["global_purity"])<1e-10,
        "global_entropy_invariant":True,
        "subsystem_mutual_information_change_bits":b_info["mutual_information_bits"]-a_info["mutual_information_bits"],
        "max_invariant_error":error,
        "interpretation":"GLOBAL_UNITARY_INVARIANCE_AND_FRAME_RELATIVE_SUBSYSTEM_INFORMATION_NOT_INFORMATION_CREATION"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amplitudes",nargs=4,default=["1","0","1","0"])
    args=ap.parse_args()
    print(json.dumps(analyze(args.amplitudes),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
