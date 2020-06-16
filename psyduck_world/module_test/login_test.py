import time
from module_test import req


def get_state(_token):
    _doc = req.req_simple('login_get_state', _token)
    return _doc['state']


# 初始 token
token = ''

# 创建请求
print(f'创建登陆请求 token: {token}')
doc = req.req_simple('login', token)
token = doc['token']

if doc['status'] == 'error':
    print(f'Error: {doc["message"]}')
    exit(0)

time.sleep(1)

# 等待二维码获取
print(f'等待二维码请求 token: {token}')
state = get_state(token)
while state != 'scan':
    time.sleep(1)
    state = get_state(token)

# 取得二维码
print(f'取得二维码 token: {token}')
doc = req.req_simple('login_get_qrcode', token)
print(doc['message'])

# 等待用户扫码
print(f'等待用户扫码 token: {token}')
state = get_state(token)
while state == 'scan':
    time.sleep(1)
    state = get_state(token)

# 扫码完成下一步
print(f'扫码完成下一步 token: {token}')
if state == 'done':
    print('登陆完成')
    exit(0)

if state != 'verify_get':
    print('错误状态')
    exit(0)

# 输入手机号
print(f'输入手机号 token: {token}')
phone = input('请输入手机号：')
print(f'手机号：{phone}')

# 获取手机验证码
print(f'获取手机验证码 token: {token}')
req.req_simple('login_verify_get', token, {'phone': phone})
time.sleep(1)

# 等待验证码获取
print(f'等待验证码获取 token: {token}')
state = get_state(token)
while state == 'verify_get':
    time.sleep(1)
    state = get_state(token)

if state != 'verify_set':
    print('错误状态')
    exit(0)

# 输入验证码
print(f'输入验证码 token: {token}')
code = input('请输入验证码：')
print(f'验证码：{code}')

# 设置验证码
print(f'设置验证码 token: {token}')
req.req_simple('login_verify_set', token, {'code': code})

# 等待完成登陆
print(f'等待完成登陆 token: {token}')
state = get_state(token)
while state != 'done':
    time.sleep(1)
    state = get_state(token)

print('登陆完成')
