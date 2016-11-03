#!/usr/bin/env python3

from queue import Queue
import json
import requests
from bs4 import BeautifulSoup

import model

def get_information(user):
    res = requests.get('http://github.com/{}'.format(user))
    html = BeautifulSoup(res.text, 'lxml')

    location_list = html.select('li[aria-label="Home location"]')
    if len(location_list) > 0:
        location = location_list[0].contents[1]
    else:
        location = None

    fullname_list = html.select('span[class~="vcard-fullname"]')
    if len(fullname_list) > 0 and len(fullname_list[0].contents) > 0:
        fullname = fullname_list[0].contents[0]
    else:
        fullname = None

    return {
        'location': location,
        'fullname': fullname,
    }

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

        info = get_information(username)
        fullname = info['fullname']
        location = info['location']
        if location is None:
            continue

        print('username: {}, fullname: {}, location: {}'.format(username, fullname, location))
        model.add_user(username, fullname, location)

