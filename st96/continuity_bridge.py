"""ST96 Sewashi x DARC-Net offline continuity bridge (synthetic data only).

No network, cloud SDK, secrets, deployment, investment, or self-authorization.
The HMAC key below is a fixed PUBLIC TEST FIXTURE and must never be used for real authentication.
"""
from __future__ import annotations
import hashlib
import hmac
import json
from dataclasses import dataclass

TEST_KEY = b"ST96-PUBLIC-SYNTHETIC-FIXTURE-NOT-A-SECRET"
SCHEMA = "st96-continuity-v0.1"
ALLOWED_TYPES = {"research_note", "simulation_result", "venture_hypothesis"}
BLOCKED_FIELDS = {"password", "secret", "token", "private_key", "model_weights", "api_key", "access_token"}
FORBIDDEN_ACTIONS = {"deploy", "invest", "transfer_money", "approve_pr", "merge_pr", "change_secrets"}

class Denied(ValueError):
    pass

def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def validate(record: dict) -> dict:
    if type(record) is not dict or set(record) != {"schema", "id", "kind", "source", "payload", "approved_for_transfer"}:
        raise Denied("invalid record schema")
    if record["schema"] != SCHEMA or record["kind"] not in ALLOWED_TYPES:
        raise Denied("unrecognized schema or kind")
    if record["source"] not in ("sewashi", "darc-net"):
        raise Denied("unrecognized source")
    if type(record["id"]) is not str or not record["id"] or len(record["id"]) > 128:
        raise Denied("invalid id")
    if record["approved_for_transfer"] is not True:
        raise Denied("explicit authorization required")
    payload = record["payload"]
    if type(payload) is not dict or len(canonical(payload)) > 8192:
        raise Denied("payload invalid or oversized")
    def check(obj):
        if type(obj) is dict:
            for key, value in obj.items():
                if type(key) is not str:
                    raise Denied("non-string key")
                if key.lower() in BLOCKED_FIELDS or key.lower() == "action" and value in FORBIDDEN_ACTIONS:
                    raise Denied("forbidden field or action")
                check(value)
        elif type(obj) is list:
            for item in obj: check(item)
        elif obj is not None and type(obj) not in (str, int, bool, float):
            raise Denied("unsupported value")
    check(payload)
    return record

def seal(record: dict, key: bytes = TEST_KEY) -> dict:
    # No trust claim: the fixed fixture key only detects accidental corruption in offline tests.
    validate(record)
    body = canonical(record)
    return {"record": record, "sha256": hashlib.sha256(body).hexdigest(),
            "hmac_sha256": hmac.new(key, body, hashlib.sha256).hexdigest()}

def verify(envelope: dict, key: bytes = TEST_KEY) -> dict:
    if type(envelope) is not dict or set(envelope) != {"record", "sha256", "hmac_sha256"}:
        raise Denied("invalid envelope")
    record = validate(envelope["record"])
    body = canonical(record)
    if not hmac.compare_digest(hashlib.sha256(body).hexdigest(), envelope["sha256"]):
        raise Denied("digest mismatch")
    if not hmac.compare_digest(hmac.new(key, body, hashlib.sha256).hexdigest(), envelope["hmac_sha256"]):
        raise Denied("authentication mismatch")
    return record

def three_node_simulation(envelope: dict) -> dict:
    """Simulate three isolated in-memory copies; a corrupted copy is rejected."""
    nodes = [json.loads(json.dumps(envelope)) for _ in range(3)]
    nodes[1]["record"]["payload"]["text"] = "tampered synthetic example"
    good, rejected = 0, 0
    for node in nodes:
        try:
            verify(node)
            good += 1
        except Denied:
            rejected += 1
    return {"accepted": good, "rejected": rejected, "no_network": True}

def sample_record() -> dict:
    return {"schema": SCHEMA, "id": "synthetic-001", "kind": "research_note",
            "source": "sewashi", "payload": {"text": "Synthetic research note"},
            "approved_for_transfer": True}

if __name__ == "__main__":
    env = seal(sample_record())
    result = three_node_simulation(env)
    print(json.dumps({"prototype": SCHEMA, "simulation": result,
                      "scope": "offline synthetic demonstration; no deployment or scientific proof"}, sort_keys=True))
