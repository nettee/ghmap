#!/usr/bin/env python3

from queue import Queue
import json
import requests
from bs4 import BeautifulSoup

import model

def get_location(user):
    res = requests.get('http://github.com/{}'.format(user))
    html = BeautifulSoup(res.text, 'lxml')

    location_list = html.select('li[aria-label="Home location"]')
    if len(location_list) > 0:
        location = location_list[0].contents[1]
    else:
        location = None

#    username_list = html.select('span[class~="vcard-username"]')
#    if len(username_list) > 0:
#        username = username_list[0].contents[0]
#    else:
#        username = None

    return location

def get_following(user):
    res = requests.get('https://github.com/{}?tab=following'.format(user))
    html = BeautifulSoup(res.text, 'lxml')

    following_usernames = [
            following.select('div[class~="d-table-cell"]')[1]\
                .select('a')[0]\
                .select('span')[1]\
                .contents[0]
            for following in 
            html.select('div[class~="js-repo-filter"] > div[class~="d-table"]')
    ]
    return following_usernames

def do_user(username):
    location = get_location(username)

    user = {
            'username' : username,
            'location' : location,
    }

    return user

def crawl(output, startUser='nettee'):

    queue = Queue()
    queue.put(startUser)

    count = 0
    while count < 100 and not queue.empty():
        username = queue.get()
        print('[{}] {}'.format(count, username))
        followings = get_following(username)
        for following in followings:
            queue.put(following)

        count += 1

        if model.exists_user(username):
            continue

        location = get_location(username)
        if location is None:
            continue

        print('username: {}, location: {}'.format(username, location))
        model.add_user(username, location)

