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
    client = pymongo.MongoClient(
        f"mongodb://{db_setting.username}:{db_setting.password}@{db_setting.host}:{db_setting.port}/database?authMechanism={db_setting.auth_mechanism}")
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
    act.update_many({'$nor': [{'state': 'fail'}, {'state': 'done'}]}
                    , {'$set': {'state': 'fail', 'result': 'reset'}})


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
