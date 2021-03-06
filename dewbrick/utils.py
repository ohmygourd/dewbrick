import os
import hashlib
import json
import tldextract
import pyphen
from random import choice, randrange
import requests
from urllib.parse import quote

IMAGE_CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'cache/images.json')


def get_image_cache():
    if os.path.exists(IMAGE_CACHE_PATH):
        with open(IMAGE_CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_image_cache():
    with open(IMAGE_CACHE_PATH, 'w+') as f:
        f.write(json.dumps(IMAGE_CACHE))


DEFAULT_SHOT = ('https://upload.wikimedia.org/wikipedia/commons/7/75/'
                'Children-404_logo.png')
GOOGLE_URL = 'https://www.googleapis.com/pagespeedonline/v1/runPagespeed'
ROBOHASH_URL = 'http://robohash.org/'
TITLES = ('Mister', 'Little Miss', 'Señor', 'Queen')
SUFFIXES = ('Destroyer of Worlds', 'the Monkey Botherer', 'the Librarian',
            'Ah-gowan-gowan-gowan', 'in the lounge with a wrench',
            'aaaaaaargh', '(help me I\'m trapped in a museum)')
IMAGE_CACHE = get_image_cache()

LOREMS = (
    'One morning, when Gregor Samsa woke from troubled dreams,'
    ' he found himself transformed in his bed into a horrible vermin.',
    'A wonderful serenity has taken possession of my entire soul, like these'
    ' sweet mornings of spring',
    'The quick, brown fox jumps over a lazy dog. DJs flock by when MTV ax '
    'quiz prog. Junk MTV quiz graced by fox whelps.',
    'Far far away, behind the word mountains, far from the countries Vokalia'
    ' and Consonantia, there live the blind texts.',
    'This handy tool helps you create dummy text for all your layout needs.',
)
JOINERS = (
    'and',
    'is',
    'of',
    'the',
    'this',
    'them',
    'their',
    'there',
    'then',
    'we',
    'that',
    'or',
    'with',
    'when',
    'which',
    'was',
    'will',
    'handy',
    'helps',
    'you',
    'live',
    'graced',
    'by',
    'like',
    'sweet',
    'quick',
    'jumped',
    'has',
)


def generate_description(topics):
    lorem = choice(LOREMS).split()
    for topic in topics:
        while True:
            which_word = randrange(0, len(lorem))
            test_word = (lorem[which_word].replace('.',
                         '').replace(',', '').lower())
            if test_word not in JOINERS:
                break
        lorem[which_word] = topic.lower()
    return ' '.join(lorem)


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

    if choice((True, False, None)):
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
    if name not in IMAGE_CACHE:
        url = ('{}?url={}&screenshot=true').format(GOOGLE_URL, quote(name, ''))
        response = requests.get(url)
        data = json.loads(response.text)
        if 'screenshot' in data:
            img_data = data['screenshot']['data']
            img_data = img_data.replace('_', '/').replace('-', '+')
            img_data = 'data:image/gif;base64,{}'.format(img_data)

            IMAGE_CACHE[name] = img_data
        else:
            IMAGE_CACHE[name] = DEFAULT_SHOT
        save_image_cache()
    return IMAGE_CACHE[name]
