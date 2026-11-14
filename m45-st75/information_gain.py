#!/usr/bin/env python3
"""ST75: one-step Bayesian expected-risk experimental allocation benchmark.

Decision rule uses a delta-method approximation to posterior theta variance
and exact Beta-Bernoulli expected variance reduction for each observation
stream. Confidence intervals remain frequentist, from ST73, independent
of the Bayesian decision heuristic.
"""
import argparse
import importlib.util
import json
import math
import random
import statistics
from pathlib import Path

def load(name,relative):
    path=Path(__file__).resolve().parent.parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def beta_stats(k,n,a,b):
    x=a+k
    y=b+n-k
    s=x+y
    return x/s, x*y/(s*s*(s+1)),s

def expected_variance_reduction(k,n,a,b,batch):
    # Law of total variance: Var(E[parameter | future batch])
    # = current Beta variance * batch/(posterior concentration + batch).
    _,v,s=beta_stats(k,n,a,b)
    return v*batch/(s+batch)

def theta_risk_and_gains(kq,nq,kr,nr,batch):
    # q and r are modeled as independent Beta posteriors for decisions.
    # q prior Beta(1,19) encodes a preference for low flip rates;
    # r prior Beta(1,1). The q posterior is not truncated to q<1/2,
    # so the delta-method calculation is an approximation.
    q,vq,_=beta_stats(kq,nq,1,19)
    r,vr,_=beta_stats(kr,nr,1,1)
    q=min(q,.49)
    denom=1-2*q
    p=max(.000001,min(.999999,(r-q)/denom))
    # d theta/d p = 1/sqrt(p*(1-p)); p=(r-q)/(1-2q).
    dtheta_dp=1/math.sqrt(p*(1-p))
    dr=dtheta_dp/denom
    dq=dtheta_dp*(2*r-1)/(denom*denom)
    risk=dr*dr*vr+dq*dq*vq
    gain_cal=dq*dq*expected_variance_reduction(kq,nq,1,19,batch)
    gain_sci=dr*dr*expected_variance_reduction(kr,nr,1,1,batch)
    return risk,gain_cal,gain_sci

def choose(kq,nq,kr,nr,batch):
    _,cal,sci=theta_risk_and_gains(kq,nq,kr,nr,batch)
    return "calibration" if cal>sci else "science"

def run_information_gain(cal,sci,batch,budget,log_factor,target_width,theta,st73):
    nq=nr=batch
    kq=sum(cal[:batch])
    kr=sum(sci[:batch])
    decisions={"calibration":0,"science":0}
    while True:
        ci=st73.interval(kq,nq,kr,nr,log_factor)
        width=ci[1]-ci[0]
        if width<=target_width or nq+nr>=budget:
            break
        take=min(batch,budget-nq-nr)
        stream=choose(kq,nq,kr,nr,take)
        decisions[stream]+=1
        if stream=="calibration":
            kq+=sum(cal[nq:nq+take])
            nq+=take
        else:
            kr+=sum(sci[nr:nr+take])
            nr+=take
    qhat=kq/nq
    rhat=kr/nr
    point=None if qhat>=.5 else math.asin(2*st73.clip((rhat-qhat)/(1-2*qhat))-1)
    return {"trials_used":nq+nr,"calibration_trials":nq,"science_trials":nr,
            "theta_estimate":point,"theta_interval":ci,"interval_width":width,
            "covers_truth":ci[0]<=theta<=ci[1],"target_reached":width<=target_width,
            "decision_counts":decisions}

def analyze(theta=.3,flip=.15,budget=1200,batch=50,alpha=.05,
            seed=2026,replications=100,target_width=.65):
    st74=load("st74","m45-st74/active_learning_benchmark.py")
    st73=st74.validate(theta,flip,budget,batch,alpha,seed,replications,target_width)
    st69=load("st69","m45-st69/observer_estimation.py")
    p=st69.analyze(theta,1,seed)["shared_born_probability"]
    r=flip+(1-2*flip)*p
    log_factor=math.log(4*budget/alpha)
    names=("balanced","science_heavy","adaptive","expected_risk")
    results={name:[] for name in names}
    for trial in range(replications):
        rng_q=random.Random((seed+2*trial*0x9E3779B97F4A7C15)%(2**64))
        rng_r=random.Random((seed+(2*trial+1)*0x9E3779B97F4A7C15)%(2**64))
        cal=[rng_q.random()<flip for _ in range(budget)]
        sci=[rng_r.random()<r for _ in range(budget)]
        for name in names:
            if name=="expected_risk":
                row=run_information_gain(cal,sci,batch,budget,log_factor,target_width,theta,st73)
            else:
                row=st74.run_policy(name,cal,sci,batch,budget,log_factor,target_width,theta,st73)
            results[name].append(row)
    summary={}
    for name,rows in results.items():
        errors=[row["theta_estimate"]-theta for row in rows if row["theta_estimate"] is not None]
        summary[name]={
            "mean_trials":statistics.mean(row["trials_used"] for row in rows),
            "mean_interval_width":statistics.mean(row["interval_width"] for row in rows),
            "empirical_coverage":statistics.mean(row["covers_truth"] for row in rows),
            "target_reached_fraction":statistics.mean(row["target_reached"] for row in rows),
            "theta_rmse":math.sqrt(statistics.mean(e*e for e in errors)) if errors else None,
            "theta_bias":statistics.mean(errors) if errors else None,
            "defined_estimate_fraction":len(errors)/replications,
            "mean_calibration_trials":statistics.mean(row["calibration_trials"] for row in rows),
            "mean_science_trials":statistics.mean(row["science_trials"] for row in rows)
        }
    comparison={}
    for other in ("balanced","science_heavy","adaptive"):
        comparison["expected_risk_minus_"+other]={
            "mean_trial_difference":statistics.mean(a["trials_used"]-b["trials_used"]
                 for a,b in zip(results["expected_risk"],results[other])),
            "mean_interval_width_difference":statistics.mean(a["interval_width"]-b["interval_width"]
                 for a,b in zip(results["expected_risk"],results[other]))
        }
    return {
        "protocol":"M45-ST75-EXPECTED-RISK-ACTIVE-LEARNING-v1",
        "parameters":{"theta_true_simulation_only":theta,
                      "true_detector_flip_simulation_only":flip,
                      "budget":budget,"batch":batch,"alpha":alpha,
                      "seed":seed,"replications":replications,"target_width":target_width},
        "policy_summaries":summary,
        "paired_comparisons":comparison,
        "frequentist_simultaneous_coverage_lower_bound_per_replication":1-alpha,
        "decision_objective":"ONE_STEP_APPROXIMATE_EXPECTED_POSTERIOR_THETA_VARIANCE_REDUCTION",
        "interpretation":"APPROXIMATE_BAYESIAN_DESIGN_WITH_SEPARATE_FREQUENTIST_INTERVALS; NOT_PROVEN_OPTIMAL"
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
