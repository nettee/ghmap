#!/usr/bin/env python3

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

if __name__ == '__main__':

    username = 'nettee'
    f = open('location.json', 'w')

    user = do_user(username)
    print(json.dumps(user), file=f)

    followings = get_following(username)

    for following in followings:
        following_user = do_user(following)
        print(json.dumps(following_user), file=f)
