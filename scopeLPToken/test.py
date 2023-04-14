import urllib.request as urllib2
import ssl

headers = {'Content-Type':  'application/json',"User-Agent": "cf-api-python/1.0"}
request = urllib2.Request("https://api.arbiscan.io/api?module=contract&action=getabi&address=0x87425D8812f44726091831a9A109f4bDc3eA34b4&apikey=XU3YPHFPWX55F2A8B7UJ8IKVPC3GG2DR3X",headers=headers)
request.get_method = lambda:"GET"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib2.urlopen(
request, context=ctx, timeout=10)
print(response.read().decode("utf-8"))