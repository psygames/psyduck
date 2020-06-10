from core import db
import uuid
import json


# inner
def _get_token(prefix=''):
    if prefix == '':
        return uuid.uuid4()
    return f'{prefix}_{uuid.uuid4()}'


# login
def _login_build(token, uid, status, message):
    dic = {'status': status, 'token': token, 'uid': uid, 'message': message}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def _login_build_state(status, state, result):
    dic = {'status': status, 'state': state, 'result': result}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def login_get_state(token, uid):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _login_build_state('error', 'fail', 'Token不存在。')
    return _login_build_state('ok', act['state'], act['result'])


def login_verify_get(token, uid, phone):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _login_build(token, uid, 'ok', '请使用正确Token。')
    if act['state'] == 'verify_get':
        combine_token = token + '_verify_get'
        act = db.act.find_one({'id': combine_token, 'uid': uid})
        if act is None:
            db.act_create(combine_token, uid, 'user', 'login_verify_get', 'request', phone)
            return _login_build(token, uid, 'ok', '获取手机验证码...')
        elif act['state'] == 'request' or act['state'] == 'process':
            return _login_build(token, uid, 'ok', '获取手机验证码...')
        elif act['state'] == 'done':
            return _login_build(token, uid, 'ok', '获取手机验证码完成')
    return _login_build(token, uid, 'error', 'unknown')


def login_verify_set(token, uid, code):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _login_build(token, uid, 'error', '请使用正确Token。')
    if act['state'] == 'verify_set':
        combine_token = token + '_verify_set'
        act = db.act.find_one({'id': combine_token, 'uid': uid})
        if act is None:
            db.act_create(combine_token, uid, 'user', 'login_verify_set', 'request', code)
            return _login_build(token, uid, 'ok', '设置手机验证码...')
        elif act['state'] == 'request' or act['state'] == 'process':
            return _login_build(token, uid, 'ok', '设置手机验证码...')
        elif act['state'] == 'done':
            return _login_build(token, uid, 'ok', '设置手机验证码完成')
    return _login_build(token, uid, 'error', 'unknown')


def login_get_qr_code(token, uid):
    if token is None or token == '':
        _condition = {'type': 'user', 'action': 'login', 'uid': uid,
                      '$or': [{'state': 'request'}, {'state': 'process'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前正在登陆中，请勿重复提交。{uid} -> {0}')
            return _login_build('', uid, 'error', '当前正在登陆中，请勿重复提交。')

        _condition = {'type': 'user', 'action': 'login', 'uid': uid,
                      '$or': [{'state': 'scan'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前正在扫码阶段，请执行正确操作。{uid} -> {0}')
            return _login_build('', uid, 'error', '当前正在扫码阶段，请执行正确操作。')

        _condition = {'type': 'user', 'action': 'login', 'uid': uid,
                      '$or': [{'state': 'verify_get'}, {'state': 'verify_set'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前正在手机验证阶段，请执行正确操作。{uid} -> {0}')
            return _login_build('', uid, 'error', '当前正在手机验证阶段，请执行正确操作。')

        token = _get_token('login')
        db.act_create(token, uid, 'user', 'login', 'request')
        return _login_build(token, uid, 'ok', '开始获取二维码...')
    act = db.act.find_one({'id': token})
    if act is None:
        return _login_build(token, uid, 'error', '请使用正确Token获取二维码。')
    if act['state'] == 'request' or act['state'] == 'process':
        return _login_build(token, uid, 'ok', '正在获取二维码...')
    if act['state'] == 'fail':
        return _login_build(token, uid, 'error', act['result'])
    if act['state'] == 'scan':
        return _login_build(token, uid, 'ok', act['result'])
    return _login_build(token, uid, 'error', 'unknown')


# validate
def _validate_build(status, token, uid, csdn, message):
    dic = {'status': status, 'token': token, 'uid': uid, 'csdn': csdn, 'message': message}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def _validate_build_state(status, state, result):
    dic = {'status': status, 'state': state, 'result': result}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def validate_get_state(token, uid, csdn):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _validate_build_state('error', 'fail', 'Token不存在')
    return _validate_build_state('ok', act['state'], act['result'])


def validate_csdn(token, uid, csdn):
    if token is None or token == '':
        if db.user_get(uid, csdn) is None:
            print(f'用户暂未登陆CSDN账号 {uid} -> {csdn}')
            return _validate_build('error', '', uid, csdn, '用户暂未登陆CSDN账号')

        _condition = {'type': 'user', 'action': 'validate', 'uid': uid, 'message': csdn,
                      '$or': [{'state': 'request'}, {'state': 'process'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前账户正在验证中，请勿重复提交。{uid} -> {csdn}')
            return _validate_build('error', '', uid, csdn, '当前账户正在验证中，请勿重复提交。')

        token = _get_token('validate')
        db.act_create(token, uid, 'user', 'validate', 'request', csdn)
        return _validate_build('ok', token, uid, csdn, '开始验证...')
    else:
        act = db.act.find_one({'id': token})
        if act is None:
            return _validate_build('error', token, uid, csdn, '请使用正确Token验证账号。')
        if act['state'] == 'request' or act['state'] == 'process':
            return _validate_build('ok', token, uid, csdn, '正在验证中...')
        if act['state'] == 'fail':
            return _validate_build('error', token, uid, csdn, act['result'])
        if act['state'] == 'done':
            return _validate_build('ok', token, uid, csdn, act['result'])
        return _validate_build('error', token, uid, csdn, 'unknown')


# list
def _common_build(status, message):
    dic = {'status': status, 'message': message}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def user_list(uid):
    docs = db.user.find({'uid': uid})
    items = []
    for doc in docs:
        items.append({'csdn': doc['csdn'], 'state': doc['state']})
    return _common_build('ok', items)
