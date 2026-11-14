#!/usr/bin/env python3
"""ST77: held-out posterior predictive checks for model criticism.

Training data update ST76's finite-grid posterior. Independent held-out
reference/science counts are checked against exact posterior predictive
binomial-mixture distributions. Tail areas are descriptive Bayesian model
criticism scores, NOT uniformly calibrated frequentist p-values.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

ACTIONS=("reference_zero","reference_one","science")

def load_st76():
    path=Path(__file__).resolve().parent.parent/"m45-st76"/"bayesian_model_selection.py"
    spec=importlib.util.spec_from_file_location("st76",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,q01,q10,train_shots,holdout_shots,drift,alpha,seed,prior):
    st76=load_st76()
    st76.validate(theta,q01,q10,0,seed,prior,train_shots,train_shots)
    if isinstance(holdout_shots,bool) or not isinstance(holdout_shots,int) or not 1<=holdout_shots<=200:
        raise ValueError("holdout_shots must be integer in [1,200]")
    if isinstance(drift,bool) or not isinstance(drift,(float,int)) or not math.isfinite(drift) or not -.5<=drift<=.5:
        raise ValueError("science_drift must be finite in [-0.5,0.5]")
    if isinstance(alpha,bool) or not isinstance(alpha,(float,int)) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be in (0,1)")
    return st76

def binomial_pmf(k,n,p):
    if not 0<=p<=1 or not 0<=k<=n:
        raise ValueError("invalid binomial arguments")
    if p==0:
        return 1. if k==0 else 0.
    if p==1:
        return 1. if k==n else 0.
    return math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
                    +k*math.log(p)+(n-k)*math.log1p(-p))

def predictive_pmf(hypotheses,weights,action,n):
    probabilities=[0.]*(n+1)
    for h,w in zip(hypotheses,weights):
        if w==0:
            continue
        p=load_probability(h,action)
        for k in range(n+1):
            probabilities[k]+=w*binomial_pmf(k,n,p)
    total=sum(probabilities)
    return [v/total for v in probabilities]

def load_probability(h,action):
    _,p,q01,q10=h
    if action=="reference_zero":
        return q01
    if action=="reference_one":
        return 1-q10
    if action=="science":
        return q01+(1-q01-q10)*p
    raise ValueError("unknown action")

def predictive_check(pmf,observed):
    mean=sum(k*prob for k,prob in enumerate(pmf))
    variance=sum((k-mean)**2*prob for k,prob in enumerate(pmf))
    discrepancy=abs(observed-mean)
    tail=sum(prob for k,prob in enumerate(pmf)
             if abs(k-mean)>=discrepancy-1e-10)
    return {"predictive_mean_count":mean,
            "predictive_sd_count":math.sqrt(variance),
            "two_sided_predictive_tail_area":min(1.,tail),
            "observed_discrepancy_from_mean":discrepancy}

def analyze(theta=.3,q01=.05,q10=.2,train_shots=40,holdout_shots=30,
            science_drift=.0,alpha=.05,seed=2026,prior_symmetric=.5):
    st76=validate(theta,q01,q10,train_shots,holdout_shots,science_drift,
                  alpha,seed,prior_symmetric)
    p=st76.st69_probability(theta,seed)
    true_probs={"reference_zero":q01,"reference_one":1-q10,
                "science":q01+(1-q01-q10)*p}
    holdout_probs=dict(true_probs)
    holdout_probs["science"]=min(1.,max(0.,true_probs["science"]+science_drift))
    rng_train=random.Random(seed)
    rng_test=random.Random(seed^0x9E3779B97F4A7C15)
    train=[]
    heldout={}
    for action in ACTIONS:
        k=sum(rng_train.random()<true_probs[action] for _ in range(train_shots))
        train.append((action,k,train_shots))
        heldout[action]=sum(rng_test.random()<holdout_probs[action]
                            for _ in range(holdout_shots))
    hypotheses=st76.grid()
    weights=st76.posterior(hypotheses,train,prior_symmetric)
    checks={}
    for action in ACTIONS:
        pmf=predictive_pmf(hypotheses,weights,action,holdout_shots)
        check=predictive_check(pmf,heldout[action])
        check["heldout_successes"]=heldout[action]
        check["heldout_trials"]=holdout_shots
        check["exploratory_flag"]=check["two_sided_predictive_tail_area"]<alpha/len(ACTIONS)
        checks[action]=check
    return {
        "protocol":"M45-ST77-HELDOUT-POSTERIOR-PREDICTIVE-CRITICISM-v1",
        "true_parameters_simulation_only":{"theta":theta,"q01":q01,"q10":q10,
                                            "science_holdout_drift":science_drift},
        "training_observations":[{"action":a,"successes":k,"trials":n} for a,k,n in train],
        "posterior_symmetric":st76.model_probability(hypotheses,weights),
        "posterior_asymmetric":1-st76.model_probability(hypotheses,weights),
        "holdout_checks":checks,
        "flag_threshold_per_action":alpha/len(ACTIONS),
        "any_exploratory_flag":any(v["exploratory_flag"] for v in checks.values()),
        "interpretation":"HELDOUT_POSTERIOR_PREDICTIVE_DIAGNOSTIC_NOT_A_FREQUENTIST_SIGNIFICANCE_TEST"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--q01",type=float,default=.05)
    ap.add_argument("--q10",type=float,default=.2)
    ap.add_argument("--train-shots",type=int,default=40)
    ap.add_argument("--holdout-shots",type=int,default=30)
    ap.add_argument("--science-drift",type=float,default=0.)
    ap.add_argument("--alpha",type=float,default=.05)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--prior-symmetric",type=float,default=.5)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.q01,a.q10,a.train_shots,
                             a.holdout_shots,a.science_drift,a.alpha,
                             a.seed,a.prior_symmetric),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
