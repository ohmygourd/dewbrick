import argparse
import json
import os

import requests
from itertools import cycle
from random import shuffle

from dewbrick.utils import generate_image, generate_name, generate_screenshot

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {'app_api_key': os.environ.get('MAJESTIC_API_KEY')}
DEFAULT_IMG = ('http://content.mycutegraphics.com/'
               'graphics/monster/cute-monster.png')


class GameDataSet(object):
    _data = []

    def __init__(self, prefetch=100):
        if not BASE_PARAMS['app_api_key']:
            raise AttributeError('You need to set MAJESTIC_API_KEY to use'
                                 ' the Majestic.com API')
        if not self._data:
            urls = list(find_urls('python', 0, prefetch))
            self.load_data(urls)
            shuffle(self._data)
        self.data = cycle(self._data)

    def load_data(self, urls):
        self._data = list(get_card_stats(urls))

    def get(self, num=1):
        return (next(self.data) for d in range(0, num))


def majestic_get(cmd, params):
    querydict = {'cmd': cmd}
    querydict.update(BASE_PARAMS)
    querydict.update(params)
    response = requests.get(BASE_URL, params=querydict)
    return json.loads(response.text)


def get_card_stats(urls):
    cmd = 'GetIndexItemInfo'
    params = {'items': len(urls),
              'datasource': 'fresh'}
    items = {'item{0}'.format(i): url for i, url in enumerate(urls)}
    params.update(items)

    responsedata = majestic_get(cmd, params)
    if responsedata['Code'] == 'OK':
        for data in responsedata['DataTables']['Results']['Data']:
            yield {
                'name': generate_name(data['Item']),
                'site': data['Item'],
                'image': generate_image(data['Item']),
                'screenshot': generate_screenshot(data['Item']),
                'description': '',
                'attributes': [
                    {'name': 'speed', 'value': data['OutDomainsExternal'] + 1},
                    {'name': 'power', 'value': data['OutLinksExternal'] + 1},
                    {'name': 'agility',
                     'value': data['OutLinksInternal'] + 1},
                    {'name': 'strength', 'value': data['RefDomainsEDU'] + 1},
                    {'name': 'smell', 'value': data['CitationFlow'] + 1},
                ]
            }
    else:
        yield {}


def find_urls(key, start=0, count=10):
    cmd = 'SearchByKeyword'
    params = {'query': key, 'scope': '1', 'from': start, 'count': count}
    responsedata = majestic_get(cmd, params)
    if responsedata['Code'] == 'OK':
        for data in responsedata['DataTables']['Results']['Data']:
            yield data['Item']


def run():
    parser = argparse.ArgumentParser(description="a test thing")
    parser.add_argument('urls', nargs='+')
    args = parser.parse_args()

    print('get_card_stats')
    print('='*10)
    results = get_card_stats(args.urls)
    for result in results:
        print(result)

    print('find_urls')
    print('='*10)
    print(list(d for d in find_urls('python', start=10, count=10)))
    print('GameDataSet')
    print('='*10)
    dataset = GameDataSet(20)
    print(list(dataset.get(5)))

if __name__ == '__main__':
    run()
