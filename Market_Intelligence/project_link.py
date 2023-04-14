import requests
import json
import pandas as pd

def get_API(url, header = None):
    data = requests.get(url, headers= header)
    return json.loads(data.text)

def getCoinInfo(_id):
    data = {}
    base_url = f"https://api.coingecko.com/api/v3"
    path_url = f"/coins/{_id}"
    rsp = get_API(base_url + path_url)
    data["id"] = rsp["id"]
    data["symbol"] = rsp["symbol"]
    data["Contract"] = rsp.get("contract_address", None)
    data["detail_platforms"] = rsp["detail_platforms"]
    data["image"] = rsp["image"]
    data["Website"] = rsp["links"]["homepage"]
    data["Explorers"] = rsp["links"]["blockchain_site"]
    data["Community"] = rsp["links"]["chat_url"]
    data["twitter"] = "https://twitter.com/" + rsp["links"]["twitter_screen_name"]
    data["Source Code"] = rsp["links"]["repos_url"]["github"]
    return rsp
    
if __name__ == "__main__":
    id = "bitcoin"
    bitcoin = getCoinInfo(id)
    id = "arbitrum"
    arbitrum = getCoinInfo(id)
    print()


