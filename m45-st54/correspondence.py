#!/usr/bin/env python3
"""ST54: commutative micro-to-macro diagram for independent qubits.

A product of identical qubits yields a binomial count distribution for
projective measurement along any signed X/Z axis. Under H/Z conjugation,
measurement axes are transported, and the macro distribution agrees exactly
up to floating point rounding in the binomial calculation.
"""
import argparse
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

def load(name,relative):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parent.parent/relative)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run(n=32,x="3/5",z="4/5",word="HZ"):
    st53=load("st53","m45-st53/transform_algebra.py")
    st50=load("st50","m45-st50/micro_macro.py")
    initial=st53.state(x,z)
    op=st53.operator(word)
    final=st53.transform(op,initial)
    cases={}
    for axis in ("X","Z"):
        transported=st53.measured_axis(op,axis)
        p_after=st53.probability(final,axis)
        p_before=st53.original_probability(initial,transported)
        # Exact rational equality of Born probabilities precedes numeric statistics.
        if p_after!=p_before:raise AssertionError("micro covariance failed")
        after=st50.binomial(n,float(p_after))
        before=st50.binomial(n,float(p_before))
        max_error=max(abs(a-b) for a,b in zip(after,before))
        cases[axis]={
            "input_frame_measurement_axis":transported,
            "exact_plus_probability":str(p_after),
            "macro_count_distribution":after,
            "maximum_absolute_distribution_error":max_error,
            "macro_covariant":max_error<=1e-12,
            "mean_plus_count":n*float(p_after),
            "variance_plus_count":n*float(p_after)*(1-float(p_after))
        }
    return {
        "protocol":"M45-ST54-MICRO-MACRO-COVARIANCE-v1",
        "assumptions":["identical independent qubits","same unitary applied to each qubit",
                       "projective X/Z measurements","binomial coarse-graining"],
        "n":n,"word":word,"initial":{"x":str(initial[0]),"z":str(initial[1])},
        "final":{"x":str(final[0]),"z":str(final[1])},
        "contexts":cases,
        "interpretation":"MATHEMATICAL_COVARIANCE_NOT_PHYSICAL_COLLAPSE_OR_UNIVERSE_CONTROL"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=32)
    ap.add_argument("--x",default="3/5")
    ap.add_argument("--z",default="4/5")
    ap.add_argument("--word",default="HZ")
    args=ap.parse_args()
    print(json.dumps(run(args.n,args.x,args.z,args.word),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
