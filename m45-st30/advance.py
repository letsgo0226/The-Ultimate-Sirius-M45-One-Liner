#!/usr/bin/env python3
"""M45-ST/30 persistent, auditable finite-step unary TM (GitHub Actions ready)."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DELTA = json.loads((ROOT.parent / "m45-st28" / "delta.json").read_text())
STATE = ROOT / "state.json"
JOURNAL = ROOT / "journal.jsonl"

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def validate(state):
    if state["table_hash"] != sha(DELTA):
        raise ValueError("transition table changed")
    if state["state"] not in DELTA["transitions"] and state["state"] not in DELTA["halt"]:
        raise ValueError("unknown state")
    if not isinstance(state["head"], int) or not isinstance(state["steps"], int) or state["steps"] < 0:
        raise ValueError("invalid head or steps")
    cells = state["cells"]
    if not isinstance(cells, dict) or len(cells) > 20000:
        raise ValueError("invalid tape size")
    for pos, value in cells.items():
        if str(int(pos)) != pos or value != "1":
            raise ValueError("invalid tape cell")

def execute(state, limit):
    validate(state)
    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError("batch limit must be 1..1000")
    current = json.loads(canonical(state))
    before_hash = sha(current)
    transitions = []
    for _ in range(limit):
        if current["state"] in DELTA["halt"]:
            break
        head = current["head"]
        read = current["cells"].get(str(head), "_")
        rule = DELTA["transitions"].get(current["state"], {}).get(read)
        if rule is None:
            raise ValueError("undefined transition")
        write, move, next_state = rule
        transitions.append({"q": current["state"], "h": head, "read": read, "write": write,
                            "move": move, "next": next_state})
        if write == "_":
            current["cells"].pop(str(head), None)
        else:
            current["cells"][str(head)] = write
        current["head"] += {"L": -1, "R": 1, "N": 0}[move]
        current["state"] = next_state
        current["steps"] += 1
    current["generation"] += 1
    record = {"generation": current["generation"], "previous_state_sha256": before_hash,
              "next_state_sha256": sha(current), "table_sha256": sha(DELTA),
              "transitions": transitions,
              "status": "HALTED" if current["state"] in DELTA["halt"] else "PAUSED"}
    record["record_sha256"] = sha(record)
    return current, record

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    state = json.loads(STATE.read_text())
    validate(state)
    if args.verify_only:
        print("VALID", sha(state))
        return
    next_state, record = execute(state, args.steps)
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(canonical(record) + "\n")
    STATE.write_text(json.dumps(next_state, indent=2, ensure_ascii=False) + "\n")
    print(canonical({"status": record["status"], "generation": next_state["generation"],
                     "steps": next_state["steps"], "record_sha256": record["record_sha256"]}))

if __name__ == "__main__":
    main()
