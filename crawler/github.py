#!/usr/bin/env python3

from queue import Queue
import json
import requests
from bs4 import BeautifulSoup

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

    f = open(output, 'w')

    queue = Queue()
    queue.put(startUser)

    count = 0
    while count < 20 and not queue.empty():
        username = queue.get()

        user = do_user(username)
        if user['location'] is not None:
            print(json.dumps(user), file=f)
            print(json.dumps(user))
        count += 1

        followings = get_following(username)
        for following in followings:
            queue.put(following)

    f.close()

#
#    user = do_user(startUser)
#    if user['location'] is not None:
#        print(json.dumps(user), file=f)
#        print(json.dumps(user))
#
#    followings = get_following(startUser)
#
#    for item in followings:
#        user = do_user(item)
#        if user['location'] is not None:
#            print(json.dumps(user), file=f)
#            print(json.dumps(user))
