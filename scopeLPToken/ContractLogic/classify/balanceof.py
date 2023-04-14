import requests
from web3 import Web3

# node_link = f"https://polygon.w3node.com/77e0b9890e05bb7a99c511ca3fe5d0573e26797b398045a58e5b94ff704ce865/api" #RockX
node_link = f"https://polygon.blockpi.network/v1/rpc/e4cd39fed22aa2bdad7118ae02f0fbf1b8f4aa6c" #Block PI
_token_address = f"0xb0C22d8D350C67420f06F48936654f567C73E8C8"
api_key = f"I2S28HBWEJE7CTCBDPHTD3DSRBYEDQ7BF8"
api_keys_string = f'&apikey={api_key}'
_io_link = f".polygonscan.com"
ABI_ENDPOINT = f'https://api{_io_link}/api?module=contract&action=getabi&address={_token_address}' + api_keys_string

web3 = Web3(Web3.HTTPProvider(node_link))
contractChecksum = web3.toChecksumAddress(_token_address)
rsp_api = requests.get(ABI_ENDPOINT)
rsp = rsp_api.json()
api = rsp['result']
contract_obj = web3.eth.contract(address=contractChecksum, abi = api)
balanceOf = contract_obj.functions.balanceOf("0x22aB0CE219bE85CD12e791d715eE5FF1922d9A4F").call(block_identifier = int(41123419))
print()