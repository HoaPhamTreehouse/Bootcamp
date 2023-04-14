import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api import get_API

def getLatestPrice_Binance():
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    base_url = f'https://data.binance.com'
    api_link = f'/api/v3/ticker/24hr'
    param = '?ETHBTC'

    data = get_API(base_url + api_link + param, headers)
    df = pd.DataFrame(data)
    return df

print()