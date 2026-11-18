"""CVOC-ST02: read-only, fail-closed manifest validation; no native ST execution."""
import hashlib
import json
import re
from pathlib import Path

PROTOCOL = 'cvoc-integration-v0'
COMPONENTS = {
    'st30-tape': ('TMState', 'VerifiedTMState', 1000),
    'st38-sk-ledger': ('SKLedger', 'VerifiedSKLedger', 1000),
    'st43-pocket': ('PocketLedger', 'VerifiedPocketLedger', 64),
    'st44-continuity': ('ContinuityState', 'VerifiedContinuityState', 64),
    'st47-state': ('StateEnvelope', 'VerifiedStateEnvelope', 1000),
}
HEX = re.compile(r'[0-9a-f]{64}\Z')
SHA = re.compile(r'[0-9a-f]{40}\Z')

class Rejected(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify_manifest(m, data, max_bytes=1048576):
    if not isinstance(m, dict) or set(m) != {'protocol','component','source_commit','schema_version','input_digest_sha256','operator_type','execution_budget','authorization','native_verification'}:
        raise Rejected('invalid manifest fields')
    if m['protocol'] != PROTOCOL or m['component'] not in COMPONENTS:
        raise Rejected('unknown protocol or component')
    if not isinstance(m['source_commit'], str) or not SHA.fullmatch(m['source_commit']):
        raise Rejected('source must be pinned to a full SHA-1 Git commit ID')
    if m['schema_version'] != 'unverified-raw-v0':
        raise Rejected('unsupported schema')
    if m['authorization'] != 'read-only' or m['native_verification'] is not False:
        raise Rejected('no write or native-verification claims permitted')
    inp, out, limit = COMPONENTS[m['component']]
    if m['operator_type'] != f'RawBytes -> Unverified{out}':
        raise Rejected('type mismatch')
    budget = m['execution_budget']
    if type(budget) is not int or not 0 <= budget <= limit:
        raise Rejected('invalid budget')
    if not isinstance(data, bytes) or len(data) > max_bytes:
        raise Rejected('invalid or oversized input')
    claimed = m['input_digest_sha256']
    if not isinstance(claimed, str) or not HEX.fullmatch(claimed) or digest(data) != claimed:
        raise Rejected('digest mismatch')
    return {'accepted': True, 'component': m['component'], 'digest': digest(data), 'native_verified': False, 'cross_component_verified': False, 'execution_performed': False}

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('manifest', type=Path)
    p.add_argument('artifact', type=Path)
    args = p.parse_args()
    try:
        if args.manifest.stat().st_size > 8192 or args.artifact.stat().st_size > 1048576:
            raise Rejected('file too large')
        m = json.loads(args.manifest.read_text(encoding='utf-8'))
        result = verify_manifest(m, args.artifact.read_bytes())
        print(json.dumps(result, sort_keys=True))
    except (Rejected, OSError, ValueError, TypeError) as exc:
        p.exit(1, f'REJECTED: {exc}\n')

if __name__ == '__main__':
    main()
