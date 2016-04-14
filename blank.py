from __future__ import unicode_literals

from random import choice
from time import sleep

from inflect import engine
import requests

inflect = engine()

WORDS = []
CONNECTIVES = [
    'in',
    'the',
    'to',
    'of',
    'on',
    'and',
    'a',
    'an',
]


class Segment(object):
    def __init__(self, words):
        self.words = words

    def is_boxed(self):
        return not all((w in CONNECTIVES for w in self.words))

    def __unicode__(self):
        string = ' '.join(self.words)
        return '[{}]'.format(string) if self.is_boxed() else string


def populate_words():
    with open('/usr/share/dict/words') as wf:
        for word in wf.readlines():
            WORDS.append(word.strip())


def get_word():
    if not WORDS:
        populate_words()

    return choice(WORDS)


def get_example():
    tried = []

    for attempt in xrange(5):
        seed = get_word()
        tried.append(seed)
        _, examples = requests.get('https://api.bing.com/osjson.aspx',
                                   params={'query': inflect.a(seed)}).json()

        candidates = [e for e in examples if e.split()[0] in ('a', 'an')]
        if candidates:
            return choice(candidates)

        sleep(1)

    raise ValueError('Failed to find anything good; tried:\n{}'
                     .format('\n'.join(tried)))


def get_structure():
    words = get_example().split()
    islands = [[]]
    for word in words:
        if not islands[-1]:
            islands[-1].append(word)
        elif (word in CONNECTIVES) != (islands[-1][-1] in CONNECTIVES):
            islands.append([word])
        else:
            islands[-1].append(word)

    return [Segment(i) for i in islands]


if __name__ == '__main__':
    for i in xrange(10):
        print ' '.join((unicode(s) for s in get_structure()))
