import argparse
import json
import os

from itertools import cycle

from tornado import gen, httpclient, ioloop
from tornado.httputil import url_concat

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {'app_api_key': os.environ.get('MAJESTIC_API_KEY')}
CLIENT = httpclient.AsyncHTTPClient()


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


@gen.coroutine
def majestic_get(cmd, params):
    query = {'cmd': cmd}
    query.update(BASE_PARAMS)
    query.update(params)
    request = httpclient.HTTPRequest(url_concat(BASE_URL, query),
                                     method="GET")
    response = yield CLIENT.fetch(request)
    raise gen.Return(json.loads(response.body.decode('utf-8')))


@gen.coroutine
def get_card_stats(cards):
    cmd = 'GetIndexItemInfo'
    params = {'items': len(cards),
              'datasource': 'fresh'}
    items = {'item{0}'.format(i): card for i, card in enumerate(cards)}
    params.update(items)

    responsedata = yield majestic_get(cmd, params)
    if responsedata['Code'] == 'OK':
        results = []
        for data in responsedata['DataTables']['Results']['Data']:
            results.append({
                'speed': data['OutDomainsExternal'] + 1,
                'power': data['OutLinksExternal'] + 1,
                'agility': data['OutLinksInternal'] + 1,
                'strength': data['RefDomainsEDU'] + 1,
                'smell': data['CitationFlow'] + 1,
            })
        raise gen.Return(results)
    else:
        raise gen.Return({})


@gen.coroutine
def find_cards(key, start=0, count=10):
    cmd = 'SearchByKeyword'
    params = {'query': key, 'scope': '1', 'from': start, 'count': count}
    responsedata = yield majestic_get(cmd, params)
    results = []
    if responsedata['Code'] == 'OK':
        for data in responsedata['DataTables']['Results']['Data']:
            results.append(data['Item'])
    raise gen.Return(results)


@gen.coroutine
def run():
    parser = argparse.ArgumentParser(description="a test thing")
    parser.add_argument('urls', nargs='+')

    args = parser.parse_args()
    results = yield get_card_stats(args.urls)
    for result in results:
        print(result)

    cards = yield find_cards('python', start=10, count=10)
    print(list(d for d in cards))

if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(run)
