# RollbackCounsel design boundary

## Authoritative inputs

- Immutable canonical proposal ID
- Original owner wallet
- Active release record URL and normalized origin
- Incident record URL and normalized origin
- Exact rollback target and bounded expiry

## Consensus output

- Closed decision: `AUTHORIZED` or `HOLD`
- Closed risk-code set
- Complete supporting/opposing source-index partition
- Ordered full-response SHA-256 digests

## State graph

- `PROPOSED` can be assessed once before expiry.
- `AUTHORIZED` can be executed only by the owner and only before expiry.
- `HOLD` cannot execute.
- Any non-final expired proposal can be lapsed by any caller.
- `EXECUTED` and `LAPSED` are final and reject replay.

## Mechanism difference

Release Prism gates promotion of a candidate release from three release artifacts. RollbackCounsel begins with an already active release, cross-checks a release record against an incident record, creates an expiring authorization rather than an automatic action, and separates validator authorization from owner execution.
