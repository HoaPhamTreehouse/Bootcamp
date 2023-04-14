import time
import base64
import hashlib
import hmac
import urllib.request as urllib2
import ssl
import pandas as pd

class ApiMethods(object):
    def __init__(self, apiPath, apiPrivateKey="", apiPublicKey="", timeout=10):
        self.apiPath = apiPath
        self.apiPrivateKey = apiPrivateKey
        self.apiPublicKey = apiPublicKey
        self.timeout = timeout
        self.nonce = 0
    # important function

    def get_api(self, path_url, method):
        return self.make_request(method, path_url)

    def get_accounts(self):
        endpoint = "/derivatives/api/v3/accounts"
        return self.make_request("GET", endpoint)

    def get_tickers(self):
        endpoint = "/derivatives/api/v3/tickers"
        return self.make_request("GET", endpoint)

    def get_openpositions(self):
        endpoint = "/derivatives/api/v3/openpositions"
        return self.make_request("GET", endpoint)
    # signs a message

    def sign_message(self, endpoint, postData, nonce=""):
        if endpoint.startswith('/derivatives'):
            endpoint = endpoint[len('/derivatives'):]
        # step 1: concatenate postData, nonce + endpoint
        message = postData + nonce + endpoint

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf8'))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secretDecoded = base64.b64decode(self.apiPrivateKey)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secretDecoded, hash_digest,
                               hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64encode(hmac_digest)

    # creates a unique nonce
    def get_nonce(self):
        self.nonce = (self.nonce + 1) & 8191
        return str(int(time.time() * 1000)) + str(self.nonce).zfill(4)

    # sends an HTTP request
    def make_request_raw(self, requestType, endpoint, postUrl="", postBody=""):
        # create authentication headers
        postData = postUrl + postBody
        signature = self.sign_message(endpoint, postData)
        authentHeaders = {
            "APIKey": self.apiPublicKey, "Authent": signature}

        authentHeaders["User-Agent"] = "cf-api-python/1.0"

        # create request
        if postUrl != "":
            url = self.apiPath + endpoint + "?" + postUrl
        else:
            url = self.apiPath + endpoint

        request = urllib2.Request(url, str.encode(postBody), authentHeaders)
        request.get_method = lambda: requestType

        # read response
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib2.urlopen(
            request, context=ctx, timeout=self.timeout)

        # return
        return response

    # sends an HTTP request and read response body
    def make_request(self, requestType, endpoint, postUrl="", postBody=""):
        return self.make_request_raw(requestType, endpoint, postUrl, postBody).read().decode("utf-8")



if __name__ == "__main__":
    print()
    # getLatestPrice_Kraren('XBTUSD')