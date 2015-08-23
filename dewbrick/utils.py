import hashlib
import json
import tldextract
import pyphen
from random import choice
import requests
from urllib.parse import quote


GOOGLE_URL = 'https://www.googleapis.com/pagespeedonline/v1/runPagespeed'
ROBOHASH_URL = 'http://robohash.org/'
TITLES = ('Mister', 'Little Miss', 'Señor', 'Queen')
SUFFIXES = ('Destroyer of Worlds', 'the Monkey Botherer', 'PhD',
            'Ah-gowan-gowan-gowan')


def generate_name(domain):
    title = choice(TITLES)

    _parts = tldextract.extract(domain)
    _parts = [_parts.subdomain, _parts.domain]
    parts = []
    for i, part in enumerate(_parts):
        if part and part != 'www':
            parts.append('{}{}'.format(part[0].upper(), part[1:]))
    name = '-'.join(parts)
    dic = pyphen.Pyphen(lang='en_US')
    hyphenated = tuple(dic.iterate(name))
    if hyphenated:
        name = '-'.join(hyphenated[0])
    name = '{} {}'.format(title, name)

    if choice((True, False)):
        name = '{} {}'.format(name, choice(SUFFIXES))

    return name


def generate_image(name):
    name_hash = hashlib.md5()
    name_hash.update(name.encode('utf-8'))
    url = '{}/{}?set=set2&amp;size=400x400'.format(
        ROBOHASH_URL,
        name_hash.hexdigest())
    return url


def generate_screenshot(name):
    if 'http' not in name:
        name = 'http://{}'.format(name)

    url = ('{}?url={}&screenshot=true').format(GOOGLE_URL, quote(name, ''))
    response = requests.get(url)
    data = json.loads(response.text)
    if 'screenshot' in data:
        img_data = data['screenshot']['data']
        img_data = img_data.replace('_', '/').replace('-', '+')
        return 'data:image/gif;base64,{}'.format(img_data)
