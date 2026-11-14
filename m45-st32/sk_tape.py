#!/usr/bin/env python3
"""M45-ST/32: deterministic SK-to-tape encoding and bounded, replayable reductions.

This is a tape-encoded interpreter, NOT a fixed-delta single-tape TM.
"""
import argparse
import hashlib
import json
from pathlib import Path

ALPHABET = {"@": 0, "S": 1, "K": 2}
INVERSE = {v: k for k, v in ALPHABET.items()}
MAX_SIZE = 10000

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def parse(src):
    if not isinstance(src, str) or not 1 <= len(src) <= 300:
        raise ValueError("expression must contain 1..300 symbols")
    i = 0
    def term(depth=0):
        nonlocal i
        if depth > 300 or i >= len(src):
            raise ValueError("invalid prefix expression")
        symbol = src[i]
        i += 1
        if symbol in ("S", "K"):
            return symbol
        if symbol != "@":
            raise ValueError("invalid symbol")
        return (term(depth + 1), term(depth + 1))
    tree = term()
    if i != len(src):
        raise ValueError("trailing symbols")
    return tree

def encode(tree):
    if isinstance(tree, str):
        return tree
    return "@" + encode(tree[0]) + encode(tree[1])

def tape_encode(src):
    parse(src)
    return [ALPHABET[c] for c in src]

def tape_decode(cells):
    if not isinstance(cells, list) or not 1 <= len(cells) <= MAX_SIZE:
        raise ValueError("invalid tape length")
    if any(type(v) is not int or v not in INVERSE for v in cells):
        raise ValueError("invalid tape alphabet")
    src = "".join(INVERSE[v] for v in cells)
    parse(src)
    return src

def reduce_once(tree):
    if isinstance(tree, str):
        return None
    args = []
    head = tree
    while isinstance(head, tuple):
        args.insert(0, head[1])
        head = head[0]
    if head == "K" and len(args) >= 2:
        result, rest = args[0], args[2:]
    elif head == "S" and len(args) >= 3:
        result, rest = ((args[0], args[2]), (args[1], args[2])), args[3:]
    else:
        left = reduce_once(tree[0])
        if left is not None:
            return (left, tree[1])
        right = reduce_once(tree[1])
        return (tree[0], right) if right is not None else None
    for arg in rest:
        result = (result, arg)
    return result

def advance(snapshot, budget):
    if type(budget) is not int or not 0 <= budget <= 100:
        raise ValueError("budget must be 0..100")
    src = tape_decode(snapshot["tape"])
    if snapshot["steps"] < 0:
        raise ValueError("invalid step counter")
    tree = parse(src)
    initial_hash = digest(snapshot)
    trace = []
    for _ in range(budget):
        next_tree = reduce_once(tree)
        if next_tree is None:
            break
        next_src = encode(next_tree)
        if len(next_src) > MAX_SIZE:
            break
        trace.append({"before": encode(tree), "after": next_src})
        tree = next_tree
    next_src = encode(tree)
    result = {"tape": [ALPHABET[c] for c in next_src], "steps": snapshot["steps"] + len(trace)}
    status = "NORMAL" if reduce_once(tree) is None else "PAUSED"
    record = {"protocol": "M45-ST32", "before_sha256": initial_hash,
              "after_sha256": digest(result), "trace": trace, "status": status}
    record["record_sha256"] = digest(record)
    return result, record

def replay(initial, records):
    current = initial
    for rec in records:
        nxt, expected = advance(current, len(rec["trace"]))
        if rec != expected:
            raise ValueError("invalid reduction record")
        current = nxt
    return current

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--expression", default="@@@SKKS")
    p.add_argument("--steps", type=int, default=30)
    p.add_argument("--out", default="m45-st32-certificate.json")
    args = p.parse_args()
    start = {"tape": tape_encode(args.expression), "steps": 0}
    end, record = advance(start, args.steps)
    certificate = {"genesis": start, "records": [record], "final": end}
    assert replay(start, [record]) == end
    Path(args.out).write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + "\n")
    print(canonical({"status": record["status"], "steps": end["steps"], "expression": tape_decode(end["tape"])}))

if __name__ == "__main__":
    main()
