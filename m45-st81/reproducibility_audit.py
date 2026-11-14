#!/usr/bin/env python3
"""ST81: reproducible cross-stage audit, no network and no writes by default."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
CASES=(
 ("ST64","m45-st64/frame_switch.py",[]),
 ("ST68","m45-st68/quantum_metrology.py",[]),
 ("ST69","m45-st69/observer_estimation.py",["--shots","20","--seed","17"]),
 ("ST73","m45-st73/adaptive_design.py",["--budget","120","--batch","10","--seed","17"]),
 ("ST74","m45-st74/active_learning_benchmark.py",["--budget","120","--batch","10","--replications","3","--seed","17"]),
 ("ST75","m45-st75/information_gain.py",["--budget","120","--batch","10","--replications","3","--seed","17"]),
 ("ST76","m45-st76/bayesian_model_selection.py",["--steps","2","--cal-shots","4","--science-shots","4","--seed","17"]),
 ("ST77","m45-st77/predictive_criticism.py",["--train-shots","4","--holdout-shots","5","--seed","17"]),
 ("ST78","m45-st78/model_expansion.py",["--shots","4","--seed","17"]),
 ("ST79","m45-st79/model_evolution.py",["--shots","4","--seed","17"]),
 ("ST80","m45-st80/discovery_benchmark.py",["--replicates","2","--shots","4","--seed","17"]),
)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def run_once(path,args,timeout=90):
    command=[sys.executable,str(ROOT/path),*args]
    env=os.environ.copy()
    env["PYTHONHASHSEED"]="0"
    completed=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=timeout,
                             env=env,check=False)
    if completed.returncode:
        raise RuntimeError(f"exit={completed.returncode}: {completed.stderr.decode('utf-8','replace')[-800:]}")
    data=json.loads(completed.stdout)
    if not isinstance(data,dict) or not data.get("protocol"):
        raise ValueError("stage did not return protocol JSON object")
    canonical=json.dumps(data,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    return data,digest(canonical)

def audit(repeat=True,run_tests=False):
    results=[]
    for stage,path,args in CASES:
        file=ROOT/path
        entry={"stage":stage,"source_path":path,"source_sha256":digest(file.read_bytes()),
               "command_arguments":args}
        try:
            output,sha=run_once(path,args)
            entry.update(status="pass",protocol=output["protocol"],output_sha256=sha)
            if repeat:
                _,sha2=run_once(path,args)
                entry["repeat_output_sha256"]=sha2
                entry["reproducible"]=sha==sha2
                if sha!=sha2:
                    entry["status"]="fail"
        except Exception as exc:
            entry.update(status="fail",error=f"{type(exc).__name__}: {exc}")
        results.append(entry)
    if run_tests:
        for stage,path,_ in CASES:
            folder=str(Path(path).parent)
            p=subprocess.run([sys.executable,"-m","unittest","discover","-s",folder,"-p","test_*.py"],
                             cwd=ROOT,capture_output=True,timeout=120,check=False)
            results.append({"stage":stage+"-TESTS","status":"pass" if p.returncode==0 else "fail",
                            "exit_code":p.returncode,
                            "stderr_tail":p.stderr.decode("utf-8","replace")[-1200:]})
    return {"protocol":"M45-ST81-REPRODUCIBILITY-AUDIT-v1",
            "python_version":sys.version.split()[0],
            "stage_results":results,
            "passed":sum(x["status"]=="pass" for x in results),
            "failed":sum(x["status"]=="fail" for x in results),
            "all_passed":all(x["status"]=="pass" for x in results),
            "interpretation":"EXECUTION_AND_DETERMINISM_AUDIT_NOT_SCIENTIFIC_VALIDATION"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--no-repeat",action="store_true")
    ap.add_argument("--run-tests",action="store_true")
    ap.add_argument("--output",default=None,
                    help="Optional path to save JSON; by default only stdout")
    a=ap.parse_args()
    report=audit(not a.no_repeat,a.run_tests)
    payload=json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n"
    if a.output:
        Path(a.output).write_text(payload,encoding="utf-8")
    print(payload,end="")
    sys.exit(0 if report["all_passed"] else 1)
if __name__=="__main__":main()
