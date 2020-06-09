import requests
import json


def req(_action):
    _doc = requests.get(f"http://127.0.0.1:8000/psyduck/{_action}?uid=admin")
    _json = json.loads(_doc.content)
    return _json


doc = req('user_list')
print(f'结果: {doc}')
