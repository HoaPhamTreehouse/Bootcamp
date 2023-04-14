import pandas as pd
import requests
import json
from kraren import ApiMethods
from bybit import test_bybit_api
from coinbase import main


def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)

# def getInfo_binance():
def getInfo_binance(base_url,api_link):
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    data = get_API(base_url + api_link , headers)
    df = pd.DataFrame(data['symbols'])#[['symbol', 'permissions']]
    return df['symbol'].to_list()

def getInfo_kraken():
    public_key = "3TQIuMPJQpgrZWOvcRptY9X3hxJ8aQFivK2GKTE1mfvx7dxLQaZYe8xs"
    private_key = "0VrzZFKwwekCi3q7sOwlSkEDtx0QLrI4I+zw4Dx1rvhwPUIVJuoi0klqOvGf5lybEQDgzwRo4GiGuxXoFje+PcAH"
    apiPath = "https://futures.kraken.com"

    path_url = '/derivatives/api/v3/instruments'
    method = 'GET'
    cfApi = ApiMethods(apiPath=apiPath, timeout=20,
                       apiPrivateKey=private_key, apiPublicKey=public_key)
    result = cfApi.get_api(path_url, method)
    result = eval(result)['result']
    df = pd.DataFrame(result.keys())
    return df[0].to_list()

def getInfo_coinbase():
    coinbase_base_url = f'https://api.exchange.coinbase.com'
    path_url = f'/products'
    result = main(coinbase_base_url, path_url)
    return pd.DataFrame(result)['id'].tolist()

def getInfo_bybit():
    category = f'inverse'
    base_url = f'https://api.bybit.com'
    path_url = f'/v5/market/instruments-info?category={category}'
    method = 'GET'

    api_info = {'api_secret': "3NUVv2m9qN3s8yyrCozfFyNRrG0Iu6yHgNuD",
                'api_key': "YbrUqa61ZyZY1hJP10"}
    result = test_bybit_api(base_url, api_info, method, path_url)
    df = pd.DataFrame(result['result']['list'])
    return pd.DataFrame(result['result']['list'])['symbol'].to_list()

def getInfo(exchange):
    _func = f"getInfo_{exchange}()"
    data = eval(_func)
    return data

if __name__ == "__main__":
    # base_url = f"https://fapi.binance.com"
    # path_url = f"/fapi/v1/exchangeInfo"
    df = getInfo_bybit()
    # https://api.bybit.com/v5/market/instruments-info?category=linear
    # https://api-testnet.bybit.com/v5/market/instruments-info?category=linear
    # df1 = getInfo_bybit("https://api.bybit.com", "/v5/market/instruments-info?category=option")
    # df2 = getInfo_bybit("https://api-testnet.bybit.com", "/v5/market/instruments-info?category=option")
    # list_ = []
    # for _pair in df1:
    #     if _pair not in df2:
    #         list_.append(_pair)
    print()
    print(getInfo('kraken'))