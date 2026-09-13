import base64, hashlib, json, re, time
from pathlib import Path
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
deployment = json.loads((ROOT / 'deployment.json').read_text())
run = json.loads((ROOT / 'evidence' / 'network-run.json').read_text())
env = (ROOT.parents[3] / 'accounts.env').read_text(); key = re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M).group(1).strip()
account = create_account(account_private_key=key); client = create_client(chain=studionet, account=account)
hashes = {'deployment': deployment['deploymentTransaction'], **{name: item['hash'] for name, item in run['transactions'].items()}}
records = {name: client.get_transaction(transaction_hash=value) for name, value in hashes.items()}
def execution(info):
 receipts = (info.get('consensus_data') or {}).get('leader_receipt') or []
 return receipts[0].get('execution_result') if receipts else info.get('tx_execution_result_name')
deployed = base64.b64decode(records['deployment']['data']['contract_code']).decode(); local = (ROOT / 'contracts' / 'contract.py').read_text()
state = client.read_contract(address=deployment['contractAddress'], function_name='get_rollback', args=[run['proposalId']])
proof = {'sourceMatches': deployed == local, 'contractSha256': hashlib.sha256(local.encode()).hexdigest(), 'walletMatchesOwner': state['owner'].lower() == account.address.lower(), 'state': state, 'transactions': {name: {'hash': hashes[name], 'status': info.get('status_name'), 'execution': execution(info)} for name, info in records.items()}}
assert proof['sourceMatches'] and proof['walletMatchesOwner'] and state['state'] == 'EXECUTED' and len(state['digests']) == 2
assert all(item['status'] == 'FINALIZED' and item['execution'] in ('SUCCESS', 'FINISHED_WITH_RETURN') for item in proof['transactions'].values())
print(json.dumps(proof, indent=2))
