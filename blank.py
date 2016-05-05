from __future__ import unicode_literals

from random import choice
from time import sleep

from inflect import engine
import requests

inflect = engine()

WORDS = []
CONNECTIVES = set([
    'in',
    'the',
    'to',
    'of',
    'for',
    'on',
    'and',
    'a',
    'an',
    'with',
    'from',
    'is',
])


class Segment(object):
    def __init__(self, words):
        self.words = words

    def context(self):
        return {
            'text': self.string,
            'box': self.is_boxed,
        }

    def __unicode__(self):
        return '[{}]'.format(self.string) if self.is_boxed else self.string

    @property
    def is_boxed(self):
        return not all((w in CONNECTIVES for w in self.words))

    @property
    def string(self):
        return ' '.join(self.words)


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

    for attempt in xrange(15):
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

    segments = [Segment(i) for i in islands]

    if len(segments) == 2 and len(segments[1].words) == 2:
        segments = [
            Segment([w])
            for s in segments
            for w in s.words
        ]

    return segments


if __name__ == '__main__':
    for i in xrange(10):
        print ' '.join((unicode(s) for s in get_structure()))
