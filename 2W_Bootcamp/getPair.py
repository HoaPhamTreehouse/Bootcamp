import pandas as pd
from api import get_API

def getPair_AmberSupport(market_type):
    amber_base_url = f'https://web3api.io/api/v2'
    header = {
        'accept': 'application/json',
        'x-api-key': 'UAK2737ca7c451e145cfccc825dc428dec0'
    }
    if market_type == 'spot':
        end_point = f'/market/exchanges'
    else:
        end_point = f'/market/{market_type}/exchanges/information'
    url = amber_base_url + end_point
    data = get_API(url, header = header)
    data = data['payload']['data']
    dict_pair = {}
    for _key, _pair_data in data.items():
        dict_pair[_key] = list(_pair_data.keys())
    df = pd.DataFrame.from_dict(dict_pair, orient='index')
    df = df.transpose()
    df.to_csv(f'{market_type}.csv')  
    return df

if __name__ == '__main__':
    market_type = 'options'
    print(getPair_AmberSupport(market_type))
    print()