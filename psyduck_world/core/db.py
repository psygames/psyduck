import pymongo
import datetime

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


def user_set(username, state):
    if act.find({'username': username}) is None:
        act.insert_one({'username': username, 'state': state})
    else:
        act.update_one({'username': username}, {'$set': {'state': state}})


# act
def act_init():
    global act
    act = db['act']

    # test
    if act.find_one({'id': 0}) is None:
        act_create(0, 0, 'user', 'login', 'request', '')
    else:
        act_set(0, 'request')


def act_create(_id, uid, _type, action, state, file):
    act.insert_one({'id': 0, 'uid': uid, 'type': _type, 'action': action, 'state': state, 'file': file,
                    'message': '', 'time': datetime.datetime.now()})


def act_get(_type, action, state):
    return act.find_one({'type': _type, 'action': action, 'state': state})


def act_set(_id, state, message='', file=''):
    act.update_one({'id': _id},
                   {'$set': {'state': state, 'message': message, 'file': file, 'time': datetime.datetime.now()}})
