#!/usr/bin/env python3
"""ST71: observer disagreement from mismatched detector calibrations.

The shared ST69 relational Born probability is frame-covariant. Each
observer has a true binary-flip probability and an independently assumed
calibration. Hoeffding intervals have coverage guarantees only when
the assumed calibration matches the true detector model.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load(name,relative):
    path=Path(__file__).resolve().parent.parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def parse_rates(value):
    try:
        rates=[float(s.strip()) for s in value.split(",")]
    except (ValueError,AttributeError) as exc:
        raise ValueError("rates must be comma-separated finite numbers") from exc
    if not rates or any(not math.isfinite(q) or not 0<=q<0.5 for q in rates):
        raise ValueError("each flip rate must lie in [0,0.5)")
    return rates

def validate(theta,shots,alpha,seed,actual,assumed):
    if isinstance(theta,bool) or not isinstance(theta,(int,float)) or not math.isfinite(theta) or not -math.pi/2<theta<math.pi/2:
        raise ValueError("theta must be in (-pi/2,pi/2)")
    if isinstance(shots,bool) or not isinstance(shots,int) or not 1<=shots<=100000:
        raise ValueError("shots must be integer in [1,100000]")
    if isinstance(alpha,bool) or not isinstance(alpha,(int,float)) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be in (0,1)")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")
    if len(actual)!=len(assumed) or not 2<=len(actual)<=100 or len(actual)*shots>1000000:
        raise ValueError("rate arrays must have equal length 2..100 and <=1e6 total shots")
    if any(not isinstance(q,(int,float)) or isinstance(q,bool) or not math.isfinite(q) or not 0<=q<0.5 for q in actual+assumed):
        raise ValueError("flip rates must be finite in [0,0.5)")

def clip01(x):
    return max(0.0,min(1.0,x))

def theta_of_p(p):
    return math.asin(max(-1.0,min(1.0,2*p-1)))

def corrected_probability(r,q):
    return clip01((r-q)/(1-2*q))

def confidence_interval(k,n,q,epsilon):
    raw=k/n
    lo=corrected_probability(clip01(raw-epsilon),q)
    hi=corrected_probability(clip01(raw+epsilon),q)
    return [theta_of_p(lo),theta_of_p(hi)]

def analyze(theta=0.3,shots=1000,alpha=0.05,seed=2026,
            actual=(0.02,0.08,0.15,0.04),
            assumed=(0.02,0.08,0.02,0.04)):
    actual=list(actual)
    assumed=list(assumed)
    validate(theta,shots,alpha,seed,actual,assumed)
    st69=load("st69","m45-st69/observer_estimation.py")
    p=st69.analyze(theta,1,seed)["shared_born_probability"]
    m=len(actual)
    eps=math.sqrt(math.log(2*m/alpha)/(2*shots))
    reports=[]
    intervals=[]
    true_intervals=[]
    for i,(q_true,q_assumed) in enumerate(zip(actual,assumed)):
        r_true=q_true+(1-2*q_true)*p
        rng=random.Random((seed+i*0x9E3779B97F4A7C15)%(2**64))
        k=sum(rng.random()<r_true for _ in range(shots))
        observed=k/shots
        corrected=corrected_probability(observed,q_assumed)
        interval=confidence_interval(k,shots,q_assumed,eps)
        oracle_interval=confidence_interval(k,shots,q_true,eps)
        intervals.append(interval)
        true_intervals.append(oracle_interval)
        reports.append({
            "observer":i+1,
            "true_flip_rate_simulation_only":q_true,
            "assumed_flip_rate":q_assumed,
            "calibration_correct":q_true==q_assumed,
            "successes":k,
            "observed_probability":observed,
            "estimated_theta":theta_of_p(corrected),
            "assumption_based_interval":interval,
            "assumption_based_interval_contains_true_theta":interval[0]<=theta<=interval[1],
            "oracle_calibrated_interval":oracle_interval
        })
    def intersect(intervals):
        lo=max(a for a,b in intervals)
        hi=min(b for a,b in intervals)
        return [lo,hi] if lo<=hi else None
    # Model-independent check: each pair of raw observed rates should agree
    # only if the detectors have the same true flip rate, so this is an
    # intentionally conservative descriptive heterogeneity flag, not a
    # universal model-disagreement detector.
    spread=max(r["estimated_theta"] for r in reports)-min(r["estimated_theta"] for r in reports)
    return {
        "protocol":"M45-ST71-RELATIONAL-MODEL-DISAGREEMENT-v1",
        "theta_true_simulation_only":theta,
        "shared_ideal_born_probability":p,
        "shots_per_observer":shots,
        "familywise_alpha":alpha,
        "simultaneous_hoeffding_radius_observed_scale":eps,
        "observers":reports,
        "assumption_based_consensus_intersection":intersect(intervals),
        "oracle_calibrated_consensus_intersection":intersect(true_intervals),
        "assumption_based_all_cover":all(r["assumption_based_interval_contains_true_theta"] for r in reports),
        "oracle_calibrated_all_cover":all(a<=theta<=b for a,b in true_intervals),
        "assumption_based_estimate_spread":spread,
        "oracle_simultaneous_coverage_at_least":1-alpha,
        "assumption_based_coverage_guaranteed":all(q==r for q,r in zip(actual,assumed)),
        "interpretation":"COMMON_QUANTUM_PREDICTIONS_CAN_COEXIST_WITH_CALIBRATION_BIAS; COVERAGE_REQUIRES_VALID_ASSUMPTIONS"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=0.3)
    ap.add_argument("--shots",type=int,default=1000)
    ap.add_argument("--alpha",type=float,default=0.05)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--actual-flips",default="0.02,0.08,0.15,0.04")
    ap.add_argument("--assumed-flips",default="0.02,0.08,0.02,0.04")
    args=ap.parse_args()
    print(json.dumps(analyze(args.theta,args.shots,args.alpha,args.seed,
                             parse_rates(args.actual_flips),parse_rates(args.assumed_flips)),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
