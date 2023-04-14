import pandas as pd
import requests
import json
from kraren import ApiMethods
from bybit import test_bybit_api
from coinbase import main
from getTickerInfo import getInfo


def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)


def getHistoricalPrice_binance(symbol, interval, startTime, limit = 1000):
    '''
    startTime in mstimestamp
     maximum return: default 500, max 1000
     interval: 1m-1h-1d-1m...
    '''
    startTime = startTime * 1000
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    base_url = f'https://data.binance.com'
    api_link = f'/api/v3/klines'

    param = f'?symbol={symbol}'
    param += f'&interval={interval}&startTime={startTime}&limit={limit}'
    result = get_API(base_url + api_link + param, headers)
    data = pd.DataFrame(result)[[0, 4]].rename(columns = {0: 'timestamp', 4: 'lastPrice'})
    data['symbol'] = symbol
    return data

def getHistoricalPrice_kraren(symbol, interval, startTime):
    '''
     maximum return: 720 items
     interval : 1 5 15 30 60 240 1440 10080 21600
    '''
    public_key = "3TQIuMPJQpgrZWOvcRptY9X3hxJ8aQFivK2GKTE1mfvx7dxLQaZYe8xs"
    private_key = "0VrzZFKwwekCi3q7sOwlSkEDtx0QLrI4I+zw4Dx1rvhwPUIVJuoi0klqOvGf5lybEQDgzwRo4GiGuxXoFje+PcAH"
    apiPath = "https://api.kraken.com/0"

    path_url = '/public/OHLC'
    path_url += f'?pair={symbol}&interval={interval}&since={startTime}'
    method = 'GET'
    cfApi = ApiMethods(apiPath=apiPath, timeout=20,
                       apiPrivateKey=private_key, apiPublicKey=public_key)
    result = cfApi.get_api(path_url, method)
    try:
        result = eval(result)['result']
        _value = list(result.items())[0][1]
        closePrice = [_item[4] for _item in _value ]
        timestamp = [_item[0] for _item in _value ]
        data = pd.DataFrame(list(zip(closePrice,timestamp)), columns= ['closePrice', 'timestamp'])
        data['symbol'] = symbol
        return data
    except:
        print(eval(result)['error'])
        return None
    

def getHistoricalPrice_coinbase(symbol, interval, startTime):
    '''
    maximum return: 300 items
    granularity: 60, 300, 900, 3600, 21600, 86400
    '''
    coinbase_base_url = f'https://api.exchange.coinbase.com'
    path_url =  f'/products/{symbol}/candles'
    path_url += f'?granularity={interval}&start={startTime}'
    result = main(coinbase_base_url, path_url)
    print(result)
    closePrice = [_item[4] for _item in result ]
    timestamp = [_item[0] for _item in result ]
    data = pd.DataFrame(list(zip(closePrice,timestamp)), columns= ['closePrice', 'timestamp'])
    data['symbol'] = symbol
    return data

def getHistoricalPrice_bybit(symbol, interval, startTime):
    '''
    The start timestamp (ms)
    maxinmum return: 200 items
    '''
    startTime  = startTime * 1000
    base_url = 'https://api-testnet.bybit.com'
    path = '/v5/market/kline'
    param = f'category=inverse&symbol={symbol}&interval={interval}&start={startTime}'
    path_url = path + '?' + param
    method = 'GET'
    api_info = {'api_secret': "3NUVv2m9qN3s8yyrCozfFyNRrG0Iu6yHgNuD",
                'api_key': "YbrUqa61ZyZY1hJP10"}
    result = test_bybit_api(base_url, api_info, method, path_url)
    try:
        _value = result['result']['list']
        closePrice = [_item[4] for _item in _value ]
        timestamp = [_item[0] for _item in _value ]
        data = pd.DataFrame(list(zip(closePrice,timestamp)), columns= ['closePrice', 'timestamp'])
        data['symbol'] = symbol
        return data
    except:
        print(result['retMsg'])
        return None
    
def getHistoricalPrice(exchange, symbol, interval, startTime):
    _func = f"getHistoricalPrice_{exchange}('{symbol}', '{interval}', {startTime})"
    data = eval(_func)
    return data

if __name__ == "__main__":
    getHistoricalPrice_coinbase()
    # list_CEX = ['coinbase']
    # for exchange in list_CEX:
    #     list_pair = getInfo(exchange)
    #     for symbol in list_pair[3:]:
    #         print(getHistoricalPrice(exchange, symbol, '60', startTime=149904000))
    #     print()
    # print(getHistoricalPrice('binance', 'BNBBTC', '1s' , startTime=149904000))