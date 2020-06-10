from core import db
from action_process.update import update_procedure
from datetime import datetime
from datetime import timedelta
import uuid

_last_auto_update = datetime.now()
procedures = []


# 处理请求
def process_request():
    act = db.act_get('user', 'update', 'request')
    if act is None:
        return
    db.act_set(act['id'], 'process', act['message'], act['result'])
    procedures.append(update_procedure.UpdateProcedure(act))


# 自动更新
def auto_update():
    global _last_auto_update
    if (datetime.now() - _last_auto_update).seconds < 10:
        return
    u = db.user.find_one({'update_time': {'$lt': datetime.now() - timedelta(seconds=3600)}})
    if u is not None:
        db.user_set_info(u['uid'], u['csdn'], u['info'])
        fake_add_request(u['uid'], u['csdn'])


def fake_add_request(uid, csdn):
    _id = f'auto_update_{uuid.uuid4()}'
    db.act_create(_id, uid, 'user', 'update', 'request', csdn)


def procedure_update():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    process_request()
    auto_update()
    procedure_update()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
