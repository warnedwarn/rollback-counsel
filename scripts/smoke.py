import json, re, subprocess, sys, time
from pathlib import Path
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
if len(sys.argv) != 2: raise SystemExit('usage: python scripts/smoke.py <contract-address>')
ADDRESS = sys.argv[1]
env = (ROOT.parents[3] / 'accounts.env').read_text()
key = re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M).group(1).strip()
account = create_account(account_private_key=key)
client = create_client(chain=studionet, account=account)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
proposal = 'RC-' + str(int(time.time()))
release = f'https://raw.githubusercontent.com/warnedwarn/rollback-counsel/{commit}/evidence/fixtures/release-v4.2.1.txt'
incident = f'https://cdn.jsdelivr.net/gh/warnedwarn/rollback-counsel@{commit}/evidence/fixtures/incident-781.txt'

def execution(info):
 receipts = (info.get('consensus_data') or {}).get('leader_receipt') or []
 return receipts[0].get('execution_result') if receipts else info.get('tx_execution_result_name')
def send(name, args):
 tx = client.write_contract(address=ADDRESS, function_name=name, args=args, value=0)
 print(name + '_tx=' + str(tx), flush=True)
 client.wait_for_transaction_receipt(transaction_hash=tx, status='FINALIZED', retries=120, interval=10000)
 info = client.get_transaction(transaction_hash=tx); result = execution(info)
 if info.get('status_name') != 'FINALIZED' or result not in ('SUCCESS', 'FINISHED_WITH_RETURN'): raise RuntimeError({'function': name, 'status': info.get('status_name'), 'execution': result})
 return tx, info.get('status_name'), result

transactions = {}
transactions['propose'] = send('propose_rollback', [proposal, release, incident, 'v4.1.9', 86400])
transactions['review'] = send('review_rollback', [proposal])
reviewed = client.read_contract(address=ADDRESS, function_name='get_rollback', args=[proposal])
if reviewed['state'] != 'AUTHORIZED' or reviewed['decision'] != 'AUTHORIZED' or reviewed['supporting_indexes'] != [0, 1] or reviewed['opposing_indexes'] or reviewed['risk_codes'] or len(reviewed['digests']) != 2: raise RuntimeError(reviewed)
transactions['execute'] = send('execute_rollback', [proposal])
state = client.read_contract(address=ADDRESS, function_name='get_rollback', args=[proposal])
if state['state'] != 'EXECUTED' or state['owner'].lower() != account.address.lower(): raise RuntimeError(state)
proof = {'network': 'StudioNet', 'contract': ADDRESS, 'sourceCommit': commit, 'wallet': account.address, 'proposalId': proposal, 'sources': [release, incident], 'transactions': {name: {'hash': value[0], 'status': value[1], 'execution': value[2]} for name, value in transactions.items()}, 'state': state}
(ROOT / 'evidence' / 'network-run.json').write_text(json.dumps(proof, indent=2))
print(json.dumps(proof, indent=2), flush=True)
