import os
import requests as r

BASE_URL = "http://127.0.0.1:5000"

def post(api, data):
    return r.post(f'{BASE_URL}{api}', json=data)

api = '/load_line'
data = ['湖南中医学院第一附属医院', '江苏省中医院']
print(post(api, data).text)
