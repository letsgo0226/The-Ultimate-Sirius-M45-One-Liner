#!/usr/bin/env python3
"""ST80: reproducible paired benchmark of fixed vs bounded-evolving models.

Each replicate creates independent training, validation and locked test
datasets. Model selection sees validation only. Evaluation sees locked test
only once. Compare paired per-observation predictive log scores.
"""
import argparse
import importlib.util
import json
import math
import random
import statistics
from pathlib import Path

SCENARIOS={
    "stationary":0.,
    "positive_science_drift":.3,
    "negative_science_drift":-.3,
    "off_grid_science_drift":.22,
}

def st79():
    path=Path(__file__).resolve().parent.parent/"m45-st79"/"model_evolution.py"
    spec=importlib.util.spec_from_file_location("st79",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(replicates,shots,seed,penalty):
    if isinstance(replicates,bool) or not isinstance(replicates,int) or not 2<=replicates<=100:
        raise ValueError("replicates must be integer in [2,100]")
    if isinstance(shots,bool) or not isinstance(shots,int) or not 1<=shots<=200:
        raise ValueError("shots must be integer in [1,200]")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")
    if isinstance(penalty,bool) or not isinstance(penalty,(int,float)) or not math.isfinite(penalty) or not 0<=penalty<=1:
        raise ValueError("penalty must be finite in [0,1]")

def summarize(values):
    mean=statistics.mean(values)
    sd=statistics.stdev(values)
    se=sd/math.sqrt(len(values))
    return {"mean":mean,"sample_sd":sd,
            "normal_approx_95pct_ci":[mean-1.96*se,mean+1.96*se]}

def benchmark(replicates=12,shots=20,seed=2026,complexity_penalty=.002):
    validate(replicates,shots,seed,complexity_penalty)
    mod=st79()
    grids=mod.candidates()
    p=(1+math.sin(.3))/2
    q01,q10=.05,.2
    out={}
    for scenario_index,(scenario,drift) in enumerate(SCENARIOS.items()):
        rows=[]
        for i in range(replicates):
            # Separate deterministic RNGs for the three splits and scenario.
            root=(seed+scenario_index*1000003+i*10007)%(2**64)
            train=mod.simulate(random.Random(root),p,q01,q10,drift,shots)
            valid=mod.simulate(random.Random(root^0x9E3779B97F4A7C15),p,q01,q10,drift,shots)
            locked=mod.simulate(random.Random(root^0xD1B54A32D192ED03),p,q01,q10,drift,shots)
            weights={}
            validation_scores={}
            for name,g in grids.items():
                weights[name]=mod.train_posterior(g,train)
                raw=mod.score(g,weights[name],valid)
                validation_scores[name]=raw-(complexity_penalty if name!="stationary" else 0.)
            winner=max(validation_scores,key=validation_scores.get)
            fixed_score=mod.score(grids["stationary"],weights["stationary"],locked)
            selected_score=mod.score(grids[winner],weights[winner],locked)
            rows.append({"replicate":i,"selected":winner,
                         "fixed_locked_log_score":fixed_score,
                         "evolved_locked_log_score":selected_score,
                         "paired_gain":selected_score-fixed_score})
        gains=[r["paired_gain"] for r in rows]
        counts={name:sum(r["selected"]==name for r in rows) for name in grids}
        out[scenario]={
            "true_science_drift_simulation_only":drift,
            "mean_fixed_locked_log_score":statistics.mean(r["fixed_locked_log_score"] for r in rows),
            "mean_evolved_locked_log_score":statistics.mean(r["evolved_locked_log_score"] for r in rows),
            "paired_gain_summary":summarize(gains),
            "fraction_evolved_beats_fixed_on_locked_test":sum(v>0 for v in gains)/replicates,
            "selected_model_counts":counts,
            "stationary_selection_fraction":counts["stationary"]/replicates,
            "replicate_results":rows
        }
    return {
        "protocol":"M45-ST80-SCIENTIFIC-DISCOVERY-BENCHMARK-v1",
        "parameters":{"replicates_per_scenario":replicates,"shots_per_action_phase_split":shots,
                      "seed":seed,"complexity_penalty":complexity_penalty},
        "scenario_results":out,
        "interpretation":"PAIRED_OUT_OF_SAMPLE_PREDICTIVE_BENCHMARK; NO_PROOF_OF_DISCOVERY_OR_SUPERIORITY"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--replicates",type=int,default=12)
    ap.add_argument("--shots",type=int,default=20)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--complexity-penalty",type=float,default=.002)
    a=ap.parse_args()
    print(json.dumps(benchmark(a.replicates,a.shots,a.seed,a.complexity_penalty),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
