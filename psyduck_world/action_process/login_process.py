from core import db
import action_process.login_procedure

login_procedure = []


# login
def login_verify_get():
    act = db.act_get('user', 'login_verify_get', 'request')
    if act is None:
        return
    solved = False
    for p in login_procedure:
        if p.act['uid'] == act['uid']:
            p.get_verify_code(act['message'])
            db.act_set(act['id'], 'done', act['message'])
            solved = True
            break
    if not solved:
        db.act_set(act['id'], 'fail', 'procedure not exist.')


def login_verify_set():
    act = db.act_get('user', 'login_verify_set', 'request')
    if act is None:
        return
    solved = False
    for p in login_procedure:
        if p.act['uid'] == act['uid']:
            p.set_verify_code(act['message'])
            db.act_set(act['id'], 'done', act['message'])
            solved = True
            break
    if not solved:
        db.act_set(act['id'], 'fail', 'procedure not exist.')


def login_request():
    act = db.act_get('user', 'login', 'request')
    if act is None:
        return
    db.act_set(act['id'], 'process')
    login_procedure.append(action_process.login_procedure.LoginProcedure(act))


def login_procedure_update():
    for p in login_procedure:
        if p.over:
            login_procedure.remove(p)
            continue
        p.update()


def update():
    login_request()
    login_verify_get()
    login_verify_set()
    login_procedure_update()


def stop():
    for p in login_procedure:
        p.stop()
    login_procedure.clear()
