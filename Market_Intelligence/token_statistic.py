import requests
import json
import pandas as pd

api_doc_link = f"https://www.coingecko.com/en/api/documentation"

def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)

def getCoin_list():
    base_url = f"https://api.coingecko.com/api/v3"
    path_url = f"/coins/list"
    header = {"accept": "application/json"}
    rsp = get_API(base_url + path_url, header)
    data = pd.DataFrame(rsp)
    return data

def getCoinInfo(type = 1):
    # lenght = getCoin_list().shape[0]
    price_change_percentage = "1h,24h,7d"
    per_page = 250
    page = 1
    base_url = f"https://api.coingecko.com/api/v3"
    param = f"&price_change_percentage={price_change_percentage}"
    header = {"accept": "application/json"}
    path_url = f"/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=false&locale=en"
    rsp = get_API(base_url + path_url + param, header)
    if type == 1:
        data = pd.DataFrame(rsp)[['id', 'symbol','current_price',
                 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency','price_change_percentage_7d_in_currency',
                 'ath', 'total_volume', 'market_cap', 'fully_diluted_valuation']]
        data.columns = ['id', 'symbol','Price',
                 '1h', '24h','7d',
                 'ATH', '24h Volume', 'Mkt Cap', 'FDV']
        data["Market Cap ÷ FDV"] = data["Mkt Cap"]/data["FDV"]
    else:
        data = pd.DataFrame(rsp)[['id', 'symbol', 'circulating_supply', 'total_supply','max_supply']]
        data.columns = ['id', 'symbol', 'Circulating', 'Total','Max Token Supply']
    # #--------
    # data = pd.DataFrame()
    # while page < 5:
    #     print(page)
    #     path_url = f"/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=false&locale=en"
    #     rsp = get_API(base_url + path_url + param, header)
    #     _data = pd.DataFrame(rsp)[['id', 'symbol','circulating_supply', 'total_supply','max_supply']]
    #     # _data = pd.DataFrame(rsp)[['id', 'symbol','current_price',
    #     #          'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency','price_change_percentage_7d_in_currency',
    #     #          'ath', 'total_volume', 'market_cap', 'fully_diluted_valuation']]
    #     data = data.append(_data)
    #     page += 1
    # data.columns = ['id', 'symbol', 'Circulating Supply', 'Total Supply','Max Token Supply']
    # #--------
    return data

if __name__ == "__main__":
    pair = "bitcoin"
    data = getCoinInfo()
    print()