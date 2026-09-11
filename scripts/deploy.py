import re,json
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
r=Path(__file__).parents[1];e=(r.parents[3]/'accounts.env').read_text();k=re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',e,re.M).group(1).strip();c=create_client(chain=studionet,account=create_account(account_private_key=k));h=c.deploy_contract(code=(r/'contracts/contract.py').read_text(),args=[]);print('deploy_tx='+str(h),flush=True);z=c.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=120,interval=10000);print(json.dumps({'tx':h,'receipt':z},default=str),flush=True)
