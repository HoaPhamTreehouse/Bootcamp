from itertools import chain
from pymongo import MongoClient
from influxdb_client import InfluxDBClient
import time
import requests, os, pytz
import sys
import ssl
from datetime import datetime, timedelta
from datetime import time as dttime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from pos_db.hdb import getEODBid
from classes.Web3Call import Web3Call
# utils_dir = os.path.dirname(os.path.realpath(__file__))
# repo_dir = os.path.abspath(os.path.join(utils_dir, os.path.pardir))
# output_dir = os.path.join(repo_dir, "output")
# os.makedirs(output_dir, exist_ok=True)


# influx_setting
influx_setting = {
        "token_api":"lBHU_Oi_vvPRlVCi_4b1qw683wTZY3JQsLHzTvrxymR99jQYdDG0g5FbiUxnqcdLhKat-XnxAMtaKPQKA4AxZw==",
        "url":"http://influx.treehouse.finance:8086",
        "bucket":"pricings-prd",
        "measurement":"token_pricing"}
api_token = influx_setting['token_api']
influx_client = InfluxDBClient(url=influx_setting['url'], token=api_token, org="treehouse")
bucket = influx_setting['bucket']
measurement = influx_setting['measurement']

rdb_link = f'mongodb+srv://product:07EVvoAuNGVMaScs07EVvoAuNGVMaScs@prd3-rdb.5wv0x.mongodb.net/'
hdb_link = f'mongodb+srv://product:07EVvoAuNGVMaScs07EVvoAuNGVMaScs@prd3-hdb.5wv0x.mongodb.net/'
rdb_price = MongoClient(rdb_link, ssl_cert_reqs=ssl.CERT_NONE)['treehouse']['rdb_price']
hdb_price = MongoClient(hdb_link, ssl_cert_reqs=ssl.CERT_NONE)['treehouse']['hdb_price']

#pricing_db
pricingdb_link = f'mongodb+srv://product:07EVvoAuNGVMaScs07EVvoAuNGVMaScs@clusterpricing.5wv0x.mongodb.net/'
pricing_db = MongoClient(pricingdb_link, ssl_cert_reqs=ssl.CERT_NONE)
pricing_rdb = pricing_db['treehouse_token_price']['current_price_cmc_v2']
pricing_hdb = pricing_db['treehouse_token_price']['historical_price_cmc_v2']
token_lstdb = pricing_db['treehouse_token_price']['coin_list_cmc_v2']

# Cache db
cache_db = MongoClient(f'mongodb+srv://product:07EVvoAuNGVMaScs07EVvoAuNGVMaScs@prd3-cache.5wv0x.mongodb.net/',ssl_cert_reqs=ssl.CERT_NONE)
tkn_mapping = cache_db['treehouse_pricing']['tkn_mapping']

def contract_db(chain):
    if chain == 'eth':
        contractdb_link = f'mongodb://treehouse_ro:%25EEjCC4q4%3F%262ux%40E@10.148.15.240/?authMechanism=DEFAULT&authSource=treehouse'
    elif chain == 'bsc':
        contractdb_link = f'mongodb://mgo_ro:PWcZ%25uK%26uwLe5B%2B2@10.148.15.212/?authMechanism=DEFAULT&authSource=admin'
    elif chain == 'avax':
        contractdb_link = f'mongodb://treehouse_ro:F83Yb9qmZArQTrqV@10.148.0.70/?authMechanism=DEFAULT&authSource=admin'
    contractdb = MongoClient(contractdb_link, ssl_cert_reqs=ssl.CERT_NONE)['treehouse']['contract']
    return contractdb

# map_block_date db
def map_block_date(chain):
    db_link = f'mongodb://treehouse_ro:CLpjnRW79z53Ee7f@10.148.1.48/?authMechanism=DEFAULT&authSource=admin'
    db_connect = MongoClient(db_link, ssl_cert_reqs=ssl.CERT_NONE)
    db = db_connect[f'{chain}_mapblockdate']['map_block_date']
    return db

# block db
def block_db(chain):
    db_link = f'mongodb://treehouse_ro:CLpjnRW79z53Ee7f@10.148.1.48/?authMechanism=DEFAULT&authSource=admin'
    db_connect = MongoClient(db_link, ssl_cert_reqs=ssl.CERT_NONE)
    db = db_connect[f'{chain}_block']['block']
    return db
    
# conver Bid to timestamp using for get price in Influx db
def convBid2Ts(_bid, chain):
    # make sure the _block_number is a string
    _tb = block_db(chain)
    bid = int(_bid)
    try:
        query = _tb.find_one({"block_int": bid})
        assert query is not None
        tstamp = int(query.get("timestamp", 1))
    except:
        tstamp = 1
        print(f"Block {bid} not found in block collection | {str(sys.exc_info())}")
    return tstamp

# get start and end time to query Influx db
def get_start_and_end_time(dt=None):
    if dt is None:
        dt = datetime.today()
    start = datetime.combine(dt, dttime.min).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.combine(dt, dttime.max).strftime("%Y-%m-%dT%H:%M:%SZ")
    return start, end

def get_price_Influx_db(chain, token_address, block = None):
    if block == '' or block is None:
        dt=None
    else:
        tstamp = convBid2Ts(_bid = block, chain = chain)
        map_block_date_db = map_block_date(chain=chain)
        yesterday_date = (datetime.utcnow() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        block_data = map_block_date_db.find_one({"date": yesterday_date})
        yesterday_EOD_block = float(block_data['end_block'])
        dt = datetime.utcfromtimestamp(convBid2Ts(_bid = block, chain = chain))
        if tstamp == 1:
            latest_block = Web3Call.getLatest(chain= chain)
            if (block <= latest_block) and (block > yesterday_EOD_block): #
                dt = None
            else:
                raise Exception(f"Please check your block {block} from pricing")
        else:
            dt = datetime.utcfromtimestamp(tstamp)
    return_dict = {}
    

    # To obtain the tkn, first query the table pricing_src. 
    _day = (datetime.utcnow() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    rsp = tkn_mapping.find_one({"date": _day, "chain": chain, "addr": token_address})
    if rsp is None:
        print(f'{token_address} is not in tkn_mapping!!!')
        return None, None
    sday, eday = get_start_and_end_time(dt)
    query = f'from(bucket: "{bucket}")\
    |> range(start: {sday}, stop: {eday})\
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")\
    |> filter(fn: (r) => r["_field"] == "prc")\
    |> filter(fn: (r) => r["tkn"] == "{rsp["tkn"]}")\
    |> last()'

    query_api = influx_client.query_api()
    records = query_api.query(query=query)
    for i in records:
        return_dict[i.records[0].values["src"]] = i.records[0].values["_value"]
    if len(return_dict) >0:
        for s in ['coingecko','coinmarketcap','1inch']:
            price = return_dict.get(s)
            if price is not None:
                provider = s
                return price, provider
    else:
        return None


def getPrice_fromdb(chain, token_address, block=None):

    price = None
    try:
        if block == "" or block is None:  # real-time
            ret = rdb_price.find({"token": token_address.lower(), "chain": chain})
            if ret.count() == 0:
                price = None
                return price
            else:
                for r in ret:
                    price = r["price"]
        else:
            ret = hdb_price.find(
                {"token": token_address.lower(), "block": str(block), "chain": chain}
            )
            if ret.count() == 0:
                price = None
                return price
            else:
                for r in ret:
                    price = r["price"]
    except:
        price = None
    return price



def getPrice_db_API(chain, token_address, block=None):
    price = getPrice_fromdb(chain, token_address, block=block)
    if price == None:
        price = get_price_Influx_db(chain, token_address, block=block)[0]
    return price

