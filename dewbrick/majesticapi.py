import requests
import json

BASE_URL = "https://api.majestic.com/api/json"
BASE_PARAMS = {"app_api_key": "F090534BA7196CD922CF312FECCECBF5"}


def get(cmd, params):
    querydict = {'cmd': cmd}
    querydict.update(BASE_PARAMS)
    querydict.update(params)
    response = requests.get(BASE_URL, params=querydict)
    return json.loads(response.text)

if __name__ == '__main__':
    response = get(cmd='GetBackLinkData',
                   params={'item': 'http://boingboing.net',
                           'Count': '5',
                           'datasource': 'fresh'})
    print(response)
