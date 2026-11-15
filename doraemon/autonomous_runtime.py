#!/usr/bin/env python3
"""Deterministic, bounded-resource autonomous state transitions; not consciousness."""
import argparse
import hashlib
import json
import os
import signal
import time
from pathlib import Path

STOP = False
PARTICLES = ("LOVE", "KNOWLEDGE", "PEACE")

def stop(*_):
    global STOP
    STOP = True

def godel(data: bytes) -> int:
    value = 1
    for byte in data:
        value = value * 257 + byte + 1
    return value

def run(path: Path, interval: float, max_steps: int | None):
    if interval <= 0 or (max_steps is not None and max_steps < 1):
        raise ValueError("interval must be positive and max-steps >= 1")
    path.parent.mkdir(parents=True, exist_ok=True)
    step = 0
    if path.exists():
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    step = max(step, int(json.loads(line)["step"]) + 1)
    with path.open("a", encoding="utf-8") as stream:
        completed = 0
        while not STOP and (max_steps is None or completed < max_steps):
            particle = PARTICLES[step % len(PARTICLES)]
            code = godel(particle.encode())
            digest = hashlib.sha256(f"{step}:{code}".encode()).hexdigest()
            record = {"step": step, "particle": particle, "godel": str(code),
                      "digest": digest, "autonomous_transition": True,
                      "consciousness_proven": False}
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
            print(json.dumps(record), flush=True)
            step += 1
            completed += 1
            if max_steps is None or completed < max_steps:
                time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=Path("data/doraemon.jsonl"))
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=None,
                        help="Optional CI/testing bound; omitted for continuous operation")
    args = parser.parse_args()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    run(args.state, args.interval, args.max_steps)
