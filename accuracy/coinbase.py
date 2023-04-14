import pandas as pd
import http.client
import requests
import hmac
import hashlib
import time
import base64
import json


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


def create_signature(api_secret, timestamp, method, path_url, body):
    message = timestamp + method + path_url.split('?')[0] + body
    hmac_key = base64.b64decode(api_secret)
    signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return signature_b64


def test_coinbase_api(base_url, api_info, method, path_url):
    '''
        prepare headers, params
    '''

    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if path_url[0] != '/':
        path_url = '/' + path_url

    api_key = api_info['api_key']
    api_secret = api_info['api_secret']
    passphrase = api_info['passphrase']
    body = api_info.get('body', "")
    timestamp_int = int(time.time())
    timestamp = str(timestamp_int)

    signature_b64 = create_signature(
        api_secret, timestamp, method, path_url, body)
    headers = {
        'Content-Type': 'application/json',
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-PASSPHRASE': passphrase,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'User-Agent': 'python-requests'
    }
    rs = request_api(base_url, path_url, method, headers=headers)
    return rs


def main(base_url, path_url):

    method = 'GET'
    default_api_info = {'api_secret': "igp79+OvyMEvB7x9sYocP+6Ez+lM34aqQKW+SniRKj/p3HY9Fgf9sLS42sDy73mTcFhoOzLUzPcH9+sg42wK0g==",
                        'api_key': "42e6d1a07889c9637c13c1182f7e348e",
                        'passphrase': 'iyqez22ozth'}

    # phuc_api_info = {'api_secret': "Bj9ymEYBiFtBAUxyFiRMWqp4YDHV//vFJ5JKA4QuxoKha9qL9bRDfVha3gc7q0HwZIYaIB5nVrTgSJ8IiRwGsg==",
    #                  'api_key': "6bb1cc089f670be8ca6b4cb7ecb6400b",
    #                  'passphrase': '09ta5wc7st05'}
    phuc_api_info = {'api_secret': "otaBO/rNy/7lfCBtwiHffWGTKHH9ap0GKXwcz9Gf3O9dTJCIlGM8xOdUGoDe3zRhwNZEwWj1TzzyGMMhiaIt2w==",
                     'api_key': "fdbe235200965b2282857728dd7c0b35",
                     'passphrase': 'mptcznetjx'}
    timestamp_int = int(time.time())
    timestamp = str(timestamp_int)
    rs = test_coinbase_api(base_url, phuc_api_info, method, path_url)
    return rs




if __name__ == "__main__":
    base_url = 'api.exchange.coinbase.com'
    path = '/products/{product_id}/ticker'
    instrument = 'BTC-USD'
    print(main(instrument))
