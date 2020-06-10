import pymongo
from datetime import datetime

db: pymongo.MongoClient = None
act: pymongo.collection.Collection = None
user: pymongo.collection.Collection = None


def init():
    global db
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client['psyduck']
    act_init()
    user_init()


# user
def user_init():
    global user
    user = db['csdn_user']


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
    act.update_many({'type': 'user', '$nor': [{'state': 'fail'}, {'state': 'done'}]}
                    , {'$set': {'state': 'fail', 'message': 'reset'}})


def act_create(_id, uid, _type, action, state, message='', result=''):
    act.insert_one({'id': _id, 'uid': uid, 'type': _type, 'action': action, 'state': state,
                    'message': message, 'result': result, 'time': datetime.now()})


def act_get(_type, action, state):
    return act.find_one({'type': _type, 'action': action, 'state': state})


def act_set(_id, state, message, result):
    act.update_one({'id': _id},
                   {'$set': {'state': state, 'message': message, 'result': result, 'time': datetime.now()}})
