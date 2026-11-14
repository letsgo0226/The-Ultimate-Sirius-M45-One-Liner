#!/usr/bin/env python3
"""ST55: operational, threshold-dependent classicality indicators.

Independent qubits, Z-basis dephasing, and a Z-majority macro observable.
No assertion of objective wavefunction collapse or universal classicality.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load(name,relative):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parent.parent/relative)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def analyze(n=64,p=0.7,gamma=0.05,coherence_tolerance=0.05,majority_error_tolerance=0.05):
    st49=load("st49","m45-st49/decoherence.py")
    st50=load("st50","m45-st50/micro_macro.py")
    for name,v in (("coherence_tolerance",coherence_tolerance),
                   ("majority_error_tolerance",majority_error_tolerance)):
        if not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=1:
            raise ValueError(name+" must be finite in [0,1]")
    # Validates n,p and computes exact finite-N Z statistics.
    macro=st50.analyze(n,p,gamma)
    rho=st49.dephase(st49.state(p),gamma)
    coherence=2*abs(rho[0][1])
    # When p > 1/2, a Z-plus majority is the target; otherwise a Z-minus
    # majority is the target. A tie is counted as failure in either case.
    if p>0.5:
        target="plus"
        success=macro["macro"]["majority_plus"]
        gap=p-0.5
    elif p<0.5:
        target="minus"
        success=macro["macro"]["majority_minus"]
        gap=0.5-p
    else:
        target="none_at_p_half"
        success=None
        gap=0.0
    failure=max(0.0,min(1.0,1-success)) if success is not None else None
    hoeffding=min(1.0,math.exp(-2*n*gap*gap)) if success is not None else None
    low_coherence=coherence<=coherence_tolerance
    stable_majority=failure is not None and failure<=majority_error_tolerance
    return {
        "protocol":"M45-ST55-EMERGENT-CLASSICALITY-v1",
        "scope":"IID_QUBITS_Z_DEPHASING_Z_MAJORITY",
        "parameters":{"n":n,"p":p,"gamma":gamma,
                      "coherence_tolerance":coherence_tolerance,
                      "majority_error_tolerance":majority_error_tolerance},
        "observables":{"coherence_l1":coherence,
                       "z_fraction_std":macro["macro"]["fraction_standard_deviation"],
                       "majority_target":target,
                       "majority_success_probability":success,
                       "majority_failure_probability":failure,
                       "hoeffding_failure_upper_bound":hoeffding},
        "criteria":{"low_coherence":low_coherence,
                    "stable_majority":stable_majority,
                    "operational_classicality":low_coherence and stable_majority},
        "interpretation":"USER_DEFINED_OPERATIONAL_CRITERION_NOT_OBJECTIVE_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=64)
    ap.add_argument("--p",type=float,default=0.7)
    ap.add_argument("--gamma",type=float,default=0.05)
    ap.add_argument("--coherence-tolerance",type=float,default=0.05)
    ap.add_argument("--majority-error-tolerance",type=float,default=0.05)
    args=ap.parse_args()
    print(json.dumps(analyze(args.n,args.p,args.gamma,args.coherence_tolerance,
                             args.majority_error_tolerance),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
