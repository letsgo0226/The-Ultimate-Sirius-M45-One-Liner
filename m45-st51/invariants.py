#!/usr/bin/env python3
"""ST51: explicitly scoped observational invariants and counterexamples."""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load(name,relpath):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parent.parent/relpath)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def near(a,b,tol=1e-10):
    return math.isclose(a,b,rel_tol=tol,abs_tol=tol)

def report(n=32,p=0.7,gamma_a=0.0,gamma_b=1.0):
    st49=load("st49","m45-st49/decoherence.py")
    st50=load("st50","m45-st50/micro_macro.py")
    # Validate n, p and both gammas before comparison.
    st50.binomial(n,p)
    a=st50.analyze(n,p,gamma_a)
    b=st50.analyze(n,p,gamma_b)
    rho_a=st49.dephase(st49.state(p),gamma_a)
    rho_b=st49.dephase(st49.state(p),gamma_b)
    invariants={
        "trace_one":near(sum(rho_a[i][i] for i in range(2)),1) and near(sum(rho_b[i][i] for i in range(2)),1),
        "z_plus_probability":near(a["single_qubit"]["Z"]["plus"],b["single_qubit"]["Z"]["plus"]),
        "macro_count_distribution":all(near(x,y) for x,y in zip(a["macro"]["k_distribution"],b["macro"]["k_distribution"])),
        "macro_mean":near(a["macro"]["expected_plus_count"],b["macro"]["expected_plus_count"]),
        "macro_variance":near(a["macro"]["variance_plus_count"],b["macro"]["variance_plus_count"]),
    }
    noninvariants={
        "x_plus_probability_changed":not near(a["single_qubit"]["X"]["plus"],b["single_qubit"]["X"]["plus"]),
        "coherence_changed":not near(a["single_qubit"]["coherence_l1"],b["single_qubit"]["coherence_l1"]),
    }
    return {"protocol":"M45-ST51-OBSERVATIONAL-INVARIANTS-v1",
            "scope":"IDENTICAL_INDEPENDENT_QUBITS_Z_BASIS_DEPHASING",
            "parameters":{"n":n,"p":p,"gamma_a":gamma_a,"gamma_b":gamma_b},
            "invariants":invariants,"context_dependent":noninvariants,
            "x_plus":[a["single_qubit"]["X"]["plus"],b["single_qubit"]["X"]["plus"]],
            "z_plus":[a["single_qubit"]["Z"]["plus"],b["single_qubit"]["Z"]["plus"]],
            "majority_plus":[a["macro"]["majority_plus"],b["macro"]["majority_plus"]],
            "interpretation":"MODEL_COMPARISON_NOT_UNIVERSAL_PHYSICAL_INVARIANCE"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=32)
    ap.add_argument("--p",type=float,default=0.7)
    ap.add_argument("--gamma-a",type=float,default=0)
    ap.add_argument("--gamma-b",type=float,default=1)
    args=ap.parse_args()
    print(json.dumps(report(args.n,args.p,args.gamma_a,args.gamma_b),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
