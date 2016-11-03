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
    return {
        'address': result['formatted_address'],
        'latitude': result['geometry']['location']['lat'],
        'longtitude': result['geometry']['location']['lng'],
    }

if __name__ == '__main__':

    users = model.user.get_all()
    for user in users:
        if model.geocode.exists(user.location):
            continue

        print(user)
        geocode = get_geocoding(user.location)
        model.geocode.add(user.location,
                geocode['address'],
                geocode['latitude'],
                geocode['longtitude'])

#    f = open('location.json', 'r')
#    of = open('geo.json', 'w')
#    for line in f:
#        line = line.strip('\n')
#        user = json.loads(line)
#
#        user2 = do_user(user)
#        print(json.dumps(user2))
#        print(json.dumps(user2), file=of)

