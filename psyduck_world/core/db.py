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

    # test
    # user_set('admin', 'y85171642', 'on')


def user_set_state(uid, csdn, state):
    if user.find_one({'uid': uid, 'csdn': csdn}) is None:
        user.insert_one({'uid': uid, 'csdn': csdn, 'state': state})
    else:
        user.update_one({'uid': uid, 'csdn': csdn}, {'$set': {'state': state}})


def user_get(uid, csdn):
    return user.find_one({'uid': uid, 'csdn': csdn})


def user_get_by_state(state):
    return user.find_one({'state': state})


# act
def act_init():
    global act
    act = db['act']


def act_reset():
    act.update_many({'type': 'user', '$nor': [{'state': 'fail'}, {'state': 'done'}]}
                    , {'$set': {'state': 'fail', 'message': 'reset'}})


def act_test():
    # test
    if act.find_one({'id': 0}) is None:
        act_create(0, 'admin', 'user', 'login', 'request')
    else:
        act_set(0, 'request', '', '')

    if act.find_one({'id': 1}) is None:
        act_create(1, 'admin', 'user', 'login_verify_get', 'done', '18600105483')
    else:
        act_set(1, 'done', '18600105483', '')

    if act.find_one({'id': 2}) is None:
        act_create(2, 'admin', 'user', 'login_verify_set', 'done', '000000')
    else:
        act_set(2, 'done', '000000', '')

    if act.find_one({'id': 4}) is None:
        act_create(4, 'admin', 'user', 'validate', 'request', 'y85171642')
    else:
        act_set(4, 'request', 'y85171642', '')


def act_create(_id, uid, _type, action, state, message='', result=''):
    act.insert_one({'id': _id, 'uid': uid, 'type': _type, 'action': action, 'state': state,
                    'message': message, 'result': result, 'time': datetime.datetime.now()})


def act_get(_type, action, state):
    return act.find_one({'type': _type, 'action': action, 'state': state})


def act_set(_id, state, message, result):
    act.update_one({'id': _id},
                   {'$set': {'state': state, 'message': message, 'result': result, 'time': datetime.datetime.now()}})
