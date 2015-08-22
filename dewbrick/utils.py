import tldextract
import pyphen
from random import choice

TITLES = ('Mister', 'Little Miss')
SUFFIXES = ('Destroyer of Worlds', 'the Monkey Botherer', 'PhD')


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
    name = '{} {}'.format(title, dic.inserted(name))

    if choice((True, False)):
        name = '{} {}'.format(name, choice(SUFFIXES))

    return name
