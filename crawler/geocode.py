#!/usr/bin/env python3

import json
import requests

import model

def get_geocoding(location):

    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(location))
    json = res.json()
    if len(json['results']) == 0:
        return None
    result = json['results'][0]
    return (result['formatted_address'], result['geometry']['location'])

def do_user(user0):
    username = user0['username']
    location = user0['location']
    geocoding = get_geocoding(location)
    user = {
            'username' : username,
            'address' : geocoding[0],
            'location' : geocoding[1],
    }
    return user

if __name__ == '__main__':

    users = model.user.get_all()
    for user in users:
        print(user)

#    f = open('location.json', 'r')
#    of = open('geo.json', 'w')
#    for line in f:
#        line = line.strip('\n')
#        user = json.loads(line)
#
#        user2 = do_user(user)
#        print(json.dumps(user2))
#        print(json.dumps(user2), file=of)

