from core import db
import uuid
import json
from datetime import date, datetime
import jieba.analyse


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


def _error_xxx_empty(xxx):
    return _error_build(f'{xxx} is empty.')


def _error_uid_empty():
    return _error_xxx_empty('uid')


def _error_csdn_empty():
    return _error_xxx_empty('csdn')


def _error_token_empty():
    return _error_xxx_empty('token')


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


def _success_build(result):
    return _common_build('ok', result=result)


# login
def login_get_state(token, uid):
    if token == '':
        return _error_token_empty()
    if uid == '':
        return _error_uid_empty()

    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    return _state_build(act)


def login(token, uid):
    if token == '':
        if uid == '':
            return _error_uid_empty()

        _condition = {'action': 'login', 'uid': uid,
                      '$nor': [{'state': 'fail'}, {'state': 'done'}]}
        if db.act.find_one(_condition) is not None:
            print(f'重复的登陆请求 {uid}')
            return _error_repeated_request()

        token = _gen_token('login')
        db.act_create(token, uid, 'login', 'request')
        return _token_build(token)
    else:
        return login_get_state(token, uid)


def login_verify_get(token, uid, phone):
    if token == '':
        return _error_token_empty()
    if uid == '':
        return _error_uid_empty()
    if phone == '':
        return _error_xxx_empty('phone')

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
    if token == '':
        return _error_token_empty()
    if uid == '':
        return _error_uid_empty()
    if code == '':
        return _error_xxx_empty('code')

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
    if token == '':
        return _error_token_empty()
    if uid == '':
        return _error_uid_empty()
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    if act['state'] == 'done':
        _d = db.download_get(act['result'])
        if _d is None:
            act['result'] = 'download not found.'
        else:
            act['result'] = _download_cut(_d)
    return _state_build(act)


def download(token, uid, csdn, url):
    if token == '':
        if uid == '':
            return _error_uid_empty()
        if csdn == '':
            return _error_csdn_empty()
        if url == '':
            return _error_xxx_empty('url')

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
    if token == '':
        return _error_token_empty()
    if uid == '':
        return _error_uid_empty()
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return _error_token_not_exist()
    return _state_build(act)


def update(token, uid, csdn):
    if token == '':
        if uid == '':
            return _error_uid_empty()
        if csdn == '':
            return _error_csdn_empty()

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
        return _error_uid_empty()
    docs = db.user.find({'uid': uid})
    items = []
    for doc in docs:
        doc.pop('_id')
        items.append(doc)
    return _success_build(items)


# get download
def _download_cut(_d):
    def try_pop(key):
        if key in _d:
            _d.pop(key)

    try_pop('_id')
    try_pop('qq')
    try_pop('uid')
    try_pop('csdn')

    if len(_d['info']['description']) > 200:
        _d['info']['description'] = _d['info']['description'][0:200] + '...'

    return _d


def download_get(_id):
    if _id == '':
        return _error_xxx_empty('id')
    _d = db.download_get(_id)
    if _d is None:
        return _error_build('download not found.')
    _download_cut(_d)
    return _success_build(_d)


def _build_query(keywords, op, tag):
    query = {f'${op}': []}
    for k in keywords:
        k = k.strip('/i')
        k = k.strip('/')
        query[f'${op}'].append({f'{tag}': {'$regex': f'{k}', '$options': '$i'}})
    return query


def _print_log(keywords, count, step, st):
    import time
    print(f'search keys: {keywords}, count: {count}, cost: {time.time() - st:.2f}s, step: {step}')


def build_result(*args, ):
    result = []
    for r in args:
        for ri in r:
            _d = _download_cut(ri)
            result.append(_d)
    return result


def _download_search(keywords, limit, skip):
    import time
    __st = time.time()
    r1 = db.download.find(_build_query(keywords, 'and', 'info.title')).skip(skip).limit(limit)
    raw_count = r1.count()
    count = r1.count(with_limit_and_skip=True)
    _print_log(keywords, count, 1, __st)
    if count >= limit:
        return build_result(r1)

    __st = time.time()
    _skip = max(skip - raw_count, 0)
    r2 = db.download.find(_build_query(keywords, 'and', 'brief')).skip(_skip).limit(limit - count)
    raw_count += r2.count()
    count += r2.count(with_limit_and_skip=True)
    _print_log(keywords, count, 2, __st)
    if count >= limit:
        return build_result(r1, r2)

    __st = time.time()
    _skip = max(skip - raw_count, 0)
    r3 = db.download.find(_build_query(keywords, 'or', 'title')).skip(_skip).limit(limit - count)
    raw_count += r3.count()
    count += r3.count(with_limit_and_skip=True)
    _print_log(keywords, count, 3, __st)
    return build_result(r1, r2, r3)


def download_find(keyword, index):
    if keyword == '':
        return _error_xxx_empty('keyword')

    keywords = jieba.analyse.extract_tags(keyword, 3)
    if len(keywords) == 0:
        keywords.append(keyword)
    result = _download_search(keywords, 10, index)
    return _success_build(result)


def download_list(uid, csdn, index):
    if uid == '':
        return _error_uid_empty()

    _res = []
    if csdn == '':
        _res = db.download.find({'uid': uid}).skip(index).limit(10)
    else:
        _res = db.download.find({'uid': uid, 'csdn': csdn}).skip(index).limit(10)

    _build_res = []
    for r in _res:
        r = _download_cut(r)
        _build_res.append(r)
    return _success_build(_build_res)
