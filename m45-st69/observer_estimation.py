#!/usr/bin/env python3
"""ST69: finite-sample observer agreement in a Z2 relational quantum toy model.

Two observers use consistently transported A/B relational measurements.
Their independent Bernoulli samples share the same Born probability, but
sample estimates differ. The parameter is identifiable on [-pi/2,pi/2].
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parent.parent/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,shots,seed):
    if not isinstance(theta,(float,int)) or isinstance(theta,bool) or not math.isfinite(theta) or abs(theta)>=math.pi/2:
        raise ValueError("theta must be finite and strictly between -pi/2 and pi/2")
    if isinstance(shots,bool) or not isinstance(shots,int) or not 1<=shots<=1000000:
        raise ValueError("shots must be an integer in [1,1000000]")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be a nonnegative 64-bit integer")

def estimate(k,n):
    # Exact p(theta)=(1+sin theta)/2; clip finite-sample boundary values.
    p=k/n
    return math.asin(max(-1.0,min(1.0,2*p-1)))

def analyze(theta=0.3,shots=1000,seed=2026):
    validate(theta,shots,seed)
    st64=load("st64","m45-st64/frame_switch.py")
    st68=load("st68","m45-st68/quantum_metrology.py")
    # Two u-sectors arranged so B=C event has p=(1+sin theta)/2.
    initial=st64.normalize(("1","1j","1","-1j"))
    encoded_a=st68.encode(initial,theta)
    encoded_b=st64.switch_a_to_b(encoded_a)
    p_a=st64.probability_equal_b_c(encoded_a,"A")
    p_b=st64.probability_equal_b_c(encoded_b,"B")
    expected=(1+math.sin(theta))/2
    error=max(abs(p_a-p_b),abs(p_a-expected))
    if error>1e-10:raise AssertionError("observer probability covariance failed")
    rng_a=random.Random(seed)
    rng_b=random.Random(seed^0x9E3779B97F4A7C15)
    k_a=sum(rng_a.random()<p_a for _ in range(shots))
    k_b=sum(rng_b.random()<p_b for _ in range(shots))
    e_a=estimate(k_a,shots)
    e_b=estimate(k_b,shots)
    qfi=st68.qfi(initial)
    # This transported binary projector saturates F_C=F_Q=1 in the interior.
    cfi=(math.cos(theta)**2)/(4*p_a*(1-p_a))
    if abs(cfi-qfi)>1e-10:raise AssertionError("Fisher information mismatch")
    sigma=1/math.sqrt(shots*cfi)
    return {
        "protocol":"M45-ST69-RELATIONAL-OBSERVER-ESTIMATION-v1",
        "theta_true":theta,"shots_per_observer":shots,"seed":seed,
        "shared_born_probability":p_a,
        "a_observer":{"successes":k_a,"sample_probability":k_a/shots,
                      "theta_estimate":e_a,"absolute_error":abs(e_a-theta)},
        "b_observer":{"successes":k_b,"sample_probability":k_b/shots,
                      "theta_estimate":e_b,"absolute_error":abs(e_b-theta)},
        "estimate_disagreement":abs(e_a-e_b),
        "asymptotic_standard_error_per_observer":sigma,
        "quantum_fisher_information":qfi,
        "classical_fisher_information":cfi,
        "max_born_covariance_error":error,
        "interpretation":"IDENTICAL_PREDICTIONS_DO_NOT_IMPLY_IDENTICAL_FINITE_SAMPLE_ESTIMATES"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=0.3)
    ap.add_argument("--shots",type=int,default=1000)
    ap.add_argument("--seed",type=int,default=2026)
    args=ap.parse_args()
    print(json.dumps(analyze(args.theta,args.shots,args.seed),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
