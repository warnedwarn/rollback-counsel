# RollbackCounsel remediation matrix

| Requirement | Code path | Targeted proof | Live proof | Status |
|---|---|---|---|---|
| Bind fetched evidence to the stored ruling | `_records`, `_assess`, `get_rollback` | PASS: `test_authorized_lifecycle_binds_sources` | New deployment and smoke required | UNVERIFIED |
| Reject forged digests and source attribution | validator in `_assess` | PASS: `test_validator_rejects_forged_digest_and_attribution` | New deployment and smoke required | UNVERIFIED |
| Avoid exact free-form prose equality | closed enums and semantic verifier | PASS: `test_semantic_validator` | New deployment required | UNVERIFIED |
| Normalize and separate HTTPS origins | `source`, `propose_rollback` | PASS: `test_duplicate_origins_ids_and_bad_urls_fail` | New deployment required | UNVERIFIED |
| Preserve owner execution and permissionless expiry | `execute_rollback`, `lapse_rollback` | PASS: `test_authorization_owner_expiry_and_permissionless_lapse` | New lifecycle smoke required | UNVERIFIED |

## Originality check

Release Prism decides whether a candidate may be promoted from three release artifacts. RollbackCounsel starts from a release that is already active, cross-checks a release record against an independent incident record, grants an expiring rollback authorization, separates authorization from owner execution, and allows permissionless lapse. The party roles, transition graph, and downstream authorization primitive are distinct.
