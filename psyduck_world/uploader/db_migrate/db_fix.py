from core import db

db.init()
_ds = db.download.find({})
for _d in _ds:
    if type(_d['csdn']) is str:
        continue
    csdn = _d['csdn']['account']
    info = _d['csdn']
    info.pop('account')
    info.pop('tag')
    info['uploader'] = ''
    db.download.update_one({'id': _d['id']}, {'$set': {'csdn': csdn, 'info': info}})
