"""Read-only typed operator graph: verification edges, not state conversion."""
from dataclasses import dataclass

class ContractError(ValueError):
    pass

@dataclass(frozen=True)
class Operator:
    name: str
    input_type: str
    output_type: str
    writes: bool = False

OPERATORS = {
    "st30.verify": Operator("st30.verify", "ST30Tape", "VerifiedST30Tape"),
    "st38.verify": Operator("st38.verify", "ST38Ledger", "VerifiedST38Ledger"),
    "st43.verify": Operator("st43.verify", "ST43Pocket", "VerifiedST43Pocket"),
    "st44.verify": Operator("st44.verify", "ST44WithVerifiedST43Pocket", "VerifiedST44State"),
    "st47.verify": Operator("st47.verify", "ST47Envelope", "VerifiedST47Envelope"),
    "st43_st44.bind": Operator("st43_st44.bind", "VerifiedST43Pocket", "ST44PocketBinding"),
}

def validate_chain(names, input_type):
    if not isinstance(names, (list, tuple)) or not names:
        raise ContractError("empty or invalid chain")
    if not isinstance(input_type, str) or not input_type:
        raise ContractError("invalid input type")
    current = input_type
    for name in names:
        op = OPERATORS.get(name)
        if op is None or op.writes:
            raise ContractError("unknown or mutating operator")
        if current != op.input_type:
            raise ContractError(f"type mismatch: {current} != {op.input_type}")
        current = op.output_type
    return current

def verify_st43_st44_binding(st43, st44, pocket, state):
    """Actually call both native verifiers; returns a read-only Boolean."""
    if not st43.verify(pocket):
        return False
    if not st44.verify(state, pocket):
        return False
    return state.get("pocket_sha256") == pocket.get("sha256")
