# M45-ST/45 — Doraemon–G Unified Machine

ST45 unifies **ST42 prime Gödel memory records**, **ST43 persistent hash-linked pocket ledger** and **ST44 bounded, stoppable verification loop** behind a single pure transition function.

`transition(state, action, payload)` is the virtual-machine interface; actions are symbolic operators, not separate minds or hardware gears. Supported actions: `remember`, `recall`, `tick`, `stop`, `inspect`.

## Example

```sh
python3 -m unittest discover -s m45-st45 -p 'test_*.py'
python3 m45-st45/unified_machine.py --file doraemon-g.json --init --action inspect
python3 m45-st45/unified_machine.py --file doraemon-g.json --action remember --payload '{"name":"Doraemon (fiction)","values":[1,0,2],"message":"Help others"}'
python3 m45-st45/unified_machine.py --file doraemon-g.json --action recall --payload '{"code":1500}'
python3 m45-st45/unified_machine.py --file doraemon-g.json --action tick
python3 m45-st45/unified_machine.py --file doraemon-g.json --action stop
```

## Design boundaries

- Every operation checks the whole state, with fail-closed validation.
- Memory changes create a new controller epoch **only when the current epoch has no ticks**. Once ticks exist, updates are rejected rather than silently rewriting controller history.
- Stop is explicit and effective. No self-restart, perpetual scheduler, deletion resistance or hidden GitHub Actions triggering.
- A single JSON file is atomically replaced; concurrent writers, crash-resistant directory sync and cryptographic authentication are out of scope.
- GitHub Actions are **ephemeral CI workers**, not a physically continuous computer. Future integration needs a single-writer state store, authenticated updates, version checks and explicit operator approval.
- This is a fictional character-inspired symbolic state machine, **not subjective consciousness**, time travel or an embodied robot.
- ST39's SK reducer/controller is **not integrated** in ST45. This release integrates ST42–ST44 only.

The PR is draft and stacked on ST44. CI and merge status remain unconfirmed.
