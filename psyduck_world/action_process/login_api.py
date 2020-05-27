from action_process import login_process
from action_process import login_procedure

procedures = {}


def get_procedure(uid):
    if uid in procedures.keys():
        return procedures[uid]
    return None


def get_qrcode(uid):
    p = get_procedure(uid)
    if p is None:
        p = login_procedure.LoginProcedure(uid)
        procedures[uid] = p

