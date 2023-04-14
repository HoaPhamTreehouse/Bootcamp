import requests
import hmac
import hashlib
import time
import base64
import json
import datetime as dt


def request_api(base_url, path_url, method, _json={}, headers={}, params={}, body=''):
    if not _json:
        if method == 'GET':
            return json.loads(requests.get(base_url + path_url, headers=headers).content)
        elif method == 'POST':
            return json.loads(requests.post(base_url + path_url,
                                            headers=headers, params=params).content)
    else:
        if method == 'GET':
            return json.loads(requests.get(base_url + path_url, json=_json, headers=headers).content)
        elif method == 'POST':
            return json.loads(requests.post(base_url + path_url, json=_json,
                                            headers=headers, params=params).content)


def genSignature(time_stamp,api_key,api_secret,recv_window, payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature


def get_time():
    return dt.datetime.utcnow().isoformat()[:-3]+'Z'

def test_bybit_api(base_url, api_info, method, path_url):
    '''
        prepare headers, params
    '''

    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if path_url[0] != '/':
        path_url = '/' + path_url

    api_key = api_info['api_key']
    api_secret = api_info['api_secret']
    
    param = 'accountType=spot'
    timestamp_int = int(time.time()*1000)
    timestamp = str(timestamp_int)
    recv_window = str(5000)
    
    signature_b64 = genSignature(timestamp,api_key,api_secret,recv_window,param)

    headers = {
        'Content-Type': 'application/json',
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature_b64,
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        
    }
    rs = request_api(base_url, path_url, method, headers=headers)
    return rs

    

