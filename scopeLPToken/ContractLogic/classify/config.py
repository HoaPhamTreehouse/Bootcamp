from pymongo import MongoClient
import ssl


def smartContract(_chain):
    smartContract_dict = {
    "eth": ["0xcc49997cc2a3ef4ccb86c449d2852fe81d3cbd5c", "0x67e7dfFfA35Bb998b82B60caE2D9a73fB25c63c4"],
    "bsc": "0x461D387586Bcd572E06319B4d279F389994e7e45",
    "avax": "0x2d68DD989E77f6EBC48128C77Bb0Aba41a46039C",
    "optimism": "0xbcFd5aC09cf9E9e338a31F068eb4b7883f8F521C",
    "polygon": "0x25FC73fdd66d80cB423b64cA9BEa146c62a89EE5",
    "arbitrum": "0x25FC73fdd66d80cB423b64cA9BEa146c62a89EE5",
    # "cro": "0xffe60C13e7D32d26CD6F8188f535BCa026cBF0Cf",
    # "fantom": "0xffe60C13e7D32d26CD6F8188f535BCa026cBF0Cf",
    # "klay": "0xffe60C13e7D32d26CD6F8188f535BCa026cBF0Cf",
    # "heco": "0xffe60C13e7D32d26CD6F8188f535BCa026cBF0Cf",
    }
    return smartContract_dict[_chain]

def contract_db(_chain):
    if _chain == 'eth':
        contractdb_link = f'mongodb://treehouse_ro:%25EEjCC4q4%3F%262ux%40E@10.148.15.240/?authMechanism=DEFAULT&authSource=treehouse'
    elif _chain == 'bsc':
        contractdb_link = f'mongodb://mgo_ro:PWcZ%25uK%26uwLe5B%2B2@10.148.15.212/?authMechanism=DEFAULT&authSource=admin'
    elif _chain == 'avax':
        contractdb_link = f'mongodb://treehouse_ro:F83Yb9qmZArQTrqV@10.148.0.70/?authMechanism=DEFAULT&authSource=admin'
    contractdb = MongoClient(contractdb_link, ssl_cert_reqs=ssl.CERT_NONE)['treehouse']['contract']
    return contractdb

def getNodeLink(_chain):
    node_link_dict = {
                "polygon": f"https://polygon.w3node.com/77e0b9890e05bb7a99c511ca3fe5d0573e26797b398045a58e5b94ff704ce865/api",
                "arbitrum": f"https://full-arbitrum.w3node.com/bcb556d86d6f90e4159166941a5fa7cb5d021ec72920c13a027cdab740c344c2/api",
                "optimism": f"https://optimism.w3node.com/19ca9e550ba2cb129a801abf38910eadc1693ae2f1171709012fe2473a33ac35/api",
                "eth": f"http://harvest-eth-archive.treehouse.finance",
                # "bsc": f"http://harvest-bsc-archive.treehouse.finance",
                "bsc": "https://bsc-mainnet.nodereal.io/v1/321b4758037246f79735b32a830921c8",
                "avax": f"http://harvest-avax-archive.treehouse.finance/ext/bc/C/rpc",
    }
    return node_link_dict[_chain]

def API_key(_chain):
    APIKey_dict = {
        "polygon": f"I2S28HBWEJE7CTCBDPHTD3DSRBYEDQ7BF8",
        "arbitrum": f"XU3YPHFPWX55F2A8B7UJ8IKVPC3GG2DR3X",
        "optimism": f"48GTPBXR3GNN1296XERDZIRZ8Y7K52M3RP", 
        "eth": f"978JTWN7MXDSZFI2TI5YTFD9GV6AXZJVJU",
        "bsc": f"F723GDNT8KWRI7XVUNGXYC22FMDY6DKD6M",
        "avax": f"9M41NESN9SQNYRCWJRVW8VSDFNIXCQEC18"
    }
    return APIKey_dict[_chain]

def getAPI_io(_chain):
    getscan_io_dict = {
        "polygon": f".polygonscan.com",
        "arbitrum": f".arbiscan.io",
        "optimism": f"-optimistic.etherscan.io", 
        "eth": f".etherscan.io",
        "bsc": f".bscscan.com",
        "avax": f".snowtrace.io"
    }
    return getscan_io_dict[_chain]

# def getLLProtocolInfo():
#     import pandas as pd
#     df = pd.read_csv("synthetic.csv")
#     dict_LPInfo = {}
#     for _index in df.index:
#         addr = df.loc[_index]["addr"]
#         chain = df.loc[_index]["chain"]
#         protocol_name = df.loc[_index]["protocol_name"]
#         dict_LPInfo[addr] = [chain, protocol_name]
#     return dict_LPInfo

def other_case():
    implementation_return_None = [
        
    ]

eth_list_LP = [
    "0xddcb1663cc71937fb1e6052874484383ea80d01b",
"0xddcb1663cc71937fb1e6052874484383ea80d01b",
"0x160532d2536175d65c03b97b0630a9802c274dad",
"0xc4e595acdd7d12fec385e5da5d43160e8a0bac0e",
"0xab08b0c9dadc343d3795dae5973925c3b6e39977",
"0x369582d2010b6ed950b571f4101e3bb9b554876f",
"0x5786b267d35f9d011c4750e0b0ba584e1fdbead1",
"0xde990994309bc08e57aca82b1a19170ad84323e8",
"0xadbf1854e5883eb8aa7baf50705338739e558e5b",
"0x6e7a5fafcec6bb1e78bae2a1f0b612012bf14827",
"0x9803c7ae526049210a1725f7487af26fe2c24614",
"0xdc9232e2df177d7a12fdff6ecbab114e2231198d",
"0x3902b89e0e28a23f82086b87bb81ef5a1eabf276",
"0x853ee4b2a13f8a742d64c8f088be7ba2131f670d",
"0x6cf8654e85ab489ca7e70189046d507eba233613",
"0x304e57c752e854e9a233ae82fcc42f7568b81180",
"0xbe40f7fff5a2235af9a8cb79a17373162efefa9c",
"0x9a8b2601760814019b7e6ee0052e25f1c623d1e6",
"0x69437901da6952da49bca49ffc923dfb82abfb16",
"0xa34ec05da1e4287fa351c74469189345990a3f0c",
"0xf04adbf75cdfc5ed26eea4bbbb991db002036bdd",
"0x604229c960e5cacf2aaeac8be68ac07ba9df81c3",
"0xd32f3139a214034a0f9777c87ee0a064c1ff6ae2",
"0xaab5254e17380511887aaba7e96a5339a519e26a",
"0x34965ba0ac2451a34a0471f04cca3f990b8dea27",
"0x096c5ccb33cfc5732bcd1f3195c13dbefc4c82f4",
"0x8975ddc1c651865af89b617e0aafd5be5a1b9076",
"0x40f0a05c8c7a86ad1491a3911c293e093fe92436",
"0x5d9ac8993b714df01d079d1b5b0b592e579ca099",
"0x7432fde7aefc64f42c87e1be943024368cf68ecd",
"0xd2105fe5f1b631daf2398e918549758cd181ca7c",
"0x71bd159cf9136d038a60f10118741dfcb10c3111",
"0x2cf7252e74036d1da831d11089d326296e64a728",
"0x5a94f81d25c73eddbdd84b84e8f6d36c58270510",
"0xfc2fc983a411c4b1e238f7eb949308cf0218c750",
"0x65d43b64e3b31965cd5ea367d4c2b94c03084797",
"0xdb995f975f1bfc3b2157495c47e4efb31196b2ca",
]

