from action_process import login_process
from core import db
import uuid
import json


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


def _uuid(prefix=''):
    if prefix == '':
        return uuid.uuid4()
    return f'{prefix}_{uuid.uuid4()}'


# token
def get_token(uid):


# login
def get_state(uid):
    return _build(uid, _state(uid))


def _build_login(_id, uid, status, message):


def login_get_qr_code(_id, uid, state):
    if state == 'request' or state == '':
        # do request
        db.act_create(_uuid('login'), uid, 'user', 'login', 'request')
    elif state == 'scan':


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


# validate
def _validate_build(_id, uid, csdn, status, message):
    dic = {'status': status, 'id': _id, 'uid': uid, 'csdn': csdn, 'message': message}
    return json.dumps(dic, ensure_ascii=False, indent=4)


def validate_csdn(_id, uid, csdn):
    if _id is None or _id == '':
        if db.user_get(uid, csdn) is None:
            print(f'用户暂未登陆CSDN账号 {uid} -> {csdn}')
            return _validate_build('', uid, csdn, 'error', '用户暂未登陆CSDN账号')

        _condition = {'type': 'user', 'action': 'validate', 'uid': uid, 'message': csdn,
                      '$or': [{'state': 'request'}, {'state': 'process'}]}
        if db.act.find_one(_condition) is not None:
            print(f'当前账户正在验证中，请勿重复提交。{uid} -> {csdn}')
            return _validate_build('', uid, csdn, 'error', '当前账户正在验证中，请勿重复提交。')

        _id = _uuid('validate')
        db.act_create(_id, uid, 'user', 'validate', 'request', csdn)
        return _validate_build(_id, uid, csdn, 'ok', '开始验证...')
    else:
        act = db.act.find_one({'id': _id})
        if act is None:
            return validate_csdn('', uid, csdn)
        if act['state'] == 'request' or act['state'] == 'process':
            return _validate_build(_id, uid, csdn, 'ok', '正在验证中...')
        if act['state'] == 'fail':
            return _validate_build(_id, uid, csdn, 'error', act['result'])
        if act['state'] == 'done':
            return _validate_build(_id, uid, csdn, 'ok', act['result'])
        return _validate_build(_id, uid, csdn, 'error', 'unknown')
