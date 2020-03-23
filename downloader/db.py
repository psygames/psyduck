import pymongo

db: pymongo.MongoClient = None
raw: pymongo.collection.Collection = None
user: pymongo.collection.Collection = None
zero: pymongo.collection.Collection = None


def __init_db():
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    global db
    global zero
    db = client['csdn']
    zero = db['zero']
    return db


def __get_db():
    global db
    if db is None:
        __init_db()
    return db


# zero
def zero_exist(_id):
    __get_db()
    return zero.find_one({'id': _id}) is not None


def zero_is_download(_id):
    __get_db()
    return zero.find_one({'id': _id})['state'] == 1


def zero_get_one():
    __get_db()
    return zero.find_one({'state': 0})


# state
# 0 - none
# 1 - downloading
# 2 - download failed
# 3 - downloaded
# 4 - uploading
# 5 - upload failed
# 6 - uploaded
def zero_set_state(_id, state):
    __get_db()
    zero.update_one({'id': _id}, {'$set': {'state': state}})


def zero_set_info(_id, info):
    __get_db()
    zero.update_one({'id': _id}, {'$set': {'info': info}})
