import jieba
import jieba.analyse
import pymongo
from datetime import datetime
from core import db_setting

db: pymongo.MongoClient = None
act: pymongo.collection.Collection = None
user: pymongo.collection.Collection = None
download: pymongo.collection.Collection = None

_is_inited = False


def init():
    global _is_inited
    if _is_inited:
        return
    global db
    client = pymongo.MongoClient(db_setting.host, db_setting.port)
    if db_setting.username is not None and db_setting.password is not None:
        client.admin.authenticate(db_setting.username, db_setting.password)
    db = client['psyduck']
    act_init()
    user_init()
    download_init()
    _is_inited = True


# user
def user_init():
    global user
    user = db['user']


def user_set_state(uid, csdn, state):
    if user.find_one({'uid': uid, 'csdn': csdn}) is None:
        user_create(uid, csdn, state, {}, datetime(1970, 1, 1, 0, 0, 0))
    else:
        user.update_one({'uid': uid, 'csdn': csdn}, {'$set': {'state': state}})


def user_set_info(uid, csdn, info):
    if user.find_one({'uid': uid, 'csdn': csdn}) is None:
        user_create(uid, csdn, 'off', info, datetime.now())
    else:
        user.update_one({'uid': uid, 'csdn': csdn}, {'$set': {'info': info, 'update_time': datetime.now()}})


def user_create(uid, csdn, state, info, update_time):
    user.insert_one({'uid': uid, 'csdn': csdn, 'state': state, 'info': info, 'update_time': update_time})


def user_get(uid, csdn):
    return user.find_one({'uid': uid, 'csdn': csdn})


# act
def act_init():
    global act
    act = db['act']


def act_reset():
    act.update_many({'$nor': [{'state': 'fail'}, {'state': 'done'}]}, {'$set': {'state': 'fail', 'result': 'reset'}})


def act_create(_id, uid, action, state, message='', result=''):
    act.insert_one({'id': _id, 'uid': uid, 'action': action, 'state': state,
                    'message': message, 'result': result, 'time': datetime.now()})


def act_get(action, state):
    return act.find_one({'action': action, 'state': state})


def act_set_state(_id, state, result):
    act.update_one({'id': _id},
                   {'$set': {'state': state, 'result': result, 'time': datetime.now()}})


# download
def download_init():
    global download
    download = db['download']


def download_create_qq(_id, uid, csdn, url, title, _type, size, description, filename, point, star, upload_time,
                       uploader, qq_group, qq_num, qq_name, share_url, create_time):
    download.insert_one({'id': _id, 'uid': uid, 'csdn': csdn,
                         'info': {'url': url, 'title': title, 'type': _type, 'size': size,
                                  'description': description, 'filename': filename, 'point': point, 'star': star,
                                  'uploader': uploader, 'upload_time': upload_time, },
                         'qq': {'qq_group': qq_group, 'qq_num': qq_num, 'qq_name': qq_name},
                         'share_url': share_url,
                         'create_time': create_time})


def download_create(_id, uid, csdn, url, title, _type, size, description, filename, point, star, upload_time,
                    uploader, share_url, create_time):
    download.insert_one({'id': _id, 'uid': uid, 'csdn': csdn,
                         'info': {'url': url, 'title': title, 'type': _type, 'size': size,
                                  'description': description, 'filename': filename, 'point': point, 'star': star,
                                  'uploader': uploader, 'upload_time': upload_time, },
                         'share_url': share_url,
                         'create_time': create_time})


def download_set_share_url(_id, share_url):
    data = download.find_one({'id': _id})
    if data is not None:
        download.update_one({'id': _id}, {'$set': {'share_url': share_url}})


def download_get(_id):
    data = download.find_one({'id': _id})
    return data


def build_result(*args, ):
    result = []
    for r in args:
        for ri in r:
            result.append(ri)
    return result


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
    r2 = db.download.find(_build_query(keywords, 'and', 'info.description')).skip(_skip).limit(limit - count)
    raw_count += r2.count()
    count += r2.count(with_limit_and_skip=True)
    _print_log(keywords, count, 2, __st)
    if count >= limit:
        return build_result(r1, r2)

    __st = time.time()
    _skip = max(skip - raw_count, 0)
    r3 = db.download.find(_build_query(keywords, 'or', 'info.title')).skip(_skip).limit(limit - count)
    raw_count += r3.count()
    count += r3.count(with_limit_and_skip=True)
    _print_log(keywords, count, 3, __st)
    return build_result(r1, r2, r3)


def download_search(keyword, index, length=10):
    keywords = jieba.analyse.extract_tags(keyword, 3)
    if len(keywords) == 0:
        keywords.append(keyword)
    result = _download_search(keywords, length, index)
    return result
