import time
from module_test import req


def get_state(_token):
    _doc = req.req_simple('validate_get_state', _token)
    return _doc['state']


# 初始 token
token = ''

# 请输入要验证的CSDN账号
csdn = input('请输入要更新的CSDN账号：')
print(f'CSDN账号：{csdn}')

# 创建验证请求
print(f'创建验证请求 token: {token}')
doc = req.req_simple('update', token, {'csdn': csdn})
token = doc['token']
time.sleep(1)

# 等待验证完成
print(f'等待更新完成 token: {token}')
state = get_state(token)
while state != 'done' and state != 'fail':
    time.sleep(1)
    state = get_state(token)

if state != 'done':
    doc = req.req_simple('update_get_state', token)
    print(f'验证失败，结果: {doc["result"]}')
    exit(0)

doc = req.req_simple('update_get_state', token)
print(f'验证完成，结果: {doc["result"]}')
