
import pandas as pd
import json
import requests
from web3 import Web3
import urllib.request as urllib2
import ssl

def getNodeLink(_chain):
    node_link_dict = {
                "polygon": f"https://polygon.w3node.com/77e0b9890e05bb7a99c511ca3fe5d0573e26797b398045a58e5b94ff704ce865/api",
                "arbitrum": "https://full-arbitrum.w3node.com/bcb556d86d6f90e4159166941a5fa7cb5d021ec72920c13a027cdab740c344c2/api",
                "optimism": "https://optimism.w3node.com/19ca9e550ba2cb129a801abf38910eadc1693ae2f1171709012fe2473a33ac35/api",
                "eth": "http://harvest-eth-archive.treehouse.finance",
                "bsc": "http://harvest-bsc-archive.treehouse.finance",
                "avax": "http://harvest-avax-archive.treehouse.finance/ext/bc/C/rpc",
    }
    return node_link_dict[_chain]

def API_key(_chain):
    APIKey_dict = {
        "polygon": f"I2S28HBWEJE7CTCBDPHTD3DSRBYEDQ7BF8",
        "arbitrum": f"XU3YPHFPWX55F2A8B7UJ8IKVPC3GG2DR3X",
        "optimism": f"48GTPBXR3GNN1296XERDZIRZ8Y7K52M3RP", 
        "eth": f"978JTWN7MXDSZFI2TI5YTFD9GV6AXZJVJU",
        "bsc": f"F723GDNT8KWRI7XVUNGXYC22FMDY6DKD6M",
        "avax": f"9M41NESN9SQNYRCWJRVW8VSDFNIXCQEC18"
    }
    return APIKey_dict[_chain]

def getABI_io(_chain):
    getscan_io_dict = {
        "polygon": f'.polygonscan.com',
        "arbitrum": f'.arbiscan.io',
        "optimism": f'-optimistic.etherscan.io', 
        "eth": f'.etherscan.io',
        "bsc": f".bscscan.com",
        "avax": f".snowtrace.io"
    }
    return getscan_io_dict[_chain]
    

def getABI(_chain, _contract_address):
    _chain_scan = getABI_io(_chain)
    api_key = API_key(_chain)
    api_keys_string = f'&apikey={api_key}'
    ABI_ENDPOINT = f'https://api{_chain_scan}/api?module=contract&action=getabi&address={_contract_address}' + api_keys_string
    if _chain == 'arbitrum' or _chain == 'optimism':
        headers = {'Content-Type':  'application/json',"User-Agent": "cf-api-python/1.0"}
        request = urllib2.Request(ABI_ENDPOINT,headers=headers)
        request.get_method = lambda:"GET"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        rsp = urllib2.urlopen(
        request, context=ctx, timeout=10)
        rsp = json.loads(rsp.read().decode("utf-8"))
        if rsp['message'] != 'OK':
            return False
        else:
            abi = rsp['result']
            return abi
    else:
        rsp = requests.get(ABI_ENDPOINT)
    if rsp.status_code != 200:
        return False
    rsp = rsp.json()
    try:
        abi = json.loads(rsp['result'])
        return abi
    except:
        return False

def check5050(_chain, contract_address):
    node_link = getNodeLink(_chain)
    web3 = Web3(Web3.HTTPProvider(node_link))
    contractChecksum = web3.toChecksumAddress(contract_address)
    _abi = getABI(_chain, contract_address)
    if _abi:
        contract_obj = web3.eth.contract(address=contractChecksum, abi = _abi)
    else:
        return "Contract source code not verified"
    functions = contract_obj.functions
    if hasattr(functions, "token0") and hasattr(functions, "token1") and hasattr(functions, "getReserves") and (functions,"kLast"):
        return True
    else:
        return False

def non5050_classify(_chain, contract_address):
    node_link = getNodeLink(_chain)
    web3 = Web3(Web3.HTTPProvider(node_link))
     # block = web3.eth.block_number #get latest block
    contractChecksum = web3.toChecksumAddress(contract_address)
    _abi = getABI(_chain, contract_address)
    if _abi:
        contract_obj = web3.eth.contract(address=contractChecksum, abi = _abi)
    else:
        return "Contract source code not verified"
    functions = contract_obj.functions
    functions_support = ['getNormalizedWeight', 'AmplificiationParameter', 'getAmplificationParameter', 'A', 'gamma', 'positions', 'liquidity']
    list_funcs = []
    for _func in functions_support:
        if hasattr(functions, _func):
            list_funcs.append(_func)
    if len(list_funcs) > 0:
        return [True, list_funcs]
    else:
        return [False, list_funcs]

def main5050(_chain):
    data = pd.read_excel('LPToken In Scope.xlsx', sheet_name= f'{_chain}cgk')
    list_dex = list(data['dex_name'].unique())
    df = pd.DataFrame()
    for _dex in list_dex:
        df_data = data[data['dex_name']== _dex]
        df_data = df_data.drop_duplicates(subset = ['addr'])
        df_data = df_data.head()
        list_address = df_data['addr'].unique()
        dict_result = {}
        for _address in list_address:
            dict_result[_address] = check5050(chain, _address)  
        df_data['is_5050'] = df_data['addr'].apply(lambda _address: dict_result[_address])
        df = df.append(df_data)
    return df

def mainEachDEX(_chain,dex_name, data):
    df = data[data['dex_name'] == dex_name]
    list_address = list(df['addr'].unique())[5:]
    dict_result = {}
    for _address in list_address:
        dict_result[_address] = check5050(_chain, _address)
    return dict_result

def mainnon5050(_chain):
    data = pd.read_csv('sample.csv')
    dict_result = {}
    list_address = list(data['addr'].unique())
    for _address in list_address:
        dict_result[_address] = non5050_classify(_chain, _address)  
    # data['is_5050'] = data['addr'].apply(lambda _address: dict_result[_address])
    data['Support'] = data['addr'].apply(lambda _address: dict_result[_address][0])
    data['functions'] = data['addr'].apply(lambda _address: dict_result[_address][1])
    return data


if __name__ == "__main__":
    chain = 'polygon'
    token_address = '0x3BA4c387f786bFEE076A58914F5Bd38d668B42c3'.lower()
    df = check5050(chain, token_address)
    # data = pd.read_excel('LPToken In Scope.xlsx', sheet_name= f'{chain}cgk')
    
    # data = pd.read_csv('sample.csv')
    # data = data[data['Chain'] == f'{chain}']
    # data = data[data['5050'] == False]
    # data = data[data['MORE THAN 1 MIL'] == True]
    # data = data.drop_duplicates(subset=["dex_name"], keep= "first")

    # list_address = data['addr'].unique()
    # # list_address = ['0xd0595ff44638182e6b54051493ec0f045d04335f']
    


    # dict_result = {}
    # for _address in list_address:
    #     dict_result[_address] = check5050(chain, _address)  
    # data['is_5050'] = data['addr'].apply(lambda _address: dict_result[_address])
    # data['Support'] = data['addr'].apply(lambda _address: dict_result[_address][0])
    # data['functions'] = data['addr'].apply(lambda _address: dict_result[_address][1])
    print()






