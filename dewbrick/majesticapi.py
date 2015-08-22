import os
import requests
import json
from itertools import cycle

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {'app_api_key': os.environ.get('THEAPIKEY')}


def get(cmd, params):
    querydict = {'cmd': cmd}
    querydict.update(BASE_PARAMS)
    querydict.update(params)
    response = requests.get(BASE_URL, params=querydict)
    return json.loads(response.text)


class GameDataSet(object):
    _data = []

    def __init__(self):
        if not self._data:
            self._data = self.load_data(10)
        self.data = cycle(self._data)

    @classmethod
    def load_data(cls, num=1):
        data = []
        for _ in range(0, num):
            data.append({})
        return data

    def get(self, num=1):
        data = []
        for _ in range(0, num):
            item = self.data.pop()
            data.append(item)
            # async
            self.queue(item)
        return data

    def queue(self, item):
        # do request
        self._data.append(self.load_data(1))
        self._data.remove(item)

if __name__ == '__main__':
    response = get(cmd='GetBackLinkData',
                   params={'item': 'http://boingboing.net',
                           'Count': '5',
                           'datasource': 'fresh'})
    print(response)
