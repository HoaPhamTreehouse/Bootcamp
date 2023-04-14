import pandas as pd
import json
import requests


api_link = f'https://api.llama.fi/protocols'
data = json.loads(requests.get(api_link).text)
df1 = pd.DataFrame(data)[['name', 'category' ,'chainTvls']]
df1 = [(r['name'], r['category'], k, v) for _, r in df1.iterrows() for k, v in r['chainTvls'].items()]
df1 = pd.DataFrame(df1, columns=['Name', 'category', 'Chain', 'TVL']).sort_values('TVL').reset_index(drop=True)

min_tvl = df1['TVL'].min()
max_tvl = df1['TVL'].max()

df1['indexTVL'] = df1['TVL'].apply(lambda tvl: 1 - (tvl - min_tvl)/(max_tvl - min_tvl))
df1 = df1.sort_values('indexTVL').reset_index(drop= True)
df1.to_csv('TVL_from_defilama.csv')
# df2 = pd.read_excel('protocol_old.xlsx')
# merge_data = pd.merge(df1, df2, how = 'left', on = ['Name', 'Chain'])
# merge_data = merge_data.drop_duplicates()
# merge_data[merge_data['Chain'] == 'Multi-Chain'].to_csv('multi_chain.csv')
# merge_data = merge_data[merge_data['Chain'] != 'Multi-Chain']
# merge_data.to_csv('merge_data.csv')
print()