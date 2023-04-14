import pandas as pd
import json
import requests

block_chain_list = {
    # 'avalanche-mainnet': '0x6914fc70fac4cab20a8922e900c4ba57feecf8e1',
    # 'bitcoin-mainnet': '1MHjXoDbbfsMxEGg9kmA435CcVtS1AZ6BE',
    # 'bitcoin-abc-mainnet': 'qr65z63ud05lchị th2e8q3khyktxftkf38c4lrqpf6pn949',
    # 'bnb-mainnet': '0xcc8e6d00c17eb431350c6c50d8b8f05176b90b11',
    # 'ethereum-mainnet': '0xAFca489d144fF5865fF4116eB34E3D586456cF41',
    # 'litecoin-mainnet': 'MKEwkLGyWxUanW12tabWi9u2MWttMAqxih',
    'polygon-mainnet': '0x540df7f55552742080481e6616ad184fff30e590',
    # 'solana-mainnet': '3kQJyZKC4tdQy3nqCqFiLDT2V7dzG65vSKtkUGCht5L3',
    # 'solana-mainnet': '6sR6RuVQJTGoHpJqZfzwQ7pFSvpYMyx1E4X6FN3sGFfh',
    # 'zcash-mainnet': 't1PKBiv7mtzD9bNafYaqyxaENeiNDbpKxxQ'
}
header = {
    'accept': 'application/json',
    'x-api-key': 'UAK2737ca7c451e145cfccc825dc428dec0'
}
endpoint = 'aavev3'
# DEX
if endpoint == 'DEX':
    protocol = 'uniswapv3'
    api_link = f'https://web3api.io/api/v2/market/defi/dex/pairs?exchange={protocol}'

    raw_data = json.loads(requests.get(api_link, headers= header).text)
    data = pd.DataFrame(raw_data['payload']['data'])

# TOKEN BALANCES LATEST (RDB) - INSERT WID - RETURN BALANCE OF TOKEN IN WID
elif endpoint == 'token_rdb':
    for _block_chain, address in block_chain_list.items():
        header['x-amberdata-blockchain-id'] = _block_chain
        api_link = f'https://web3api.io/api/v2/addresses/{address}/token-balances/latest?page=0&size=1000'
        raw_data = json.loads(requests.get(api_link, headers= header).text)
        try:    
            data = pd.DataFrame(raw_data['payload']['records'])
        except: continue
        print()

# TOKEN BALANCE HISTORY
elif endpoint == 'token_hdb':
    for _block_chain, address in block_chain_list.items():
        header['x-amberdata-blockchain-id'] = _block_chain
        api_link = f'https://web3api.io/api/v2/addresses/{address}/token-balances/historical?page=0&size=100'
        raw_data = json.loads(requests.get(api_link, headers= header).text)
        try:    
            data = pd.DataFrame(raw_data['payload']['records'])
        except: continue
        print()

    
    raw_data = json.loads(requests.get(api_link, headers= header).text)
    data = pd.DataFrame(raw_data['payload']['records'])

elif endpoint == 'asset_info':
    api_link = f'https://web3api.io/api/v2/market/defi/prices/asset/information/'
    raw_data = json.loads(requests.get(api_link, headers= header).text)
    data = pd.DataFrame(raw_data['payload'])

elif endpoint == 'market_metric':
    api_link= f'https://web3api.io/api/v2/market/tokens/prices/mkr/latest?timeFormat=ms'

elif endpoint == 'aavev3':
    sub_endpoint = 'wid_info'
    if sub_endpoint == 'action':
        for _block_chain, address in block_chain_list.items():
            # _block_chain = 'polygon-mainnet'
            header['x-amberdata-blockchain-id'] = _block_chain
            api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/protocol'
            # _block_chain = 'polygon-mainnet'
            # header['x-amberdata-blockchain-id'] = _block_chain
            raw_data = json.loads(requests.get(api_link, headers= header).text)
            data = pd.DataFrame(raw_data['payload']['data'])
    elif sub_endpoint == 'wid_info':
        # wallet_address = f'0xbd90be3937744e2cd0ee680807901b1ab9479ffc'
        # api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/wallets/{wallet_address}/portfolio?timeFormat=hr'
        for _block_chain, address in block_chain_list.items():
            # _block_chain = 'polygon-mainnet'
            header['x-amberdata-blockchain-id'] = _block_chain
            api_link = f'https://web3api.io/api/v2/defi/lending/aavev3/wallets/{address}/portfolio?timeFormat=hr'
            raw_data = json.loads(requests.get(api_link, headers= header).text)
            data = pd.DataFrame(raw_data['payload']['data'])




print()