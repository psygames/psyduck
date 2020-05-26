import core.db
import action_process.validate_procedure
import datetime

last_auto_validate_time = datetime.datetime.now()
procedures = []


def process_request():
    act = core.db.act_get('user', 'validate', 'request')
    if act is None:
        return
    core.db.act_set(act['id'], 'process', act['message'], act['result'])
    procedures.append(action_process.validate_procedure.ValidateProcedure(act))


def fake_add_request(uid, csdn):
    act = {'id': 'fake_validate', 'uid': uid, 'message': csdn, 'state': 'process', 'time': datetime.datetime.now()}
    procedures.append(action_process.validate_procedure.ValidateProcedure(act))


def auto_validate():
    global last_auto_validate_time
    if (datetime.datetime.now() - last_auto_validate_time).seconds < 20:
        return
    last_auto_validate_time = datetime.datetime.now()
    u = core.db.user_get_by_state('on')
    if u is not None:
        fake_add_request(u['uid'], u['csdn'])


def procedure_update():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    process_request()
    # auto_validate()
    procedure_update()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
