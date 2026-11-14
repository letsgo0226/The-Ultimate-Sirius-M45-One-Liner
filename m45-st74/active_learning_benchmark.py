#!/usr/bin/env python3
"""ST74: paired, reproducible comparison of experimental allocation policies.

All policies in a replication consume prefixes of the SAME independent
calibration and science Bernoulli streams (common random numbers).
This reduces comparison noise without conflating the two streams.
Confidence intervals are simultaneously valid across adaptive looks
using the conservative ST73 anytime union bound.
"""
import argparse
import importlib.util
import json
import math
import random
import statistics
from pathlib import Path

POLICIES=("balanced","science_heavy","adaptive")

def load(name,relative):
    path=Path(__file__).resolve().parent.parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def validate(theta,flip,budget,batch,alpha,seed,replications,target_width):
    st73=load("st73","m45-st73/adaptive_design.py")
    st73.validate(theta,flip,budget,batch,alpha,seed,target_width)
    if isinstance(replications,bool) or not isinstance(replications,int) or not 1<=replications<=500:
        raise ValueError("replications must be integer in [1,500]")
    if budget*replications>2000000:
        raise ValueError("budget*replications must not exceed 2e6")
    return st73

def choose(policy,kq,nq,kr,nr):
    if policy=="balanced":
        return "calibration" if nq<=nr else "science"
    if policy=="science_heavy":
        return "calibration" if nq*3<=nr else "science"
    if policy=="adaptive":
        # Reuse the stage-73 sensitivity heuristic unchanged.
        return load("st73","m45-st73/adaptive_design.py").priority(kq,nq,kr,nr)
    raise ValueError("unknown policy")

def run_policy(policy,cal_stream,sci_stream,batch,budget,log_factor,target_width,theta,st73):
    nq=nr=batch
    kq=sum(cal_stream[:nq])
    kr=sum(sci_stream[:nr])
    while True:
        ci=st73.interval(kq,nq,kr,nr,log_factor)
        width=ci[1]-ci[0]
        if width<=target_width or nq+nr>=budget:
            break
        if policy=="balanced":
            stream="calibration" if nq<=nr else "science"
        elif policy=="science_heavy":
            stream="calibration" if nq*3<=nr else "science"
        elif policy=="adaptive":
            stream=st73.priority(kq,nq,kr,nr)
        else:
            raise ValueError("unknown policy")
        take=min(batch,budget-nq-nr)
        if stream=="calibration":
            kq+=sum(cal_stream[nq:nq+take])
            nq+=take
        else:
            kr+=sum(sci_stream[nr:nr+take])
            nr+=take
    qhat=kq/nq
    rhat=kr/nr
    estimate=None if qhat>=.5 else math.asin(2*st73.clip((rhat-qhat)/(1-2*qhat))-1)
    return {"trials_used":nq+nr,"calibration_trials":nq,"science_trials":nr,
            "theta_estimate":estimate,"theta_interval":ci,"interval_width":width,
            "covers_truth":ci[0]<=theta<=ci[1],
            "target_reached":width<=target_width}

def analyze(theta=.3,flip=.15,budget=1200,batch=50,alpha=.05,seed=2026,
            replications=100,target_width=.65):
    st73=validate(theta,flip,budget,batch,alpha,seed,replications,target_width)
    st69=load("st69","m45-st69/observer_estimation.py")
    p=st69.analyze(theta,1,seed)["shared_born_probability"]
    r=flip+(1-2*flip)*p
    log_factor=math.log(4*budget/alpha)
    results={name:[] for name in POLICIES}
    for trial in range(replications):
        rng_q=random.Random((seed+2*trial*0x9E3779B97F4A7C15)%(2**64))
        rng_r=random.Random((seed+(2*trial+1)*0x9E3779B97F4A7C15)%(2**64))
        # A policy cannot consume >budget observations from either stream.
        cal=[rng_q.random()<flip for _ in range(budget)]
        sci=[rng_r.random()<r for _ in range(budget)]
        for policy in POLICIES:
            results[policy].append(run_policy(policy,cal,sci,batch,budget,
                                              log_factor,target_width,theta,st73))
    summaries={}
    for name,rows in results.items():
        errors=[(row["theta_estimate"]-theta) for row in rows if row["theta_estimate"] is not None]
        summaries[name]={
            "mean_trials_used":statistics.mean(row["trials_used"] for row in rows),
            "mean_interval_width":statistics.mean(row["interval_width"] for row in rows),
            "empirical_coverage":statistics.mean(row["covers_truth"] for row in rows),
            "target_reached_fraction":statistics.mean(row["target_reached"] for row in rows),
            "theta_rmse":math.sqrt(statistics.mean(e*e for e in errors)) if errors else None,
            "theta_bias":statistics.mean(errors) if errors else None,
            "point_estimate_defined_fraction":len(errors)/replications,
            "mean_calibration_trials":statistics.mean(row["calibration_trials"] for row in rows),
            "mean_science_trials":statistics.mean(row["science_trials"] for row in rows)
        }
    paired={}
    for name in ("science_heavy","adaptive"):
        paired[name+"_minus_balanced"]={
            "mean_trial_difference":statistics.mean(a["trials_used"]-b["trials_used"]
                                                      for a,b in zip(results[name],results["balanced"])),
            "mean_width_difference":statistics.mean(a["interval_width"]-b["interval_width"]
                                                      for a,b in zip(results[name],results["balanced"]))
        }
    return {
        "protocol":"M45-ST74-RELATIONAL-ACTIVE-LEARNING-BENCHMARK-v1",
        "parameters":{"theta_true_simulation_only":theta,
                      "true_detector_flip_simulation_only":flip,
                      "budget_per_policy_per_replication":budget,
                      "batch":batch,"alpha":alpha,"seed":seed,
                      "replications":replications,"target_width":target_width},
        "ideal_born_probability":p,
        "observed_science_probability":r,
        "policy_summaries":summaries,
        "paired_comparisons":paired,
        "simultaneous_coverage_lower_bound_per_replication":1-alpha,
        "interpretation":"MONTE_CARLO_POLICY_COMPARISON_NOT_A_PROOF_OF_OPTIMALITY"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--theta",type=float,default=.3)
    parser.add_argument("--flip",type=float,default=.15)
    parser.add_argument("--budget",type=int,default=1200)
    parser.add_argument("--batch",type=int,default=50)
    parser.add_argument("--alpha",type=float,default=.05)
    parser.add_argument("--seed",type=int,default=2026)
    parser.add_argument("--replications",type=int,default=100)
    parser.add_argument("--target-width",type=float,default=.65)
    a=parser.parse_args()
    print(json.dumps(analyze(a.theta,a.flip,a.budget,a.batch,a.alpha,a.seed,
                             a.replications,a.target_width),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
