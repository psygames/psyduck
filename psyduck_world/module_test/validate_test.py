import requests
import json
import time


def req(_action, _token):
    _doc = requests.get(f"http://127.0.0.1:8000/psyduck?action={_action}&uid=admin&token={_token}&message=y85171642")
    _json = json.loads(_doc.content)
    return _json


def get_state(_token):
    _doc = req('validate_get_state', _token)
    return _doc['state']


# 初始 token
token = ''

# 创建验证请求
print(f'创建验证请求 token: {token}')
doc = req('validate', token)
token = doc['token']
time.sleep(1)

# 等待验证完成
print(f'等待验证完成 token: {token}')
state = get_state(token)
while state != 'done' and state != 'fail':
    time.sleep(1)
    state = get_state(token)

if state != 'done':
    doc = req('validate_get_state', token)
    print(f'验证失败，结果: {doc["result"]}')
    exit(0)

doc = req('validate_get_state', token)
print(f'验证完成，结果: {doc["result"]}')
