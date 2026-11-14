#!/usr/bin/env python3
"""M45-ST/28: deterministic, bounded, replayable fixed-table Turing machine."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TABLE = json.loads((ROOT / "delta.json").read_text(encoding="utf-8"))
BLANK = "_"

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()

def run(tape, limit=100, initial=None):
    if not isinstance(limit, int) or not 0 <= limit <= 100000:
        raise ValueError("limit must be in [0,100000]")
    if initial is None:
        if not isinstance(tape, str) or len(tape) > 10000 or any(c not in "1" for c in tape):
            raise ValueError("input must be a unary string of up to 10000 ones")
        cells = {i: c for i, c in enumerate(tape)}
        state, head, steps = TABLE["start"], 0, 0
    else:
        cells = {int(k): v for k, v in initial["cells"].items()}
        state, head, steps = initial["state"], initial["head"], initial["steps"]
    transitions = TABLE["transitions"]
    trace = []
    for _ in range(limit):
        if state in TABLE["halt"]:
            break
        symbol = cells.get(head, BLANK)
        rule = transitions.get(state, {}).get(symbol)
        if rule is None:
            raise ValueError(f"missing transition: {state}/{symbol}")
        new_symbol, movement, next_state = rule
        before = {"state": state, "head": head, "read": symbol, "step": steps}
        if new_symbol == BLANK:
            cells.pop(head, None)
        else:
            cells[head] = new_symbol
        head += {"L": -1, "R": 1, "N": 0}[movement]
        state = next_state
        steps += 1
        trace.append({**before, "write": new_symbol, "move": movement, "next": next_state})
    status = "HALTED" if state in TABLE["halt"] else "PAUSED"
    snapshot = {"state": state, "head": head, "steps": steps, "cells": {str(k): v for k, v in sorted(cells.items())}}
    certificate = {"protocol": "M45-ST28", "table_sha256": digest(TABLE), "status": status,
                   "snapshot": snapshot, "trace": trace}
    certificate["certificate_sha256"] = digest(certificate)
    return certificate

def verify(cert):
    if cert["table_sha256"] != digest(TABLE):
        return False
    claimed = dict(cert)
    sig = claimed.pop("certificate_sha256", None)
    if sig != digest(claimed):
        return False
    # Trace chain validation checks each step against the fixed transition table.
    for record in cert["trace"]:
        rule = TABLE["transitions"].get(record["state"], {}).get(record["read"])
        if rule != [record["write"], record["move"], record["next"]]:
            return False
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tape", default="111")
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--resume", default=None)
    p.add_argument("--verify", default=None)
    p.add_argument("--out", default="certificate.json")
    a = p.parse_args()
    if a.verify:
        cert = json.loads(Path(a.verify).read_text())
        if not verify(cert):
            raise SystemExit("FAIL")
        print("PASS")
        return
    previous = json.loads(Path(a.resume).read_text())["snapshot"] if a.resume else None
    cert = run(a.tape, a.steps, previous)
    Path(a.out).write_text(json.dumps(cert, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": cert["status"], "steps": cert["snapshot"]["steps"], "certificate": a.out}))

if __name__ == "__main__":
    main()
