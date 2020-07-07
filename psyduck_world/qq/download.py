import uuid

from core import db
from qq import config


def _gen_token(prefix=''):
    if prefix == '':
        return uuid.uuid4()
    return f'{prefix}_{uuid.uuid4()}'


def download_get_state(token):
    uid = config.download_user
    act = db.act.find_one({'id': token, 'uid': uid})
    if act is None:
        return 'fail' '令牌错误。'
    return act['state'], act['result']


def download(url):
    uid = config.download_user
    csdn = config.download_csdn

    _condition = {'action': 'download', 'uid': uid, 'message.url': url,
                  '$nor': [{'state': 'fail'}, {'state': 'done'}]}
    if db.act.find_one(_condition) is not None:
        return False, '正在下载，请勿重复提交。'

    token = _gen_token('qq_download')
    db.act_create(token, uid, 'download', 'request', {'csdn': csdn, 'url': url})
    return True, token
