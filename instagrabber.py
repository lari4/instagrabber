# -*- coding: utf-8 -*-
"""
    instagrabber
    ~~~~~~~~~~
    Grabbing post, user and location data from instagram.
    :copyright: (c) 2017 by Alexey Larionov.
"""

import requests


__version__ = "2017.0.1"


def get_user_data(username):
    """ Get user data from instagram.

    :param username: A instagram username (string).
    """
    r = requests.get("https://www.instagram.com/{}/?__a=1".format(username))

    if r.status_code == requests.codes.ok:
        user_data = r.json()
    else:
        user_data = None

    return user_data


def get_next_page_data(username, cursor):
    """ Get more user media data
    :param username: A instagram username (string)
    :param cursor: A next page cursos (string)
    """
    r = requests.get("https://www.instagram.com/{}/media/?max_id={}".format(username, cursor))
    if r.status_code == requests.codes.ok:
        return r.json()['items']


def get_user_media(username, count):
    """ Get user media data.
    :param username: A instagram username (string)
    :param count: Count of media return (int)

    :return list: a list of dict
    """
    r = requests.get("https://www.instagram.com/{}/media/".format(username))

    if r.status_code == requests.codes.ok:
        if len(r.json()['items']) > count:
            media_data = r.json()['items'][0:count]
        else:
            media_data = r.json()['items']
            if r.json()['more_available']:
                while len(media_data) < count:
                    media_data += get_next_page_data(username, media_data[-1]['id'])
                else:
                    media_data = media_data[:count]
    else:
        media_data = None

    return media_data


class User(object):
    """Instagram user class."""
    def __init__(self, username):
        """Create instagram user object.
        :param username: A instagram username (string).
        """
        self._username = username
        self.data = get_user_data(username)

    def get_full_name(self):
        """ Get user full name"""
        return self.data['user']['full_name']

    def get_biography(self):
        """ Get the user biography"""
        return self.data['user']['biography']

    def get_external_url(self):
        """ Get user external url"""
        return self.data['user']['external_url']

    def get_profile_pic(self):
        """ Get user profile picture """
        return self.data['user']['profile_pic_url']

    def get_profile_pic_hd(self):
        """ Get user profile hd picture """
        return self.data['user']['profile_pic_url_hd']

    def followed_by(self):
        """ Number of followed users"""
        return self.data['user']['followed_by']['count']

    def follows(self):
        """ Number of follows"""
        return self.data['user']['follows']['count']

    def is_private(self):
        """ Check for private """
        return self.data['user']['is_private']

    def is_verified(self):
        """ Check for verified """
        return self.data['user']['is_verified']

    def count_of_media(self):
        """ Return count of media """
        return self.data['user']['media']['count']

    def get_media(self, count=12):
        """ Return user media """
        return get_user_media(self._username, count)
