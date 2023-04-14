import requests
import json
from kraren import ApiMethods
from bybit import test_bybit_api
from coinbase import main
from getTickerInfo import getInfo



def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)

def getLatestPrice_binance(symbol):
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    base_url = f'https://data.binance.com'
    api_link = f'/api/v3/ticker/price'

    param = f'?symbol={symbol}'
    data = get_API(base_url + api_link + param, headers)

    return {symbol: data['price']}

def getLatestPrice_kraken(symbol):
    public_key = "3TQIuMPJQpgrZWOvcRptY9X3hxJ8aQFivK2GKTE1mfvx7dxLQaZYe8xs"
    private_key = "0VrzZFKwwekCi3q7sOwlSkEDtx0QLrI4I+zw4Dx1rvhwPUIVJuoi0klqOvGf5lybEQDgzwRo4GiGuxXoFje+PcAH"
    apiPath = "https://api.kraken.com/0"
    path_url = '/public/Ticker'
    path_url += f'?pair={symbol}'
    method = 'GET'
    cfApi = ApiMethods(apiPath=apiPath, timeout=20,
                       apiPrivateKey=private_key, apiPublicKey=public_key)
    result = cfApi.get_api(path_url, method)
    result = eval(result)
    try:
        result = result['result']
        _key, _value = list(result.items())[0]
        price = _value['c'][0]
    except:
        print(result['error'])

        price = None

    return {symbol: price}

def getLatestPrice_coinbase(symbol):
    coinbase_base_url = f'https://api.exchange.coinbase.com'
    path_url = f'/products/{symbol}/ticker'
    result = main(coinbase_base_url, path_url)
    try:
        price = result['price']
    except:
        price = None
        print(result['message'])
    return {symbol: price}

def getLatestPrice_bybit(symbol):
    base_url = 'https://api-testnet.bybit.com'
    path = '/v5/market/tickers'
    param = f'category=inverse&symbol={symbol}'
    path_url = path + '?' + param
    method = 'GET'

    api_info = {'api_secret': "3NUVv2m9qN3s8yyrCozfFyNRrG0Iu6yHgNuD",
                'api_key': "YbrUqa61ZyZY1hJP10"}
    result = test_bybit_api(base_url, api_info, method, path_url)
    try:
        price = result['result']['list'][0]['lastPrice']
    except:
        print(result['retMsg'])
        price = None
    return {symbol: price}

def getLatestPrice(exchange, symbol):
    _func = f"getLatestPrice_{exchange}('{symbol}')"
    data = eval(_func)
    return data

if __name__ == "__main__":
    # print(getLatestPrice('Bybit', 'NU-USD'))
    list_CEX = ['bybit']
    # for exchange in list_CEX:
    #     list_pair = getInfo(exchange)
    #     # for symbol in list_pair:
    print(getLatestPrice('kraken', 'ACHUSD'))
    print()
    # print(getLatestPrice('kraren','XBTUSD'))