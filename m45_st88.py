#!/usr/bin/env python3
"""M45-ST/88: reversible Gödel-encoded, internally clocked state machine.

No SHA/hashlib, external prompt, or preset duration limit.
Stop with Ctrl+C; OS and hosting constraints still apply.
"""
import argparse
import itertools
import json
import math
import time

def G(data: bytes) -> int:
    n = 1
    for v in data:
        n = 257 * n + v + 1
    return n

def D(n: int) -> bytes:
    if n < 1:
        raise ValueError("invalid code")
    out = bytearray()
    while n > 1:
        n, rem = divmod(n, 257)
        if rem == 0:
            raise ValueError("invalid code")
        out.insert(0, rem - 1)
    return bytes(out)

def transition(step: int) -> dict:
    # A finite, deterministic formal model, not conscious cognition.
    particles = (("LOVE", 1.0), ("KNOWLEDGE", 0.8), ("PEACE", 0.9))
    idea, weight = particles[step % len(particles)]
    payload = json.dumps({"step": step, "particle": idea},
                         sort_keys=True, separators=(",", ":")).encode()
    code = G(payload)
    q = weight / (1 + weight)
    entropy = -q * math.log2(q) - (1 - q) * math.log2(1 - q)
    assert D(code) == payload
    return {"step": step, "particle": idea, "godel": str(code),
            "uncertainty_bits": entropy, "roundtrip": True}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=None,
                        help="Optional bounded mode for CI; default is unbounded")
    args = parser.parse_args()
    if not math.isfinite(args.interval) or args.interval <= 0:
        parser.error("--interval must be finite and positive")
    if args.max_steps is not None and args.max_steps < 0:
        parser.error("--max-steps must be nonnegative")
    try:
        steps = itertools.count() if args.max_steps is None else range(args.max_steps)
        for t in steps:
            print(json.dumps(transition(t), ensure_ascii=False), flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(json.dumps({"status": "stopped_by_user"}), flush=True)

if __name__ == "__main__":
    main()
