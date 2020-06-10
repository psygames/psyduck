from core import db
from action_process.update import update_procedure
from datetime import datetime

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
    u = db.user_get_by_state('on')
    if u is not None:
        fake_add_request(u['uid'], u['csdn'])


def fake_add_request(uid, csdn):
    # todo fake data save to db
    act = {'id': 'fake_update', 'uid': uid, 'message': csdn, 'state': 'process', 'time': datetime.now()}
    procedures.append(update_procedure.UpdateProcedure(act))


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
