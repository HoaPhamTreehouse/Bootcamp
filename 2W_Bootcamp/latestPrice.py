from api import get_API
from coinbase import main
from getPair import getPair_AmberSupport

exc_support = {
    'spot':  ['binance', 'kraken',  'bybit', 'okex'],
    'futures': ['binance', 'kraken', 'deribit', 'bybit', 'okex'],
    'options': ['deribit'],
    'swaps': ['okex']
}

def getAmber_API(exchange, instrument, market_type):
    if exchange == 'coinbase':
        if market_type != 'spot':
            print(f'Coinbase does not support {market_type}')
            return None
        else:
            # instrument = instrument.replace('_', '-')
            coinbase_base_url = f'https://api.exchange.coinbase.com'
            path_url = f'/products/{instrument}/ticker'
            data = main(coinbase_base_url, path_url)
            print()
    else:
        if exchange not in exc_support[market_type]:
            print('Amber API does not support for {exchange} in {market_type}')
            return None
        else:
            # instrument = instrument.replace('-', '_')
            amber_base_url = f'https://web3api.io/api/v2'
            header = {
                'accept': 'application/json',
                'x-api-key': 'UAK2737ca7c451e145cfccc825dc428dec0'
            }
            end_point = f'/market/{market_type}/tickers/{instrument}/latest'
            param = f'?exchange={exchange}'
            url = amber_base_url + end_point + param
            data = get_API(url, header = header)
            data = data['payload']
            price_dict = {}
            if len(data) > 0:
                if market_type == 'spot':
                    price_dict['bid'] = data[exchange]['bid']
                    price_dict['ask'] = data[exchange]['ask']
                    price_dict['mid'] = data[exchange]['mid']
                    price_dict['last'] = data[exchange]['last']
                else:
                    price_dict['bid'] = data[0]['bid']
                    price_dict['ask'] = data[0]['ask']
                    price_dict['mid'] = data[0]['mid']
                    price_dict['last'] = data[0]['last']
            else:
                print(f'Data return None')
                return None

    return price_dict

if __name__ == '__main__':
    exchange = 'deribit'
    # instrument = 'eth_usdt'
    market_type = 'FUTURES'.lower()
    pair_list = getPair_AmberSupport(market_type)[exchange]
    for instrument in pair_list[21:]:
        print(instrument, ': ', getAmber_API(exchange, instrument, market_type))
    print()
