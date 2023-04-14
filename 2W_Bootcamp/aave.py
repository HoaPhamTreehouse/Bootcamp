import pandas as pd
import requests
import json
from web3 import Web3
from api import get_API
from classes.Web3Call import Web3Call
from amber import block_chain_list
from amber import header as amber_header

endpoint = 'aavev3'
if endpoint == 'aavev3':
    sub_endpoint = 'wid_info'
    if sub_endpoint == 'action':
        for _block_chain, address in block_chain_list.items():
            # _block_chain = 'polygon-mainnet'
            amber_header['x-amberdata-blockchain-id'] = _block_chain
            api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/protocol'
            # _block_chain = 'polygon-mainnet'
            # header['x-amberdata-blockchain-id'] = _block_chain
            raw_data = json.loads(requests.get(api_link, headers= amber_header).text)
            data = pd.DataFrame(raw_data['payload']['data'])
    elif sub_endpoint == 'wid_info':
        # wallet_address = f'0xbd90be3937744e2cd0ee680807901b1ab9479ffc'
        # api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/wallets/{wallet_address}/portfolio?timeFormat=hr'
        for _block_chain, address in block_chain_list.items():
            # _block_chain = 'polygon-mainnet'
            amber_header['x-amberdata-blockchain-id'] = _block_chain
            api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/wallets/{address}/portfolio?timeFormat=hr'
            raw_data = json.loads(requests.get(api_link, headers= amber_header).text)
            data = pd.DataFrame(raw_data['payload']['data'])

print()

