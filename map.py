#!/usr/bin/env python3

import requests

import creep

def get_geocoding(location):

    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(location))
    json = res.json()
    if len(json['results']) == 0:
        return None
    result = json['results'][0]
    return (result['formatted_address'], result['geometry']['location'])

def do_user(username):
    location = creep.get_location(username)
    if location is None:
        return
    geocoding = get_geocoding(location)
    if geocoding is None:
        return
    print(username, ':', geocoding[0], geocoding[1])

if __name__ == '__main__':

    username = 'nettee'
    do_user(username)
    followings = creep.get_following(username)
    for following in followings:
        do_user(following)
