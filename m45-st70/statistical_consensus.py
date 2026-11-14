#!/usr/bin/env python3
"""ST70: multi-observer relational consensus with finite-sample confidence sets.

Independent observers measure the same transported relational event in the
ST69 finite-Z2 model. Symmetric known detector flips are corrected and
simultaneous Hoeffding intervals yield a conservative consensus intersection.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load_st69():
    path=Path(__file__).resolve().parent.parent/"m45-st69"/"observer_estimation.py"
    spec=importlib.util.spec_from_file_location("st69_observer_estimation",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,observers,shots,flip,alpha,seed):
    if isinstance(theta,bool) or not isinstance(theta,(int,float)) or not math.isfinite(theta) or not -math.pi/2<theta<math.pi/2:
        raise ValueError("theta must be in (-pi/2,pi/2)")
    if isinstance(observers,bool) or not isinstance(observers,int) or not 2<=observers<=100:
        raise ValueError("observers must be integer in [2,100]")
    if isinstance(shots,bool) or not isinstance(shots,int) or not 1<=shots<=100000:
        raise ValueError("shots must be integer in [1,100000]")
    if isinstance(flip,bool) or not isinstance(flip,(int,float)) or not math.isfinite(flip) or not 0<=flip<0.5:
        raise ValueError("flip must be in [0,0.5)")
    if isinstance(alpha,bool) or not isinstance(alpha,(int,float)) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be in (0,1)")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")
    if observers*shots>1000000:
        raise ValueError("observers*shots must not exceed 1000000")

def clip01(p):
    return max(0.0,min(1.0,p))

def theta_from_p(p):
    return math.asin(max(-1.0,min(1.0,2*p-1)))

def p_interval(successes,shots,flip,epsilon):
    # Bound the observed Bernoulli parameter, then invert the known flip.
    observed=successes/shots
    qlo=clip01(observed-epsilon)
    qhi=clip01(observed+epsilon)
    factor=1-2*flip
    return (clip01((qlo-flip)/factor),clip01((qhi-flip)/factor))

def analyze(theta=0.3,observers=5,shots=1000,flip=0.05,alpha=0.05,seed=2026):
    validate(theta,observers,shots,flip,alpha,seed)
    st69=load_st69()
    # ST69 provides the exact transported Born probability.
    baseline=st69.analyze(theta,1,seed)
    p=baseline["shared_born_probability"]
    observed_p=flip+(1-2*flip)*p
    epsilon=math.sqrt(math.log(2*observers/alpha)/(2*shots))
    reports=[]
    intervals=[]
    total=0
    for i in range(observers):
        rng=random.Random((seed+i*0x9E3779B97F4A7C15)%(2**64))
        k=sum(rng.random()<observed_p for _ in range(shots))
        total+=k
        p_low,p_high=p_interval(k,shots,flip,epsilon)
        low,high=theta_from_p(p_low),theta_from_p(p_high)
        intervals.append((low,high))
        corrected=clip01((k/shots-flip)/(1-2*flip))
        reports.append({
            "observer":i+1,"successes":k,
            "raw_sample_probability":k/shots,
            "noise_corrected_theta_estimate":theta_from_p(corrected),
            "simultaneous_theta_interval":[low,high],
            "interval_contains_true_theta":low<=theta<=high
        })
    lower=max(x[0] for x in intervals)
    upper=min(x[1] for x in intervals)
    intersection=[lower,upper] if lower<=upper else None
    pooled_corrected=clip01(((total/(observers*shots))-flip)/(1-2*flip))
    estimates=[r["noise_corrected_theta_estimate"] for r in reports]
    return {
        "protocol":"M45-ST70-RELATIONAL-STATISTICAL-CONSENSUS-v1",
        "parameters":{"theta_true":theta,"observers":observers,"shots_each":shots,
                      "known_symmetric_flip_probability":flip,
                      "familywise_alpha":alpha,"seed":seed},
        "shared_ideal_born_probability":p,
        "shared_noisy_born_probability":observed_p,
        "simultaneous_hoeffding_observed_probability_radius":epsilon,
        "observer_reports":reports,
        "consensus_interval_intersection":intersection,
        "consensus_interval_contains_true_theta":None if intersection is None else lower<=theta<=upper,
        "all_observer_intervals_contain_true_theta":all(r["interval_contains_true_theta"] for r in reports),
        "pooled_theta_estimate":theta_from_p(pooled_corrected),
        "estimate_range":max(estimates)-min(estimates),
        "simultaneous_coverage_guarantee_at_least":1-alpha,
        "interpretation":"PROBABILISTIC_COVERAGE_NOT_CERTAIN_CONSENSUS_OR_IDENTICAL_OUTCOMES"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=0.3)
    ap.add_argument("--observers",type=int,default=5)
    ap.add_argument("--shots",type=int,default=1000)
    ap.add_argument("--flip",type=float,default=0.05)
    ap.add_argument("--alpha",type=float,default=0.05)
    ap.add_argument("--seed",type=int,default=2026)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.observers,a.shots,a.flip,a.alpha,a.seed),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
