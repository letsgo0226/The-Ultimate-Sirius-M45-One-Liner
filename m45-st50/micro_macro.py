#!/usr/bin/env python3
"""ST50: exact finite-N micro-to-macro coarse-graining of independent qubits.

Born probabilities are taken in the Z basis; the dephasing channel from ST49
does not change those probabilities. This is NOT a collapse model.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load_st49():
    path=Path(__file__).resolve().parent.parent/"m45-st49"/"decoherence.py"
    spec=importlib.util.spec_from_file_location("m45_st49_decoherence",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def binomial(n,p):
    if not isinstance(n,int) or isinstance(n,bool) or not 1<=n<=256:
        raise ValueError("n must be an integer in 1..256")
    if not isinstance(p,(float,int)) or not math.isfinite(p) or not 0<=p<=1:
        raise ValueError("p must be finite in [0,1]")
    # lgamma avoids large intermediate factorials; normalize rounding.
    if p==0:return [1.0]+[0.0]*n
    if p==1:return [0.0]*n+[1.0]
    logs=[math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
          +k*math.log(p)+(n-k)*math.log1p(-p) for k in range(n+1)]
    peak=max(logs)
    weights=[math.exp(v-peak) for v in logs]
    total=math.fsum(weights)
    return [v/total for v in weights]

def analyze(n=16,p=0.5,gamma=0.0):
    st49=load_st49()
    rho=st49.dephase(st49.state(p),gamma)
    z=st49.measure(rho,"Z")
    x=st49.measure(rho,"X")
    distribution=binomial(n,z["plus"])
    majority=math.fsum(distribution[n//2+1:])
    tie=distribution[n//2] if n%2==0 else 0.0
    expected=n*z["plus"]
    variance=n*z["plus"]*(1-z["plus"])
    return {
        "protocol":"M45-ST50-MICRO-MACRO-v1",
        "interpretation":"FINITE_INDEPENDENT_QUBIT_COARSE_GRAINING_NOT_COLLAPSE",
        "assumptions":["identical independent qubits","Z-basis projective measurement",
                       "majority threshold k > n/2; ties separate"],
        "n":n,"p":p,"gamma":gamma,
        "single_qubit":{"Z":z,"X":x,"coherence_l1":2*abs(rho[0][1])},
        "macro":{"k_distribution":distribution,
                 "majority_plus":majority,"tie":tie,
                 "majority_minus":math.fsum(distribution[:(n+1)//2]),
                 "expected_plus_count":expected,"variance_plus_count":variance,
                 "fraction_standard_deviation":math.sqrt(variance)/n}
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=16)
    ap.add_argument("--p",type=float,default=0.7)
    ap.add_argument("--gamma",type=float,default=0)
    args=ap.parse_args()
    print(json.dumps(analyze(args.n,args.p,args.gamma),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
