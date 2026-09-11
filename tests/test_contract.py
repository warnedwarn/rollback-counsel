from pathlib import Path
import ast
s=(Path(__file__).parents[1]/'contracts/contract.py').read_text()
def test_parse():ast.parse(s)
def test_rollback_lifecycle():assert all(('def '+x) in s for x in ('propose_rollback','review_rollback','execute_rollback','lapse_rollback','get_rollback'))
def test_execution_requires_owner():assert "gl.message.sender_address!=x.owner" in s
