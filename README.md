# RollbackCounsel

> **CONTROL ROOM / ROLLBACK AUTHORIZATION** · A release should not be reversed until its release record and an independent incident record support the same target.

RollbackCounsel is a source-bound GenLayer authorization primitive for software rollback decisions. The owner freezes one active release record, one incident record on a distinct HTTPS origin, an exact target version, and an expiry window. Validators fetch both records rather than trusting caller summaries.

## Consensus record

The leader proposes only bounded fields: `AUTHORIZED` or `HOLD`, closed-set risk codes, and a complete partition of source indexes into supporting and opposing evidence. Every validator refetches both records, recomputes ordered SHA-256 response-body digests, checks the candidate shape, and performs a semantic check against the exact target. Free-form rationale is never stored as validator-approved state.

`AUTHORIZED` requires both sources to support the target with no risk code. A hold must identify at least one opposing source and one of `VERSION_MISMATCH`, `INCIDENT_UNCONFIRMED`, `ROLLBACK_UNSUPPORTED`, `RECOVERY_RISK`, or `CONFLICTING_RECORDS`.

## Lifecycle and authority

`PROPOSED → AUTHORIZED → EXECUTED`

`PROPOSED → HOLD`

Any non-final proposal can become `LAPSED` permissionlessly after its stored expiry. Authorization never executes itself: only the original owner can execute an authorized rollback, and authorization cannot be used after expiry.

## Deterministic guards

The contract canonicalizes proposal IDs, rejects duplicates, accepts only parsed HTTPS sources, blocks credentials, fragments, invalid ports, and decoded path traversal, and requires two distinct normalized origins. The decision, risk codes, source attribution, and ordered digests remain readable through `get_rollback`.

## Verification

```bash
genvm-lint contracts/contract.py
python -m pytest -q
python scripts/verify_deployment.py
```

The direct suite covers authorization and hold outcomes, digest and attribution forgery, duplicate IDs and origins, malformed URLs and model output, unavailable sources, unauthorized execution, expired review, replay, and permissionless lapse.

## Verified StudioNet deployment

- Contract: [`0xA6F8…7cC8`](https://explorer-studio.genlayer.com/address/0xA6F8fc49688Ef188757b8D8A76bd5903fE877cC8)
- Deployment: [`0xd5db…e2abc`](https://explorer-studio.genlayer.com/transactions/0xd5dbf40e6fde6c4f5614dbf648340d321b5c9958b8e7a5af0f50096c4d6e2abc), `FINALIZED / SUCCESS`
- Proposal: [`0x2736…561b`](https://explorer-studio.genlayer.com/transactions/0x273640adc7f5b41d3ff4f1c0f07102114be50b40ca14d658e1be808a1d91561b), `FINALIZED / SUCCESS`
- Validator review: [`0xe369…8735`](https://explorer-studio.genlayer.com/transactions/0xe369c0c5ae13edd66e4eab7a4dfdf22c1870571c59995ee5986eaf404c5d8735), `FINALIZED / SUCCESS`
- Owner execution: [`0x6b05…ee9e`](https://explorer-studio.genlayer.com/transactions/0x6b05651cd84f03e97fcf480346e70d66aee582e04acc6c83ad3fa471a36dee9e), `FINALIZED / SUCCESS`

The deployed source matches `contracts/contract.py` byte-for-byte at reviewed commit `b9ddc7c82716f7bddc36f38487e7a2dbe86ee790`. The warnedwarn wallet owns the smoke record, which reached `EXECUTED` after an `AUTHORIZED` decision with two supporting indexes and two stored digests. The two hosted records are reproducible demo fixtures and do not claim independent publisher ownership or trusted authority.
