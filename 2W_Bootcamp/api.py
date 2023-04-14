import json
import requests
import datetime


def get_API(url, header = None):
    # t = datetime.datetime.now()
    # print(t)
    data = requests.get(url, headers= header)
    # print('Time: ', datetime.datetime.now() - t)
    return json.loads(data.text)

