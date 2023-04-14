from web3 import Web3
from utils.config import defaultConfig
_defaultConfig = defaultConfig()
node_link = [http_node['nr'] for http_node in _defaultConfig['eth'] if 'nr' in http_node][0]
web3 = Web3(Web3.HTTPProvider(node_link))
print(web3.eth.get_code('0x8c73d39b2da2dd1a10cc16502bc7c8d768ec74c9'))