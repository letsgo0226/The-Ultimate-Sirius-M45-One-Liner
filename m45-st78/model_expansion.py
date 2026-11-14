#!/usr/bin/env python3
"""ST78: predeclared open-world model expansion with a locked evaluation set.

Candidate stationary and science-drift models are compared by predictive
log score on an independent validation set. A separate locked test set
assesses the selected candidate without further model selection.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load_st76():
    path=Path(__file__).resolve().parent.parent/"m45-st76"/"bayesian_model_selection.py"
    spec=importlib.util.spec_from_file_location("st76",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,q01,q10,drift,shots,seed):
    st76=load_st76()
    st76.validate(theta,q01,q10,0,seed,.5,shots,shots)
    if isinstance(drift,bool) or not isinstance(drift,(float,int)) or not math.isfinite(drift) or not -.5<=drift<=.5:
        raise ValueError("drift must be finite in [-.5,.5]")
    if isinstance(shots,bool) or not isinstance(shots,int) or not 1<=shots<=200:
        raise ValueError("shots must be integer in [1,200]")
    return st76

def grid():
    # Model expansion is explicit and finite; no unbounded self-generated code.
    # Each candidate has one common latent p and detector rates.
    ps=(.15,.35,.55,.75,.95)
    rates=(.05,.15,.25,.35,.45)
    deltas=(-.3,-.15,0.,.15,.3)
    stationary=[(p,q01,q10,0.) for p in ps for q01 in rates for q10 in rates]
    drifting=[(p,q01,q10,d) for p in ps for q01 in rates
              for q10 in rates for d in deltas]
    return {"stationary":stationary,"science_drift":drifting}

def probability(h,action,phase):
    p,q01,q10,delta=h
    if action=="reference_zero":
        return q01
    if action=="reference_one":
        return 1-q10
    if action=="science":
        value=q01+(1-q01-q10)*p
        return min(1-1e-12,max(1e-12,value+(delta if phase=="late" else 0)))
    raise ValueError("unknown action")

def log_likelihood(h,observations):
    score=0.
    for action,phase,k,n in observations:
        p=probability(h,action,phase)
        score+=k*math.log(p)+(n-k)*math.log1p(-p)
    return score

def posterior(hypotheses,observations):
    logs=[log_likelihood(h,observations) for h in hypotheses]
    peak=max(logs)
    weights=[math.exp(v-peak) for v in logs]
    total=sum(weights)
    return [v/total for v in weights]

def predictive_log_score(hypotheses,weights,observations):
    # Sequentially score individual held-out outcomes using a frozen
    # training posterior mixture, without updating weights on validation/test.
    score=0.
    for action,phase,k,n in observations:
        mean=sum(w*probability(h,action,phase) for h,w in zip(hypotheses,weights))
        score+=k*math.log(mean)+(n-k)*math.log1p(-mean)
    return score/sum(n for _,_,_,n in observations)

def sample_observations(rng,true_p,q01,q10,drift,shots):
    obs=[]
    for phase in ("early","late"):
        probs={"reference_zero":q01,"reference_one":1-q10,
               "science":min(1.,max(0.,q01+(1-q01-q10)*true_p+
                                   (drift if phase=="late" else 0)))}
        for action in ("reference_zero","reference_one","science"):
            obs.append((action,phase,sum(rng.random()<probs[action] for _ in range(shots)),shots))
    return obs

def analyze(theta=.3,q01=.05,q10=.2,drift=.3,shots=30,seed=2026):
    st76=validate(theta,q01,q10,drift,shots,seed)
    p=st76.st69_probability(theta,seed)
    training=sample_observations(random.Random(seed),p,q01,q10,drift,shots)
    validation=sample_observations(random.Random(seed^0x9E3779B97F4A7C15),p,q01,q10,drift,shots)
    testing=sample_observations(random.Random(seed^0xD1B54A32D192ED03),p,q01,q10,drift,shots)
    grids=grid()
    fitted={}
    validation_scores={}
    for name,hypotheses in grids.items():
        weights=posterior(hypotheses,training)
        fitted[name]=weights
        validation_scores[name]=predictive_log_score(hypotheses,weights,validation)
    # The locked test set is never used to choose a candidate.
    selected=max(validation_scores,key=validation_scores.get)
    test_scores={name:predictive_log_score(grids[name],fitted[name],testing)
                 for name in grids}
    return {
        "protocol":"M45-ST78-OPEN-WORLD-CANDIDATE-EXPANSION-v1",
        "true_simulation_parameters":{"theta":theta,"q01":q01,"q10":q10,"late_science_drift":drift},
        "training_observations":[{"action":a,"phase":ph,"successes":k,"trials":n}
                                 for a,ph,k,n in training],
        "validation_mean_log_scores":validation_scores,
        "selected_model_by_validation":selected,
        "locked_test_mean_log_scores":test_scores,
        "locked_test_selected_model_score":test_scores[selected],
        "locked_test_score_difference_drift_minus_stationary":test_scores["science_drift"]-test_scores["stationary"],
        "candidate_hypothesis_counts":{name:len(h) for name,h in grids.items()},
        "interpretation":"PREDECLARED_FINITE_MODEL_EXPANSION_WITH_SEPARATE_VALIDATION_AND_LOCKED_TEST"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--q01",type=float,default=.05)
    ap.add_argument("--q10",type=float,default=.2)
    ap.add_argument("--drift",type=float,default=.3)
    ap.add_argument("--shots",type=int,default=30)
    ap.add_argument("--seed",type=int,default=2026)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.q01,a.q10,a.drift,a.shots,a.seed),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
