"""Local source manifest; integrity relative to a trusted manifest only."""
import hashlib,json
from pathlib import Path
FILES=("GCAPO.lean","lean-toolchain","lakefile.toml","certificate_codec.py",
       "proof_halting.py","independent_identity.py","dual_verification.py",
       "bounded_rational.py","direct_limit.py","reproducibility.py")

def manifest(root):
    root=Path(root)
    return {"schema":"UECV-07/v1","sha256":{
        name:hashlib.sha256((root/name).read_bytes()).hexdigest()
        for name in FILES}}

def verify_manifest(root,record):
    try:
        return type(record) is dict and record==manifest(root)
    except (OSError,TypeError,ValueError):
        return False

if __name__=="__main__":
    print(json.dumps(manifest(Path(__file__).resolve().parent),sort_keys=True,indent=2))
