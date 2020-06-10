from core import db
import action_process.login.login_procedure

procedures = []


# login
def login_verify_get():
    act = db.act_get('user', 'login_verify_get', 'request')
    if act is None:
        return
    solved = False
    for p in procedures:
        if p.act['uid'] == act['uid']:
            p.get_verify_code(act['message'])
            db.act_set(act['id'], 'done', act['message'], act['result'])
            solved = True
            break
    if not solved:
        db.act_set(act['id'], 'fail', act['message'], 'procedure not exist.')


def login_verify_set():
    act = db.act_get('user', 'login_verify_set', 'request')
    if act is None:
        return
    solved = False
    for p in procedures:
        if p.act['uid'] == act['uid']:
            p.set_verify_code(act['message'])
            db.act_set(act['id'], 'done', act['message'], act['result'])
            solved = True
            break
    if not solved:
        db.act_set(act['id'], 'fail', act['message'], 'procedure not exist.')


def login_request():
    act = db.act_get('user', 'login', 'request')
    if act is None:
        return
    db.act_set(act['id'], 'process', act['message'], act['result'])
    procedures.append(action_process.login.login_procedure.LoginProcedure(act))


def login_procedure_update():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    login_request()
    login_verify_get()
    login_verify_set()
    login_procedure_update()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
