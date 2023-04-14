import pandas as pd
from datetime import datetime
import requests
import json
# from utils.token import getPrice
from utils.db import contract, map_block_date
from classes.Web3Call import Web3Call


# Get list protocol name: 
def getListProtocolName(_chain):  
    if _chain == 'avax':      
        list_protocol = [
        'Pangolin',
        'SushiSwap',
        'Synapse',
        'TraderJoe']
    elif _chain == 'eth':
        list_protocol = ['1inch',
        'Arrakis Finance',
        'Balancer',
        'Curve Finance',
        'DODO',
        'Frax',
        'KyberSwap',
        'KyberSwap Elastic',
        'PancakeSwap',
        'Saddle',
        'ShibaSwap',
        'SushiSwap',
        'Synapse',
        'UniSwap',
        'Uniswap V3']
    elif _chain == 'bsc':
        list_protocol = [
        #     '1inch',
        # 'ApeSwap',
        # 'BiSwap',
        # 'Ellipsis',
        # 'KyberSwap',
        # 'KyberSwap Elastic',
        # 'MDEX',
        'PancakeSwap',
        # 'Synapse',
        # 'Wault'
        ]
    return list_protocol

# Get 50-50 lp Token:
def getData5050LPToken(_chain):
    list_protocol = getListProtocolName(_chain)
    contract_db = contract[_chain]
    if _chain == 'eth':
        query = {'protocol': {'$in': list_protocol},
                    'is_50_50': True
                    }
    else: # _chain == 'avax':
        query = {'protocol': {'$in': list_protocol},
                    'are_weights_equal': True,
                    'num_tokens': 2
                    }
    list_5050Token = contract_db.find(query).skip(485000).limit(100000)
    df = pd.DataFrame(list_5050Token)
    df = df.dropna(subset = ['underlying'])#[['address', 'protocol', 'decimal', 'token0', 'token1']]
    df['decimal0'] = df['underlying'].apply(lambda underlying: underlying[0].get('decimal', 18))
    df['decimal1'] = df['underlying'].apply(lambda underlying: underlying[1].get('decimal', 18))
    df = df[['address', 'protocol', 'decimal', 'token0', 'token1', 'decimal0', 'decimal1']]
    df.to_csv('avax_contract.csv')
    return df

def getYesterdayEODBlock(_chain):
    yesterday = datetime(2023, 3, 6)
    map_block_date_db = map_block_date[_chain]
    block_data = map_block_date_db.find({"date": yesterday})
    end_block = block_data[0]['end_block']
    return int(end_block)


def getDictPrice(_chain, list_token_address, _date_string):
    offset, count = 0, 100
    len_set = len(list_token_address)
    api_link = f'https://gw-prd-v2.treehouse.finance/pricing/v4/prices'
    header = {
        'Authorization': 'Basic 99fabba4ec8299f4cc648659932c0b1fac121062',
        'Content-Type': 'application/json'
    }
    dictPrice = {}
    while count < len_set:
        body = {
            "dates": _date_string,
            "tokens": list_token_address[offset: count],
            "chain": _chain
            }
        raw_data = json.loads(requests.post(api_link, data = json.dumps(body), headers = header).text)['data'][0]
        data = raw_data['data']
        if len(data) > 0:
            for _item in data:
                dictPrice[_item['address']] = _item['prc']
        offset += 100
        count += 100
    return dictPrice


def get_Reserves(_chain, _pool_address, block):
    try:    
        contract_obj = Web3Call(_chain, _pool_address)
        reserves = contract_obj.callBlock('getReserves', block_id = block)
    except:
        reserves = 'Cannot get reserves'
    print(_pool_address)
    return reserves


def main(_chain):
    df = getData5050LPToken(_chain)
    # df.to_csv(f'{_chain}_contract.csv')
    # df = pd.read_csv('eth_contract.csv')
    _date_string = ["2023-03-12T00:00:00"]
    block = getYesterdayEODBlock(_chain)
    _list_token0 = list(df['token0'].unique())
    _list_token1 = list(df['token1'].unique())
    list_token_address = list(set(_list_token0 + _list_token1))
    dictPrice = getDictPrice(_chain, list_token_address, _date_string)
    # dictPrice = pd.read_csv('eth_price.csv')
    # dictPrice = dict(zip(dictPrice['token_address'], dictPrice['price']))
    df['price_token0'] = df['token0'].apply(lambda _token_address: dictPrice.get(_token_address, None))
    df['price_token1'] = df['token1'].apply(lambda _token_address: dictPrice.get(_token_address, None))
    df = df.dropna(how='any')
    # dictReserves = pd.read_csv('Total_pool_value.csv')
    # dictReserves = dict(zip(dictReserves['address'], dictReserves['reserves']))
    # df['reserves'] = df['address'].apply(lambda _address: eval(dictReserves.get(_address, None)))
    df['reserves'] = df['address'].apply(lambda address: get_Reserves(_chain, address, block))
    df = df[df['reserves'] != 'Cannot get reserves']
    df['reserves_token0'] = df['reserves'].apply(lambda reserves: (reserves[0])) / (10 ** df['decimal0'])
    df['reserves_token1'] = df['reserves'].apply(lambda reserves: (reserves[1])) / (10 ** df['decimal1'])
    df['Total_pool_value'] = df['reserves_token0'] * df['price_token0'] + df['reserves_token1'] * df['price_token1']
    df.sort_values('Total_pool_value', ascending= False).to_csv('avax_data.csv')
    return df

if __name__ == '__main__':
    chain = 'bsc'
    main(chain)

