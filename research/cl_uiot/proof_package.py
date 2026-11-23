"""Standalone certificate verification entry point."""
import hashlib,json
from pathlib import Path
from cone_checker import verify
def check(path):
    raw=Path(path).read_bytes()
    if len(raw)>100000:raise ValueError("oversized proof")
    tree=json.loads(raw)
    if not verify(tree):raise ValueError("invalid proof")
    return hashlib.sha256(raw).hexdigest()
if __name__=="__main__":
    import sys
    print("Verified SHA-256:",check(sys.argv[1]))
