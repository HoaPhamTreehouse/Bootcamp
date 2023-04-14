from api import get_API
from getPair import getPair_AmberSupport
from latestPrice import exc_support

exc_support = {
    'spot':  ['binance', 'kraken',  'bybit', 'okex'],
    'futures': ['binance', 'kraken', 'deribit', 'bybit', 'okex'],
    'options': ['deribit'],
    'swaps': ['okex']
}
def getAmber_API_historical(exchange, instrument, market_type,
                            startDate = 1675347155,
                            endDate = 1675350755):
    if exchange not in exc_support[market_type]:
        print('Amber API does not support for {exchange} in {market_type}')
        return None
    else:
        amber_base_url = f'https://web3api.io/api/v2'
        header = {
            'accept': 'application/json',
            'x-api-key': 'UAK2737ca7c451e145cfccc825dc428dec0'
        }
        end_point = f'/market/{market_type}/tickers/{instrument}/historical'
        param = f'?exchange={exchange}'
        param += f'&startDate={startDate}&endDate={endDate}'
        url = amber_base_url + end_point + param
        data = get_API(url, header = header)
        data = data['payload']['data']
        price_list = []
        if len(data) > 0:
            if market_type == 'spot':
                for _item in data[exchange]:
                    price_list.append({
                        'timestamps': _item[0],
                        'bidPrice': _item[1],
                        'askPrice': _item[2],
                        'midPrice': _item[3],
                        'lastPrice': _item[4],
                        })
            else:
                for _item in data:
                    price_list.append({
                        'timestamps': _item['timestamp'],
                        'bidPrice': _item['bid'],
                        'askPrice': _item['ask'],
                        'midPrice': _item['mid'],
                        'lastPrice': _item['last'],
                        })
        else:
            print(f'Data return None')
            return None
    return price_list

if __name__ == '__main__':
    exchange = 'binance'
    # instrument = 'BTCUSDT'
    market_type = 'spot'
    startDate = 1677770695
    endDate = 1677771755
    # print(instrument, ': ', getAmber_API_historical(exchange, instrument, market_type, startDate, endDate))
    pair_list = getPair_AmberSupport(market_type)[exchange]
    for instrument in pair_list[:1]:
        print(instrument, ': ', getAmber_API_historical(exchange, instrument, market_type, startDate, endDate))
    # print()