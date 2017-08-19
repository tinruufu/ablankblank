from __future__ import unicode_literals

import tweepy

from blank import get_structure
from image import generate_image
from secrets import app_key, app_secret, token_key, token_secret


auth = tweepy.OAuthHandler(app_key, app_secret)
auth.set_access_token(token_key, token_secret)
api = tweepy.API(auth)


def tweet(interactive=False):
    structure = get_structure()
    status = 'you are {}'.format(' '.join((unicode(s) for s in structure)))
    if interactive:
        print status
        if not raw_input('do u wanna post?\n').startswith('y'):
            return

    image = generate_image([segment.context() for segment in structure])
    api.update_with_media(image, status=status)


if __name__ == '__main__':
    from sys import argv
    tweet(interactive='-i' in argv)
