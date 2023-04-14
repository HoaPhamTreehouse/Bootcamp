import pandas as pd
import json
import requests
from web3 import Web3
import urllib.request as urllib2
import ssl
from config import getNodeLink, API_key, getAPI_io, contract_db, smartContract


def getAPIEndPoint(_chain, _token_address):
    _io_link = getAPI_io(_chain)
    api_key = API_key(_chain)
    api_keys_string = f'&apikey={api_key}'
    ABI_ENDPOINT = f'https://api{_io_link}/api?module=contract&action=getabi&address={_token_address}' + api_keys_string
    return ABI_ENDPOINT

def getABI(_chain, _token_address):
    ABI_ENDPOINT = getAPIEndPoint(_chain, _token_address)
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
    
def classifiedMathType(_chain, functions):
    if hasattr(functions, "token0") and hasattr(functions, "token1") and hasattr(functions, "getReserves") and (functions,"kLast"):
        type = "5050_Math"
    elif hasattr(functions, "getNormalizedWeight"):
        type = "Balancer_Weighted_Math"
    elif hasattr(functions, "positions") and hasattr(functions, "liquidity"):
        if _chain == "bsc":
            type = "Izumi_Math"
        else:
            type = "UniswapV3_Math"
    elif hasattr(functions, "A") and hasattr(functions, "gamma"):
        type = "Curve_V2_Crypo_Math"
    elif hasattr(functions, "A") or hasattr(functions, "getAmplificationParameter") or hasattr(functions, "AmplificiationParameter"):
        type = "Curve_V1_Stable_Math"
    else:
        type = "unclassified"
    return type

def ProxyContract(_chain, web3, contractChecksum, contract_obj):
    implementation_address = contract_obj.functions.implementation().call()
    implementation_abi_string = getABI(_chain, implementation_address)
    contract_obj = web3.eth.contract(address=contractChecksum, abi = implementation_abi_string)
    return contract_obj
    
def getInfo(functions):
    decimal = functions.decimals().call() if hasattr(functions, 'decimals') else None  
    symbol = functions.symbol().call() if hasattr(functions, 'symbol') else None
    name = functions.name().call() if hasattr(functions, 'name') else None
    return decimal, symbol, name

def getunderlyingInfo_5050_Math(_chain, web3, functions):
    underlyingInfo = []
    for _index in range(2):
        _underlyingInfo = {}
        _token_underlying_address = eval(f"functions.token{_index}().call()")
        underlying_ObjInfo = getContract_Obj(_chain, _token_underlying_address, web3)
        _underlyingInfo["token_address"] = _token_underlying_address
        if underlying_ObjInfo:
            functions_underlying = underlying_ObjInfo[1]
            underlying_info = getInfo(functions_underlying)
            _underlyingInfo["decimal"] = underlying_info[0]
            _underlyingInfo["symbol"] = underlying_info[1]
            _underlyingInfo["name"] = underlying_info[2]
            _underlyingInfo["index"] = _index
            _underlyingInfo["weight"] = 0.5
            underlyingInfo.append(_underlyingInfo)
        else:
            _underlyingInfo['info'] = "err_cannot_get_abi"
    return underlyingInfo

def getContract_Obj(_chain, _token_address, web3):
    contractChecksum = web3.toChecksumAddress(_token_address)
    _abi = getABI(_chain, _token_address)
    if _abi:
        contract_obj = web3.eth.contract(address=contractChecksum, abi = _abi)
        functions = contract_obj.functions
        if hasattr(functions, 'implementation'):
            contract_obj = ProxyContract(_chain, web3, contractChecksum, functions)
            functions = contract_obj.functions
        return contract_obj, functions, _abi
    else:
        return None
    
def multicalContract(_chain, type = "getLPInfo"):
    abi_file = open("abi.txt", "r")
    ABI = abi_file.read()
    abi_file.close()
    node_link = getNodeLink(_chain)
    web3 = Web3(Web3.HTTPProvider(node_link))
    if _chain == "eth":
        if type == "getWalletBalances":
            contract = smartContract(_chain)[1]
        else:
            contract = smartContract(_chain)[0]
    else:
        contract = smartContract(_chain)
    multi_address = web3.toChecksumAddress(contract)
    multiContract = web3.eth.contract(address=multi_address, abi = ABI)
    return multiContract

def multical5050LPInfo(df: pd.DataFrame):
    df = df[df['type'] == "5050_Math"]
    chains = df['chain'].unique()
    # chains = ["polygon"]
    result_data = {}
    for _chain in  chains:
        _data = df[df["chain"] == _chain]
        list_5050 = list(_data["addrChecksum"].unique())
        multiContract = multicalContract(_chain)
        result = multiContract.functions.getLPInfo(list_5050).call()
        result_data[_chain] = result
    return result_data

def convertMulti5050Result(df: pd.DataFrame):
    df = df[df['type']== "5050_Math"]
    result_data = multical5050LPInfo(df)
    chains = df['chain'].unique()
    data = pd.DataFrame()
    for _chain in chains:
        _result_data = result_data[_chain]
        _dict_result = {}
        data_df = df[df['chain'] == _chain]
        for _item in _result_data:
            _dict_result[_item[0]] = _item
        data_df['info'] = data_df["addrChecksum"].apply(lambda address: _dict_result[address])
        data = data.append(data_df)
    data['token0'] = data["info"].apply(lambda info: info[1])    
    data['token1'] = data["info"].apply(lambda info: info[2])
    data['symbol'] = data["info"].apply(lambda info: info[7])
    data.to_csv("5050.csv")  
    return data

def multical5050underlyingInfo(df):
    """
    df data return from convertMulti5050Result
    """
    chains = df['chain'].unique()
    for _chain in chains:   
        result_data = {}
        multiContract = multicalContract(_chain)
        data = df[df['chain'] == _chain]
    
    return

    # contract_list = list(data["addrChecksum"].unique())
    # token0_list = data['token0'].to_list()
    # token1_list = data['token1'].to_list()
    # token0_list.extend(token1_list)
    # token_list = list(set(token0_list))


    # while _count < len(contract_list):
    #     _contract_list = contract_list[_index:_count]
    #     _result = multiContract.functions.getWalletBalances(_contract_list,token_list).call({"gas": 30000000})
    #     _index += 3
    #     _count += 3
    #     result.extend(_result)
    # for _item in result:
    #     result_data[]
    # result_data[_chain] = result
        


    return


    
def main(_chain, LP_address, protocol_name):
    node_link = getNodeLink(_chain)
    web3 = Web3(Web3.HTTPProvider(node_link))
    param = {"cid": LP_address}
    param['protocol'] = protocol_name
    LPcontract_ObjInfo = getContract_Obj(_chain, LP_address, web3)
    if LPcontract_ObjInfo:
        functions = LPcontract_ObjInfo[1]
        if _chain in ["eth", "bsc", "avax"]:
            contract = contract_db(_chain)
            # LPcontract_obj = LPcontract_ObjInfo[0]
            LP_address_info = contract.find_one({"address": LP_address})
            if LP_address_info:
                param["decimal"] = LP_address_info.get('decimal', None)
                param["symbol"] = LP_address_info.get('symbol', None)
                param["name"] = LP_address_info.get('name', None)
                param["underlying"] = LP_address_info.get('underlying', None)
                param["abi"] = LP_address_info.get('abi', None)
                param["type"] = classifiedMathType(_chain, functions)
                return param
        # LPcontract_obj = LPcontract_ObjInfo[0]
        param["abi"] = LPcontract_ObjInfo[2]
        param["type"] = classifiedMathType(_chain, functions)
        LPinfo = getInfo(functions)
        param["decimal"] = LPinfo[0]
        param["symbol"] = LPinfo[1]
        param["name"] = LPinfo[2]
        # param["underlying"] = eval(f"getunderlyingInfo_{param['type']}(_chain, web3, functions)")
    else:
        param['abi'] = "err_cannot_get_abi"
    return param

def main_classify(_chain, LP_address, web3):
    LPcontract_ObjInfo = getContract_Obj(_chain, LP_address, web3)
    if LPcontract_ObjInfo:
        functions = LPcontract_ObjInfo[1]
        _type = classifiedMathType(_chain, functions)
    else:
        _type = "err_cannot_get_abi"
    return _type


def classify(df):
    chains = df['chain'].unique()
    data_result = pd.DataFrame()
    for _chain in chains:
        node_link = getNodeLink(_chain)
        web3 = Web3(Web3.HTTPProvider(node_link))
        data = df[df["chain"] == _chain]
        data['type'] = data["addr"].apply(lambda address: main_classify(_chain, address, web3))
        # data['addrChecksum'] = data["addr"].apply(lambda address: web3.toChecksumAddress(address))
        data_result = data_result.append(data)
    return data_result



if __name__ == "__main__":
    # df = pd.read_csv("synthetic.csv")
    df = pd.read_csv("5050.csv")
    data_result = multical5050underlyingInfo(df)


    print()

