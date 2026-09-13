# RollbackCounsel remediation matrix

| Requirement | Code path | Targeted proof | Live proof | Status |
|---|---|---|---|---|
| Bind fetched evidence to the stored ruling | `_records`, `_assess`, `get_rollback` | PASS: `test_authorized_lifecycle_binds_sources` | PASS: `RC-1789278045` stores two indexes and two digests | PASS |
| Reject forged digests and source attribution | validator in `_assess` | PASS: `test_validator_rejects_forged_digest_and_attribution` | PASS: deployed source matches reviewed source | PASS |
| Avoid exact free-form prose equality | closed enums and semantic verifier | PASS: `test_semantic_validator` | PASS: validator review `0xe369c0c5ae13edd66e4eab7a4dfdf22c1870571c59995ee5986eaf404c5d8735` | PASS |
| Normalize and separate HTTPS origins | `source`, `propose_rollback` | PASS: `test_duplicate_origins_ids_and_bad_urls_fail` | PASS: live state preserves two normalized origins | PASS |
| Preserve owner execution and permissionless expiry | `execute_rollback`, `lapse_rollback` | PASS: `test_authorization_owner_expiry_and_permissionless_lapse` | PASS: owner execution `0x6b05651cd84f03e97fcf480346e70d66aee582e04acc6c83ad3fa471a36dee9e` | PASS |

## Originality check

Release Prism decides whether a candidate may be promoted from three release artifacts. RollbackCounsel starts from a release that is already active, cross-checks a release record against an independent incident record, grants an expiring rollback authorization, separates authorization from owner execution, and allows permissionless lapse. The party roles, transition graph, and downstream authorization primitive are distinct.
