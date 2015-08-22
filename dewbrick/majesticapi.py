import argparse
import json
import os

import requests
from itertools import cycle

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {'app_api_key': os.environ.get('MAJESTIC_API_KEY')}


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


def get(cmd, params):
    querydict = {'cmd': cmd}
    querydict.update(BASE_PARAMS)
    querydict.update(params)
    response = requests.get(BASE_URL, params=querydict)
    return json.loads(response.text)


def getIndexItemInfo(sitelist):

    cmd = 'GetIndexItemInfo'
    params = {'items': len(sitelist),
              'datasource': 'fresh'}
    items = {'item{0}'.format(i): site for i, site in enumerate(sitelist)}
    params.update(items)

    responsedata = get(cmd, params)
    if responsedata['Code'] == 'OK':
        for data in responsedata['DataTables']['Results']['Data']:
            yield {
                'speed': data['OutDomainsExternal'] + 1,
                'power': data['OutLinksExternal'] + 1,
                'agility': data['OutLinksInternal'] + 1,
                'strength': data['RefDomainsEDU'] + 1,
                'smell': data['CitationFlow'] + 1,
            }
    else:
        yield {}

def searchByKeyword(key, start=0, count=10):

    cmd = 'SearchByKeyword'
    params = {'query': key, 'scope': '1', 'from': start, 'count': count}
    responsedata = get(cmd, params)
    if responsedata['Code'] == 'OK':
        for data in responsedata['DataTables']['Results']['Data']:
            yield data['Item']

def run():
    parser = argparse.ArgumentParser(description="a test thing")
    parser.add_argument('urls', nargs='+')

    args = parser.parse_args()
    results = getIndexItemInfo(args.urls)
    for result in results:
        print(result)

if __name__ == '__main__':
    run()
    print(list(d for d in searchByKeyword('python', start=10, count=10)))
