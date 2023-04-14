import pandas as pd
import requests
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)


def getTop50Pair():
    base_url = f"https://api.binance.com"
    path_url = f"/api/v3/ticker/24hr"
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    data = get_API(base_url + path_url, headers)
    data = pd.DataFrame(data=data)[["symbol", "weightedAvgPrice", "volume"]]
    data["weightedAvgPrice"] = data["weightedAvgPrice"].astype(float)
    data["volume"] = data["volume"].astype(float)
    data["marketcap"] = data["weightedAvgPrice"] * data["volume"]
    data = data.sort_values("marketcap", ascending= False).reset_index(drop= True).head(50)
    return data['symbol'].to_list()


def getOHLC_binance(pair, interval, limit):
    base_url = f"https://api.binance.com"
    path_url = f"/api/v3/klines"
    param = f"?symbol={pair}&interval={interval}&limit={limit}"
    api_key = 'cYJ2xVgG3iRoPcCoRzUA0QOKX1gJQbIno2J6jx3qmzysYoHHAaH2IZhlen1YBPZM'
    secret_key = 'EhmFpsz8ZGzmBfPivBKgRTJ16P4LiOWBW3FqRlq13ujMf6uMK4gmgkRVjewuom9S'
    headers = {
            'content-type': 'application/json',
            'X-MBX-APIKEY': api_key
        }
    
    data = get_API(base_url + path_url + param , headers)
    columns = ["open_timestamp", "Open", "High", "Low", "Close", "Volume", "close_timestamp", "Quote_asset_volume", "Number_of_trades", "base_asset_volume", "quote_asset_volume", "ignore"]
    df = pd.DataFrame(data, columns=columns)
    return df

def convertOHLC_Data(pair, interval, limit):
    data = getOHLC_binance(pair, interval, limit)
    data["open_timestamp"] = data["open_timestamp"]/1000
    data["Date"] = [datetime.fromtimestamp(x) for x in data["open_timestamp"]]
    data=data.set_index('Date')
    data['Open'] = data['Open'].astype(float)
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)
    data['Volume'] = data['Volume'].astype(float)
    return data



def OHLC_Candlestick_chart(pair, interval, limit):
    data = convertOHLC_Data(pair, interval, limit)
    color = ["#82c2b4" if close_price < open_price else "#dca8ad" for close_price, open_price in zip(data["Open"], data["Close"])]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.001,
                subplot_titles=(f'OHLC Candlestick chart: {pair} - {interval} - {limit} items', 'Volume'), 
                )
    candlestick = go.Candlestick(
                                x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                type = "candlestick",
                                )
    fig.add_trace(candlestick, row=1, col=1)
    fig.update_yaxes(fixedrange=False)

    # Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=data.index,
                         y=data['Volume'],
                         showlegend=False,
                         marker_color= color),
                         row=2, col=1,
                        )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(width=1500, height=800)
    fig.show()
    return fig

if __name__ == "__main__":
    pair = "BTCUSDT"
    interval = "1h"
    limit = 1000
    OHLC_Candlestick_chart(pair, interval, limit)
    # list_pair = getTop50Pair()
    # for _pair in list_pair:
    #     OHLC_Candlestick_chart(_pair, interval, limit)