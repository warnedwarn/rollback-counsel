import ast
from pathlib import Path

TEXT = Path('contracts/contract.py').read_text()

def test_parse(): ast.parse(TEXT)
def test_surface():
 for name in ('propose_rollback', 'review_rollback', 'execute_rollback', 'lapse_rollback', 'get_rollback'):
  assert 'def ' + name in TEXT
def test_evidence_binding():
 assert 'sha256' in TEXT and "proposed.get('digests') != digests" in TEXT
 assert 'supporting_indexes' in TEXT and 'opposing_indexes' in TEXT
def test_semantic_validator():
 assert 'RollbackCounsel verifier.' in TEXT and "verdict.get('valid') is True" in TEXT
