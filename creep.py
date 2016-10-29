#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def get_location(user):
    res = requests.get('http://github.com/{}'.format(user))
    bs = BeautifulSoup(res.text, 'lxml')

    location_list = bs.select('li[aria-label="Home location"]')
    if len(location_list) > 0:
        location = location_list[0].contents[1]
    else:
        location = None

#    username_list = bs.select('span[class~="vcard-username"]')
#    if len(username_list) > 0:
#        username = username_list[0].contents[0]
#    else:
#        username = None

    return location

if __name__ == '__main__':

    username = 'nettee'
    location = get_location(username)

    print(username, ':', location)
