import core.db
import action_process.validate_procedure
import datetime

last_auto_validate_time = datetime.datetime.now()
procedures = []


def validate_request():
    pass


def fake_add_request(uid, csdn):
    act = {'id': 'fake_validate', 'uid': uid, 'message': csdn, 'state': 'request', 'time': datetime.datetime.now()}
    procedures.append(action_process.validate_procedure.ValidateProcedure(act))


def validate_auto():
    global last_auto_validate_time
    if (datetime.datetime.now() - last_auto_validate_time).seconds < 10:
        return
    last_auto_validate_time = datetime.datetime.now()
    u = core.db.user_get_by_state('on')
    if u is not None:
        fake_add_request(u['uid'], u['csdn'])


def validate_process():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    validate_request()
    validate_auto()
    validate_process()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
