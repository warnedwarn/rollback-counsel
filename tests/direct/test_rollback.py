import hashlib
from conftest import CONTRACT

RELEASE = 'https://release.example/releases/v4.2.1'
INCIDENT = 'https://incident.example/events/781'
BODIES = [b'Release v4.2.1 replaced v4.1.9 and changed the session migration path.', b'Incident 781 began after v4.2.1 and stopped when the service returned to v4.1.9.']

def prepared(direct_vm, direct_deploy, direct_alice, result='{"decision":"AUTHORIZED","risk_codes":[],"supporting_indexes":[0,1],"opposing_indexes":[]}', incident_status=200):
 direct_vm.warp('2033-01-01T00:00:00+00:00'); direct_vm.sender = direct_alice; contract = direct_deploy(CONTRACT)
 contract.propose_rollback('incident-781', RELEASE, INCIDENT, 'v4.1.9', 3600)
 direct_vm.mock_web(r'release\.example', {'status': 200, 'body': BODIES[0].decode()}); direct_vm.mock_web(r'incident\.example', {'status': incident_status, 'body': BODIES[1].decode()})
 direct_vm.mock_llm(r'.*RollbackCounsel\..*', result); direct_vm.mock_llm(r'.*RollbackCounsel verifier\..*', '{"valid":true}')
 return contract

def test_authorized_lifecycle_binds_sources(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice); contract.review_rollback('INCIDENT-781'); result = contract.get_rollback('incident-781')
 assert result['state'] == 'AUTHORIZED' and result['supporting_indexes'] == [0, 1] and result['opposing_indexes'] == []
 assert result['digests'] == [hashlib.sha256(body).hexdigest() for body in BODIES]
 contract.execute_rollback('incident-781'); assert contract.get_rollback('incident-781')['state'] == 'EXECUTED'

def test_hold_requires_attributed_risk(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice, '{"decision":"HOLD","risk_codes":["VERSION_MISMATCH"],"supporting_indexes":[1],"opposing_indexes":[0]}')
 contract.review_rollback('incident-781'); result = contract.get_rollback('incident-781')
 assert result['state'] == 'HOLD' and result['risk_codes'] == ['VERSION_MISMATCH'] and result['opposing_indexes'] == [0]

def test_duplicate_origins_ids_and_bad_urls_fail(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice)
 with direct_vm.expect_revert('complete rollback proposal required'): contract.propose_rollback('incident-781', RELEASE, INCIDENT, 'v4.1.9', 3600)
 with direct_vm.expect_revert('complete rollback proposal required'): contract.propose_rollback('same-host', RELEASE, 'https://release.example/incidents/2', 'v4.1.9', 3600)
 with direct_vm.expect_revert('valid HTTPS record required'): contract.propose_rollback('bad-url', RELEASE, 'https://incident.example/a/../b', 'v4.1.9', 3600)

def test_validator_rejects_forged_digest_and_attribution(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice); proposal = contract.proposals['INCIDENT-781']; result = contract._assess(proposal)
 assert direct_vm.run_validator(leader_result=result) is True
 forged = dict(result); forged['digests'] = list(reversed(result['digests'])); assert direct_vm.run_validator(leader_result=forged) is False
 forged = dict(result); forged['supporting_indexes'] = [0]; forged['opposing_indexes'] = [1]; assert direct_vm.run_validator(leader_result=forged) is False

def test_authorization_owner_expiry_and_permissionless_lapse(direct_vm, direct_deploy, direct_alice, direct_bob):
 contract = prepared(direct_vm, direct_deploy, direct_alice); contract.review_rollback('incident-781'); direct_vm.sender = direct_bob
 with direct_vm.expect_revert('live owner authorization required'): contract.execute_rollback('incident-781')
 direct_vm.warp('2033-01-01T01:00:01+00:00'); contract.lapse_rollback('incident-781'); assert contract.get_rollback('incident-781')['state'] == 'LAPSED'
 with direct_vm.expect_revert('expired active proposal required'): contract.lapse_rollback('incident-781')

def test_unavailable_source_fails(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice, incident_status=503)
 with direct_vm.expect_revert('record unavailable'): contract.review_rollback('incident-781')

def test_malformed_output_fails(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice, '{"decision":"MAYBE","risk_codes":[],"supporting_indexes":[0,1],"opposing_indexes":[]}')
 with direct_vm.expect_revert('invalid rollback assessment'): contract.review_rollback('incident-781')

def test_expired_review_fails(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice); direct_vm.warp('2033-01-01T01:00:01+00:00')
 with direct_vm.expect_revert('live proposal required'): contract.review_rollback('incident-781')

def test_review_replay_fails(direct_vm, direct_deploy, direct_alice):
 contract = prepared(direct_vm, direct_deploy, direct_alice); contract.review_rollback('incident-781')
 with direct_vm.expect_revert('live proposal required'): contract.review_rollback('incident-781')
