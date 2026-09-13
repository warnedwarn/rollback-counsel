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

Deployment evidence will be updated after the corrected source is committed and deployed from the warnedwarn wallet. Demo records prove the contract workflow and source separation only; they do not claim independent publisher ownership or trusted authority.
