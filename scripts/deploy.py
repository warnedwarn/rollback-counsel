import re,json
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
r=Path(__file__).parents[1];e=(r.parents[3]/'accounts.env').read_text();k=re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',e,re.M).group(1).strip();a=create_account(account_private_key=k);c=create_client(chain=studionet,account=a);h=c.deploy_contract(code=(r/'contracts/contract.py').read_text(),args=[]);print('deploy_tx='+str(h),flush=True);z=c.wait_for_transaction_receipt(transaction_hash=h,status='FINALIZED',retries=120,interval=10000);address=z.get('data',{}).get('contract_address') or z.get('to_address') or z.get('recipient');print(json.dumps({'tx':h,'contract':address,'wallet':a.address,'status':z.get('status_name'),'result':z.get('result_name')},default=str),flush=True)
