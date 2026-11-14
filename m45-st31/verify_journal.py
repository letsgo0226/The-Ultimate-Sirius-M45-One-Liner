#!/usr/bin/env python3
"""Replay and authenticate the complete ST30 journal from a pinned genesis state."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ST30 = ROOT.parent / "m45-st30"
TABLE = json.loads((ROOT.parent / "m45-st28" / "delta.json").read_text())

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()

def genesis():
    return {"table_hash": digest(TABLE), "state": TABLE["start"], "head": 0,
            "steps": 0, "generation": 0,
            "cells": {"0": "1", "1": "1", "2": "1"}}

def replay(records):
    state = genesis()
    for index, record in enumerate(records, 1):
        if record["generation"] != index:
            raise ValueError("generation mismatch")
        if record["previous_state_sha256"] != digest(state):
            raise ValueError("previous state hash mismatch")
        if record["table_sha256"] != digest(TABLE):
            raise ValueError("transition table hash mismatch")
        claimed = dict(record)
        signature = claimed.pop("record_sha256")
        if digest(claimed) != signature:
            raise ValueError("record digest mismatch")
        for step in record["transitions"]:
            q, head = state["state"], state["head"]
            symbol = state["cells"].get(str(head), "_")
            rule = TABLE["transitions"].get(q, {}).get(symbol)
            if rule is None:
                raise ValueError("undefined transition")
            write, move, next_state = rule
            expected = {"q": q, "h": head, "read": symbol, "write": write,
                        "move": move, "next": next_state}
            if step != expected:
                raise ValueError("invalid step in journal")
            if write == "_":
                state["cells"].pop(str(head), None)
            else:
                state["cells"][str(head)] = write
            state["head"] += {"L": -1, "R": 1, "N": 0}[move]
            state["state"] = next_state
            state["steps"] += 1
        state["generation"] += 1
        if record["next_state_sha256"] != digest(state):
            raise ValueError("next state hash mismatch")
        status = "HALTED" if state["state"] in TABLE["halt"] else "PAUSED"
        if record["status"] != status:
            raise ValueError("status mismatch")
        if status == "PAUSED" and not record["transitions"]:
            raise ValueError("empty nonhalting batch")
    return state

def verify_files():
    raw = (ST30 / "journal.jsonl").read_text(encoding="utf-8")
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    actual = replay(records)
    saved = json.loads((ST30 / "state.json").read_text(encoding="utf-8"))
    if actual != saved:
        raise ValueError("saved state differs from replay")
    return {"status": "PASS", "generations": len(records), "steps": actual["steps"],
            "state_sha256": digest(actual)}

if __name__ == "__main__":
    print(canonical(verify_files()))
