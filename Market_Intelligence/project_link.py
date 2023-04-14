import requests
import json

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
    data["Website"] = rsp["links"]["homepage"] # Website
    data["twitter"] = "https://twitter.com/" + rsp["links"]["twitter_screen_name"] # Twitter
    data["Source Code"] = rsp["links"]["repos_url"]["github"] # Github
    return data
    
if __name__ == "__main__":
    id = "ethereum"
    ethereum = getCoinInfo(id)
    print()


