import pandas as pd
from api import get_API

header = {
    'accept': 'application/json',
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2Nzc2NTc4OTQ2ODAsImVtYWlsIjoiSG9hcGhhbS5wdGhAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiaWF0IjoxNjc3NjU3ODk0fQ.z-yBK1hTUyLOp5BpAqNwoZ9Ob2mZQPVHd3CDejT-tIw'
}
offset = 0
limit = 100
url = f'https://public-api.solscan.io/token/list?sortBy=market_cap&direction=desc&limit={limit}&offset={offset}'

raw_data = get_API(url, header)
data = pd.DataFrame()
total = raw_data['total']
while offset < total:
    url = f'https://public-api.solscan.io/token/list?sortBy=market_cap&direction=desc&limit={limit}&offset={offset}'
    raw_data = get_API(url, header)
    data = data.append(raw_data['data'])
    offset += limit
    print(offset)
    
# #### Get token holders
# token_address = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
# api_link = f'https://public-api.solscan.io/token/holders?tokenAddress={token_address}&limit=10&offset=0'
# raw_data = get_API(api_link, header)

print()