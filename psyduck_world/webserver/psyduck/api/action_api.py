from core import db
import uuid
import json
from datetime import date, datetime


# inner
def _gen_token(prefix=''):
    if prefix == '':
        return uuid.uuid4()
    return f'{prefix}_{uuid.uuid4()}'


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(dic):
    return json.dumps(dic, ensure_ascii=False, indent=4, cls=MyJSONEncoder)


def _common_build(status, uid=None, token=None, state=None, result=None, message=None):
    dic = {'status': status}
    if uid is not None:
        dic['uid'] = uid
    if token is not None:
        dic['token'] = token
    if state is not None:
        dic['state'] = state
    if result is not None:
        dic['result'] = result
    if message is not None:
        dic['message'] = message
    return json_dumps(dic)


def _error_build(error):
    return _common_build('error', message=error)


def _error_token_empty():
    return _error_build('token is empty.')


def _error_token_not_exist():
    return _error_build('token not exist.')


def _error_csdn_not_login():
    return _error_build('csdn not login.')


def _error_repeated_request():
    return _error_build('repeated request.')


def _token_build(token):
    return _common_build('ok', token=token)


def _state_build(act):
    if act is None:
        return _error_token_not_exist()
    return _common_build('ok', state=act['state'], result=act['result'])


# login
def login(token, uid):
    if token is None or token == '':
        _condition = {'action': 'login', 'uid': uid,
                      '$nor': [{'state': 'fail'}, {'state': 'done'}]}
        if db.act.find_one(_condition) is not None:
            return _error_repeated_request()

        token = _gen_token('login')
        db.act_create(token, uid, 'login', 'request')
        return _token_build(token)
    else:
        return login_get_state(token, uid)


def login_get_state(token, uid):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    return _state_build(act)


def login_verify_get(token, uid, phone):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    if act['state'] == 'verify_get':
        combine_token = token + '_verify_get'
        act = db.act.find_one({'id': combine_token, 'uid': uid})
        if act is None:
            db.act_create(combine_token, uid, 'login_verify_get', 'request', phone)
            return _token_build(token)
    return login_get_state(token, uid)


def login_verify_set(token, uid, code):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    if act['state'] == 'verify_set':
        combine_token = token + '_verify_set'
        act = db.act.find_one({'id': combine_token, 'uid': uid})
        if act is None:
            db.act_create(combine_token, uid, 'login_verify_set', 'request', code)
            return _token_build(token)
    return login_get_state(token, uid)


# download
def download_get_state(token, uid):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    return _state_build(act)


def download(token, uid, csdn, url):
    if token is None or token == '':
        if db.user_get(uid, csdn) is None:
            print(f'用户暂未登陆CSDN账号 {uid} -> {csdn}')
            return _error_csdn_not_login()

        _condition = {'action': 'download', 'uid': uid, 'message.url': url,
                      '$nor': [{'state': 'fail'}, {'state': 'done'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前资源正在下载中，请勿重复提交。{uid} -> {csdn} {url}')
            return _error_repeated_request()

        token = _gen_token('download')
        db.act_create(token, uid, 'download', 'request', {'csdn': csdn, 'url': url})
        return _token_build(token)
    else:
        return download_get_state(token, uid)


# update
def update_get_state(token, uid):
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    return _state_build(act)


def update(token, uid, csdn):
    if token is None or token == '':
        if db.user_get(uid, csdn) is None:
            print(f'用户暂未登陆CSDN账号 {uid} -> {csdn}')
            return _error_csdn_not_login()

        _condition = {'action': 'update', 'uid': uid, 'message': csdn,
                      '$nor': [{'state': 'fail'}, {'state': 'done'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前账户正在更新信息中，请勿重复提交。{uid} -> {csdn}')
            return _error_repeated_request()

        token = _gen_token('update')
        db.act_create(token, uid, 'update', 'request', csdn)
        return _token_build(token)
    else:
        return update_get_state(token, uid)


# list
def user_list(uid):
    if uid == '':
        return _common_build('error', 'uid is empty.')
    docs = db.user.find({'uid': uid})
    items = []
    for doc in docs:
        doc.pop('_id')
        items.append(doc)
    return _common_build('ok', items)
