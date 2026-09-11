# RollbackCounsel

Evaluates a proposed software rollback against a release note and incident record. Lifecycle: PROPOSED -> REVIEWED -> AUTHORIZED or HOLD -> EXECUTED / LAPSED. Only the release owner can execute; any caller can lapse an expired proposal.

This is not sequence verification: it makes a safety authorization decision about one rollback proposal, retaining risk indexes and evidence digests.
