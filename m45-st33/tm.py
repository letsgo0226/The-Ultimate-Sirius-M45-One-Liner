#!/usr/bin/env python3
"""ST33: execute an explicit finite transition table, not a Python SK reducer."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DELTA = json.loads((ROOT / "delta.json").read_text(encoding="utf-8"))

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()

def simulate(expression="@@KSK", limit=100):
    if not isinstance(expression, str) or len(expression) > 1000 or any(x not in "@SK" for x in expression):
        raise ValueError("invalid input alphabet")
    if type(limit) is not int or not 0 <= limit <= 1000:
        raise ValueError("invalid step budget")
    cells = {i: v for i, v in enumerate(expression)}
    head, state, trace = 0, DELTA["start"], []
    for _ in range(limit):
        if state in DELTA["halt"]:
            break
        read = cells.get(head, "_")
        transition = DELTA["transitions"].get(state, {}).get(read)
        if transition is None:
            return {"status":"REJECT", "state":state, "head":head, "steps":len(trace),
                    "trace":trace, "table_sha256":digest(DELTA)}
        write, movement, nxt = transition
        trace.append({"state":state,"head":head,"read":read,"write":write,
                      "move":movement,"next":nxt})
        if write == "_":
            cells.pop(head, None)
        else:
            cells[head] = write
        head += {"L":-1,"R":1,"N":0}[movement]
        state = nxt
    return {"status":"HALT" if state in DELTA["halt"] else "PAUSE",
            "state":state,"head":head,"steps":len(trace),
            "tape":"".join(cells.get(i, "_") for i in range(max(cells,default=-1)+1)),
            "trace":trace,"table_sha256":digest(DELTA)}

def verify(expression, certificate):
    expected = simulate(expression, certificate.get("steps", -1))
    return expected == certificate and certificate.get("table_sha256") == digest(DELTA)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--expression", default="@@KSK")
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--out", default="m45-st33-certificate.json")
    a = p.parse_args()
    result = simulate(a.expression, a.steps)
    Path(a.out).write_text(json.dumps({"input":a.expression,"result":result},ensure_ascii=False,indent=2)+"\n")
    print(canonical({"status":result["status"],"steps":result["steps"],"tape":result.get("tape")}))
