#!/usr/bin/env python3
"""ST79: bounded, auditable model evolution with independent locked testing.

Train -> propose predeclared mutation families -> validation-select ->
locked-test selected candidate exactly once. No test-set feedback loop.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

ACTIONS=("reference_zero","reference_one","science")
PHASES=("early","late")

def st78():
    path=Path(__file__).resolve().parent.parent/"m45-st78"/"model_expansion.py"
    spec=importlib.util.spec_from_file_location("st78",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def candidates():
    ps=(.15,.35,.55,.75,.95)
    qs=(.05,.15,.25,.35,.45)
    ds=(-.3,-.15,0.,.15,.3)
    base=[(p,q0,q1,0.,0.,0.) for p in ps for q0 in qs for q1 in qs]
    return {
        "stationary":base,
        "science_drift":[(p,q0,q1,d,0.,0.) for p,q0,q1,_,_,_ in base for d in ds],
        "reference_zero_drift":[(p,q0,q1,0.,d,0.) for p,q0,q1,_,_,_ in base for d in ds],
        "reference_one_drift":[(p,q0,q1,0.,0.,d) for p,q0,q1,_,_,_ in base for d in ds]
    }

def probability(h,action,phase):
    p,q0,q1,ds,d0,d1=h
    late=phase=="late"
    if action=="reference_zero":
        v=q0+(d0 if late else 0.)
    elif action=="reference_one":
        v=1-q1+(d1 if late else 0.)
    elif action=="science":
        v=q0+(1-q0-q1)*p+(ds if late else 0.)
    else:
        raise ValueError("unknown action")
    return min(1-1e-12,max(1e-12,v))

def train_posterior(grid,observations):
    logs=[]
    for h in grid:
        ll=0.
        for action,phase,k,n in observations:
            p=probability(h,action,phase)
            ll+=k*math.log(p)+(n-k)*math.log1p(-p)
        logs.append(ll)
    maximum=max(logs)
    w=[math.exp(v-maximum) for v in logs]
    total=sum(w)
    return [v/total for v in w]

def score(grid,weights,observations):
    # Marginal per-observation log predictive score; frozen posterior.
    total=0.
    count=0
    for action,phase,k,n in observations:
        p=sum(w*probability(h,action,phase) for h,w in zip(grid,weights))
        total+=k*math.log(p)+(n-k)*math.log1p(-p)
        count+=n
    return total/count

def simulate(rng,p,q0,q1,late_drift,shots):
    obs=[]
    for phase in PHASES:
        for action in ACTIONS:
            if action=="reference_zero":
                prob=q0
            elif action=="reference_one":
                prob=1-q1
            else:
                prob=q0+(1-q0-q1)*p+(late_drift if phase=="late" else 0.)
            prob=max(0.,min(1.,prob))
            obs.append((action,phase,sum(rng.random()<prob for _ in range(shots)),shots))
    return obs

def analyze(theta=.3,q01=.05,q10=.2,late_science_drift=.3,shots=30,
            seed=2026,complexity_penalty=.002):
    mod=st78()
    mod.validate(theta,q01,q10,late_science_drift,shots,seed)
    if (isinstance(complexity_penalty,bool) or
        not isinstance(complexity_penalty,(float,int)) or
        not math.isfinite(complexity_penalty) or
        not 0<=complexity_penalty<=1):
        raise ValueError("complexity_penalty must be finite in [0,1]")
    p=mod.st76().st69_probability(theta,seed)
    train=simulate(random.Random(seed),p,q01,q10,late_science_drift,shots)
    validation=simulate(random.Random(seed^0x9E3779B97F4A7C15),p,q01,q10,late_science_drift,shots)
    locked=simulate(random.Random(seed^0xD1B54A32D192ED03),p,q01,q10,late_science_drift,shots)
    grids=candidates()
    audit=[]
    weights={}
    val={}
    for name,g in grids.items():
        weights[name]=train_posterior(g,train)
        raw=score(g,weights[name],validation)
        # Complexity penalty is a declared heuristic, not a BIC/AIC theorem.
        penalty=complexity_penalty*(name!="stationary")
        val[name]=raw-penalty
        audit.append({"candidate":name,"grid_size":len(g),
                      "validation_log_score":raw,"complexity_penalty":penalty,
                      "selection_score":val[name]})
    winner=max(grids,key=lambda name:val[name])
    for entry in audit:
        entry["selected"]=entry["candidate"]==winner
    # Locked test is evaluated ONLY for the validation-selected model.
    locked_score=score(grids[winner],weights[winner],locked)
    return {
        "protocol":"M45-ST79-BOUNDED-SCIENTIFIC-MODEL-EVOLUTION-v1",
        "simulation_truth":{"theta":theta,"q01":q01,"q10":q10,
                            "late_science_drift":late_science_drift},
        "candidate_generation_rule":"STATIONARY_PLUS_ONE_PREDECLARED_LATE_ACTION_DRIFT",
        "validation_selection_audit":audit,
        "selected_model":winner,
        "locked_test_selected_model_mean_log_score":locked_score,
        "data_split_trials_each":shots*len(ACTIONS)*len(PHASES),
        "test_used_for_selection":False,
        "interpretation":"BOUNDED_AUDITABLE_MODEL_MUTATION; NO_AUTONOMOUS_OPEN_ENDED_DISCOVERY"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--q01",type=float,default=.05)
    ap.add_argument("--q10",type=float,default=.2)
    ap.add_argument("--late-science-drift",type=float,default=.3)
    ap.add_argument("--shots",type=int,default=30)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--complexity-penalty",type=float,default=.002)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.q01,a.q10,a.late_science_drift,
                             a.shots,a.seed,a.complexity_penalty),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
