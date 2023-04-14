import yaml
import json
import requests
import ssl
import pandas as pd
import urllib.request as urllib2
from web3 import Web3



with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
file.close()

def getAPIEndPoint(_chain, _token_address):
    io_link = config["API_io"][_chain]
    api_key = config["API_key"][_chain]
    base_url = f"https://api{io_link}/api?module=contract&action=getabi"
    address_string = f"&address={_token_address}"
    api_keys_string = f"&apikey={api_key}"
    ABI_ENDPOINT = base_url + address_string + api_keys_string
    return ABI_ENDPOINT

def getABI(_chain, _token_address):
    ABI_ENDPOINT = getAPIEndPoint(_chain, _token_address)
    if _chain == "arbitrum" or _chain == "optimism":
        headers = {"Content-Type":  "application/json","User-Agent": "cf-api-python/1.0"}
        request = urllib2.Request(ABI_ENDPOINT,headers=headers)
        request.get_method = lambda:"GET"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        rsp = urllib2.urlopen(
        request, context=ctx, timeout=10)
        rsp = json.loads(rsp.read().decode("utf-8"))
        if rsp["message"] != "OK":
            return False
        else:
            abi = rsp["result"]
            return abi
    else:
        rsp = requests.get(ABI_ENDPOINT)
    if rsp.status_code != 200:
        return False
    rsp = rsp.json()
    try:
        abi = json.loads(rsp["result"])
        return abi
    except:
        return False
    
def classifiedMathType(_chain, functions):
    if hasattr(functions, "token0") and hasattr(functions, "token1") and hasattr(functions, "getReserves") and (functions,"kLast"):
        type = "5050_Math"
    elif hasattr(functions, "getNormalizedWeight") or hasattr(functions, "getNormalizedWeights"):
        type = "Balancer_Weighted_Math"
    elif hasattr(functions, "slot0") and hasattr(functions, "feeGrowthGlobal0X128") and hasattr(functions, "feeGrowthGlobal1X128"): # UniswapV3 (ETH), PancakeSwap V3 (ETH, BSC)
        type = "UniswapV3 Math 1"
    elif hasattr(functions, "globalState") and hasattr(functions, "totalFeeGrowth0Token") and hasattr(functions, "totalFeeGrowth1Token"): # Quickswap V3 (Polygon)
        type = "UniswapV3 Math 2"    
    elif hasattr(functions, "getPoolState") and hasattr(functions, "getLiquidityState"): # KyberSwap Elastic (AVAX)
        type = "UniswapV3 Math 3" 
    elif hasattr(functions, "state") and hasattr(functions, "feeScaleX_128") and hasattr(functions, "feeScaleY_128"):
        type = "Izumi Math"
    elif hasattr(functions, "A") and hasattr(functions, "gamma"):
        type = "Curve_V2_Crypo_Math"
    elif hasattr(functions, "A") or hasattr(functions, "getAmplificationParameter") or hasattr(functions, "AmplificiationParameter"):
        type = "Curve_V1_Stable_Math"
    else:
        type = "unclassified"
    return type


    if hasattr(functions, "token0") and hasattr(functions, "token1") and hasattr(functions, "getReserves") and (functions,"kLast"):
        type = "5050_Math"
    elif hasattr(functions, "getNormalizedWeight") or hasattr(functions, "getNormalizedWeights"):
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
# def classifiedMathType(_chain, functions):
def ProxyContract(_chain, web3, contractChecksum, contract_obj):
    implementation_address = contract_obj.functions.implementation().call()
    implementation_abi_string = getABI(_chain, implementation_address)
    contract_obj = web3.eth.contract(address=contractChecksum, abi = implementation_abi_string)
    return contract_obj

def getContract_Obj(_chain, _token_address, web3):
    contractChecksum = web3.toChecksumAddress(_token_address)
    _abi = getABI(_chain, _token_address)
    if _abi:
        contract_obj = web3.eth.contract(address=contractChecksum, abi = _abi)
        functions = contract_obj.functions
        if hasattr(functions, "implementation"):
            contract_obj = ProxyContract(_chain, web3, contractChecksum, functions)
            functions = contract_obj.functions
        return contract_obj, functions, _abi
    else:
        return None

def TokenclassifyLP5050_non5050(_chain, LP_address, web3):
    LPcontract_ObjInfo = getContract_Obj(_chain, LP_address, web3)
    if LPcontract_ObjInfo:
        functions = LPcontract_ObjInfo[1]
        _type = classifiedMathType(_chain, functions)
    else:
        _type = "err_cannot_get_abi"
    return _type

def Dataclassify(df):
    chains = df["chain"].unique()
    data_result = pd.DataFrame()
    for _chain in chains:
        node_link = config["node_link"][_chain]
        web3 = Web3(Web3.HTTPProvider(node_link))
        data = df[df["chain"] == _chain]
        data["addrChecksum"] = data["addr"].apply(lambda address: web3.toChecksumAddress(address))
        data["type"] = data["addr"].apply(lambda address: TokenclassifyLP5050_non5050(_chain, address, web3))
        data_result = data_result.append(data)
    return data_result
    
def multicalContract(_chain, type = "getLPInfo"):
    abi_file = open("abi.txt", "r")
    ABI = abi_file.read()
    abi_file.close()
    node_link = config["node_link"][_chain]
    web3 = Web3(Web3.HTTPProvider(node_link))
    if _chain == "eth":
        if type == "getWalletBalances":
            contract = config["multiContract"][_chain][1]
        else:
            contract = config["multiContract"][_chain][0]
    else:
        contract = config["multiContract"][_chain]
    multi_address = web3.toChecksumAddress(contract)
    multiContract = web3.eth.contract(address=multi_address, abi = ABI)
    return multiContract

def multical5050LPInfo(df: pd.DataFrame):
    """
    df = df[df["type"] == "5050_Math"]
    """
    df = df[df["type"] == "5050_Math"]
    chains = df["chain"].unique()
    # Create result_data = LP info from multiContract
    result_data = {}
    for _chain in  chains:
        _data = df[df["chain"] == _chain]
        list_5050 = list(_data["addrChecksum"].unique())
        multiContract = multicalContract(_chain)
        result = multiContract.functions.getLPInfo(list_5050).call()
        result_data[_chain] = result
    data = pd.DataFrame()
    for _chain in chains:
        _result_data = result_data[_chain]
        _dict_result = {}
        data_df = df[df["chain"] == _chain]
        for _item in _result_data:
            _dict_result[_item[0]] = _item
        data_df["info"] = data_df["addrChecksum"].apply(lambda address: _dict_result[address])
        data = data.append(data_df)
    data["token0"] = data["info"].apply(lambda info: info[1])    
    data["token1"] = data["info"].apply(lambda info: info[2])
    data["symbol"] = data["info"].apply(lambda info: info[7])
    data_result = pd.DataFrame()
    for _chain in chains:
        print(f"_Processing {_chain}")
        _data = data[data["chain"] == _chain]
        _multiContract = multicalContract(_chain,type = "getWalletBalances")
        _data["raw_underlying_info"] = _data.apply(lambda _data: _multiContract.functions.getWalletBalances(eval([_data["addrChecksum"]]), eval[_data["token0"], _data["token1"]]).call(), axis=1)
        data_result = data_result.append(_data)
    return data_result

def convertMulti5050Result(df: pd.DataFrame):
    df = df[df["type"]== "5050_Math"]
    result_data = multical5050LPInfo(df)
    chains = df["chain"].unique()
    data = pd.DataFrame()
    for _chain in chains:
        _result_data = result_data[_chain]
        _dict_result = {}
        data_df = df[df["chain"] == _chain]
        for _item in _result_data:
            _dict_result[_item[0]] = _item
        data_df["info"] = data_df["addrChecksum"].apply(lambda address: _dict_result[address])
        data = data.append(data_df)
    data["token0"] = data["info"].apply(lambda info: info[1])    
    data["token1"] = data["info"].apply(lambda info: info[2])
    data["symbol"] = data["info"].apply(lambda info: info[7])
    data.to_csv("5050.csv")  
    return data

if __name__ == "__main__":
    
    df = pd.read_csv("123.csv")
    df = Dataclassify(df)
    print()

