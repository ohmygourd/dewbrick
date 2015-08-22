import argparse
import json
import os

import requests

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {'app_api_key': os.environ.get('THEAPIKEY')}


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


def run():
    parser = argparse.ArgumentParser(description="a test thing")
    parser.add_argument('urls', nargs='+')

    args = parser.parse_args()
    results = getIndexItemInfo(args.urls)
    for result in results:
        print(result)

if __name__ == '__main__':
    run()
