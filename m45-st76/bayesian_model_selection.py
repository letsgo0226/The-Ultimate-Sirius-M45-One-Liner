#!/usr/bin/env python3
"""ST76: finite-grid Bayesian model selection and active reference design.

Competing readout models:
 S: symmetric flips q01=q10=q.
 A: asymmetric flips q01 != q10 allowed.
Reference-zero, reference-one, and science outcomes all have binary likelihoods.
Model evidence is calculated by exact discrete-grid enumeration, not MCMC.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def st69_probability(theta,seed):
    path=Path(__file__).resolve().parent.parent/"m45-st69"/"observer_estimation.py"
    spec=importlib.util.spec_from_file_location("st69",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.analyze(theta,1,seed)["shared_born_probability"]

def validate(theta,q01,q10,steps,seed,alpha_prior,science_shots,cal_shots):
    if isinstance(theta,bool) or not isinstance(theta,(float,int)) or not math.isfinite(theta) or not -math.pi/2<theta<math.pi/2:
        raise ValueError("theta must be in (-pi/2,pi/2)")
    if any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or not 0<=x<.5 for x in (q01,q10)):
        raise ValueError("true flip rates must be in [0,0.5)")
    if isinstance(steps,bool) or not isinstance(steps,int) or not 0<=steps<=50:
        raise ValueError("steps must be integer in [0,50]")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")
    if isinstance(alpha_prior,bool) or not isinstance(alpha_prior,(int,float)) or not math.isfinite(alpha_prior) or not 0<alpha_prior<1:
        raise ValueError("model prior must be in (0,1)")
    for n in (science_shots,cal_shots):
        if isinstance(n,bool) or not isinstance(n,int) or not 0<=n<=1000:
            raise ValueError("initial shots must be in [0,1000]")

def grid():
    # Midpoint grid avoids zero/one likelihoods and supports q01,q10<0.5.
    rates=(.025,.075,.125,.175,.225,.275,.325,.375,.425,.475)
    probabilities=(.05,.15,.25,.35,.45,.55,.65,.75,.85,.95)
    hypotheses=[]
    for p in probabilities:
        for q in rates:
            hypotheses.append(("symmetric",p,q,q))
        for q01 in rates:
            for q10 in rates:
                hypotheses.append(("asymmetric",p,q01,q10))
    return hypotheses

def outcome_probability(h,action):
    _,p,q01,q10=h
    if action=="reference_zero":
        return q01
    if action=="reference_one":
        return 1-q10
    if action=="science":
        return q01+(1-q01-q10)*p
    raise ValueError("unknown action")

def normalize_log_weights(log_weights):
    maximum=max(log_weights)
    weights=[math.exp(x-maximum) for x in log_weights]
    total=sum(weights)
    return [x/total for x in weights]

def posterior(hypotheses,observations,prior_symmetric=.5):
    # Model priors are equal by default, and normalized within each model
    # so that the larger asymmetric hypothesis space has no automatic advantage.
    ns=sum(h[0]=="symmetric" for h in hypotheses)
    na=len(hypotheses)-ns
    logs=[]
    for h in hypotheses:
        mass=prior_symmetric/ns if h[0]=="symmetric" else (1-prior_symmetric)/na
        ll=math.log(mass)
        for action,k,n in observations:
            prob=outcome_probability(h,action)
            ll+=k*math.log(prob)+(n-k)*math.log1p(-prob)
        logs.append(ll)
    return normalize_log_weights(logs)

def model_probability(hypotheses,weights):
    return sum(w for h,w in zip(hypotheses,weights) if h[0]=="symmetric")

def binary_entropy(p):
    return 0 if p<=0 or p>=1 else -p*math.log(p)- (1-p)*math.log1p(-p)

def expected_model_information(hypotheses,weights,action):
    # I(model; next binary outcome | data, action), exact for finite grid.
    ps=model_probability(hypotheses,weights)
    pa=1-ps
    if min(ps,pa)<1e-15:
        return 0.
    predicted=sum(w*outcome_probability(h,action) for h,w in zip(hypotheses,weights))
    pred_s=sum(w*outcome_probability(h,action) for h,w in zip(hypotheses,weights)
               if h[0]=="symmetric")/ps
    pred_a=sum(w*outcome_probability(h,action) for h,w in zip(hypotheses,weights)
               if h[0]=="asymmetric")/pa
    # I(M;Y)=H(Y)-E_M H(Y|M)
    return max(0.,binary_entropy(predicted)-ps*binary_entropy(pred_s)-pa*binary_entropy(pred_a))

def analyze(theta=.3,q01=.05,q10=.2,steps=12,seed=2026,
            prior_symmetric=.5,science_shots=20,cal_shots=10):
    validate(theta,q01,q10,steps,seed,prior_symmetric,science_shots,cal_shots)
    p=st69_probability(theta,seed)
    hypotheses=grid()
    actions=("reference_zero","reference_one","science")
    rng=random.Random(seed)
    actual={"reference_zero":q01,"reference_one":1-q10,
            "science":q01+(1-q01-q10)*p}
    observations=[]
    for action,n in (("reference_zero",cal_shots),("reference_one",cal_shots),
                     ("science",science_shots)):
        if n:
            observations.append((action,sum(rng.random()<actual[action] for _ in range(n)),n))
    trace=[]
    for step in range(steps+1):
        weights=posterior(hypotheses,observations,prior_symmetric)
        prob_sym=model_probability(hypotheses,weights)
        gains={a:expected_model_information(hypotheses,weights,a) for a in actions}
        trace.append({"step":step,"posterior_symmetric":prob_sym,
                      "posterior_asymmetric":1-prob_sym,
                      "expected_model_information_nats":gains,
                      "selected_next_action":None if step==steps else max(actions,key=lambda a:gains[a])})
        if step==steps:
            break
        action=trace[-1]["selected_next_action"]
        observations.append((action,int(rng.random()<actual[action]),1))
    # Posterior mean p is a model-averaged phase estimate, not a confidence interval.
    mean_p=sum(w*h[1] for h,w in zip(hypotheses,weights))
    return {
        "protocol":"M45-ST76-BAYESIAN-MODEL-SELECTION-v1",
        "true_parameters_simulation_only":{"theta":theta,"q01":q01,"q10":q10},
        "true_model_simulation_only":"symmetric" if q01==q10 else "asymmetric",
        "ideal_born_probability":p,
        "model_prior_symmetric":prior_symmetric,
        "grid_hypothesis_count":len(hypotheses),
        "initial_reference_shots_each":cal_shots,
        "initial_science_shots":science_shots,
        "adaptive_steps":steps,
        "observations":[{"action":a,"successes":k,"trials":n} for a,k,n in observations],
        "posterior_symmetric":prob_sym,
        "posterior_asymmetric":1-prob_sym,
        "posterior_mean_theta":math.asin(2*mean_p-1),
        "trace":trace,
        "interpretation":"DISCRETE_MODEL_EVIDENCE_AND_ONE_STEP_MODEL_INFORMATION; NOT_A_PROOF_OF_TRUE_MODEL"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--q01",type=float,default=.05)
    ap.add_argument("--q10",type=float,default=.2)
    ap.add_argument("--steps",type=int,default=12)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--prior-symmetric",type=float,default=.5)
    ap.add_argument("--science-shots",type=int,default=20)
    ap.add_argument("--cal-shots",type=int,default=10)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.q01,a.q10,a.steps,a.seed,
                             a.prior_symmetric,a.science_shots,a.cal_shots),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
