from action_process import login_process
from core import db
import uuid


# inner
def _build(uid, state):
    return {'uid': uid, 'state': state}


def _state(uid):
    return 'none'


def _has(uid):
    return login_process.has(uid)


def _create(uid):
    return login_process.create(uid)


def _check_and_get(uid):
    if not _has(uid):
        return False, _build(uid, 'fail')
    if _state(uid) == 'timeout':
        return False, _build(uid, 'timeout')
    return True, login_process.get(uid)


# api
def get_state(uid):
    return _build(uid, _state(uid))


def get_qr(uid):
    if not _has(uid) or _state(uid) == 'none':
        p = _create(uid)
        return _build(uid, 'ok')
    else:
        return _build(uid, 'fail')


def get_scan_result(uid):
    check, result = _check_and_get(uid)
    if not check:
        return result
    if _state(uid) == 'wait':
        return _build(uid, 'wait')
    if _state(uid) == 'verify':
        return _build(uid, 'verify')
    if _state(uid) == 'ok':
        return _build(uid, 'ok')
    return _build(uid, 'wrong state')


def get_verify_core(uid, phone):
    check, result = _check_and_get(uid)
    if not check:
        return result
    result.get_verify_code(phone)


def validate_csdn(uid, csdn):
    if db.user_get(uid, csdn) is None:
        print(f'用户暂未登陆CSDN账号 {uid} -> {csdn}')
        return

    _condition = {'type': 'user', 'action': 'validate', 'uid': uid, 'message': csdn,
                  '$or': [{'state': 'request'}, {'state': 'process'}]}
    if db.act.find_one(_condition) is not None:
        print(f'正在验证中，请稍等。{uid} -> {csdn}')
        return

    db.act_create(f'test_{uuid.uuid1()}', uid, 'user', 'validate', 'request', csdn)
