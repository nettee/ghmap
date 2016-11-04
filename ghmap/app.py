#!/usr/bin/env python3

import json
from flask import Flask, render_template

from .. import crawler

app = Flask(__name__)

users = [
       {"address": "Nanjing, Jiangsu, China", "username": "nettee", "location": {"lat": 32.060255, "lng": 118.796877}},
       {"address": "Shenzhen, Guangdong, China", "username": "phodal", "location": {"lat": 22.543096, "lng": 114.057865}},
       {"address": "Hangzhou, Zhejiang, China", "username": "JacksonTian", "location": {"lat": 30.274085, "lng": 120.15507}},
       {"address": "Shanghai, China", "username": "Ovilia", "location": {"lat": 31.230416, "lng": 121.473701}},
       {"address": "Hefei, Anhui, China", "username": "be5invis", "location": {"lat": 31.820592, "lng": 117.227219}},
]

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/users', methods=['GET'])
def get_users():
    return json.dumps(users)

if __name__ == '__main__':
    app.run()
