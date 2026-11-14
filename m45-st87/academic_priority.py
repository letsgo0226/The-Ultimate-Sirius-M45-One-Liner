#!/usr/bin/env python3
"""ST87 offline, read-only research audit report. No deploy credentials."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

def report(root):
    root = pathlib.Path(root).resolve()
    tests = root / "m45-st86" / "test_self_assignment.py"
    guard = root / "m45-st86" / "test_assignment_guard.cjs"
    checks = []
    for name, cmd in [
        ("st86_python", [sys.executable, "-m", "unittest", "discover", "-s", "m45-st86", "-p", "test_*.py"]),
        ("st86_js", ["node", str(guard)]),
    ]:
        try:
            p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=90, check=False)
            checks.append({"name": name, "passed": p.returncode == 0, "returncode": p.returncode,
                           "output_sha256": hashlib.sha256((p.stdout + p.stderr).encode()).hexdigest()})
        except (OSError, subprocess.TimeoutExpired) as exc:
            checks.append({"name": name, "passed": False, "error": type(exc).__name__})
    return {"protocol": "M45-ST87-ACADEMIC-PRIORITY-v1",
            "checks": checks, "all_passed": all(c["passed"] for c in checks),
            "deployment": "DISABLED", "merge": "DISABLED",
            "human_review_required": True}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--output", default="m45-st87-report.json")
    a = p.parse_args()
    result = report(a.root)
    pathlib.Path(a.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["all_passed"] else 1

if __name__ == "__main__":
    sys.exit(main())
