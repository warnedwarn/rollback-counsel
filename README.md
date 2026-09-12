# RollbackCounsel

> **CONTROL ROOM / ROLLBACK AUTHORIZATION** · Do not turn back a release until the incident record and release record agree.

RollbackCounsel is a release-safety decision gate. A rollback is not treated as an ordinary button click: it is a proposed move from one specific release to a named target version, justified against a public release note and an independent incident record.

## Console state machine

`PROPOSED → AUTHORIZED | HOLD`, then `EXECUTED` by the release owner, or `LAPSED` permissionlessly after expiry.

`propose_rollback` freezes the target version and evidence locations. `review_rollback` has GenLayer validators fetch both records and decide whether the rollback is justified, retaining a bounded list of risks. An authorization does not execute itself: only the original release owner may use `execute_rollback`.

## Console interlocks

The contract rejects duplicate proposals, repeated evidence hosts, expired reviews, malformed URLs, unauthorized execution, and lapsed-state replay. Validators compare the exact stored decision and risk list rather than trusting leader-only output.

## Operator checks

```bash
PYTHONUTF8=1 genvm-lint contracts/contract.py
python -m pytest -q
```

StudioNet: [`0x1b9C51FBe50FfA3fe6496f4a61CC50Abc759249F`](https://explorer-studio.genlayer.com/address/0x1b9C51FBe50FfA3fe6496f4a61CC50Abc759249F)
