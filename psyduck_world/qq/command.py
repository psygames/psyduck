from qq import msg_builder as mb
from core import db
import qq

commands = {
    'find': {'name': '搜索资源', 'cmd': ['-find', '搜索', ], 'more': True, 'display': True},
    'info': {'name': '查看信息', 'cmd': ['-info', '查看', ], 'more': True, 'display': True},
    'mine': {'name': '我的信息', 'cmd': ['-mine', '我的', ], 'more': False, 'display': True},
    'help': {'name': '查看帮助', 'cmd': ['-help', '帮助', '-?', '-？'], 'more': True, 'display': True},
    'more': {'name': '更多信息', 'cmd': ['-more', '更多', ], 'more': False, 'display': False},
}

cmd = ''
arg = ''
index = 0
msg_tail = ''

_find_result = []


def _is_all_number(_str: str):
    if _str is None or _str == '':
        return False
    for a in _str:
        if not '0' <= a <= '9':
            return False
    return True


def _find(_arg):
    global msg_tail
    global _find_result
    result = db.download_search(_arg, index, 10)
    _find_result = result
    msg = mb.build_search(result, index)
    msg_tail += '\n-info 1~10 查看文件信息'
    return msg


def _info(_arg):
    if not _is_all_number(_arg):
        return '参数错误！'
    i = int(_arg)
    if 0 < i <= len(_find_result):
        result = _find_result[i - 1]
    else:
        result = db.download_get(_arg)
    if result is None:
        return '未找到文件信息！'
    return mb.build_info(result, index)


def _help(_arg):
    global msg_tail
    msg = ''
    for c in commands:
        if not commands[c]['display']:
            continue
        name = commands[c]['name']
        _cmd = commands[c]['cmd'][0]
        msg += f'● {_cmd}  {name}\n'
    msg = msg[:-1]
    msg_tail = '\n*输入CSDN下载地址下载'
    return msg


def _mine(_arg):
    return '功能开发中...'


def _more(_arg):
    global index
    if cmd not in commands:
        return
    if not commands[cmd]['more']:
        return
    index += 10
    return _handle(cmd, arg)


def _handle(_cmd, _arg):
    global msg_tail
    target_func = f'_{_cmd}'
    msg_tail = ''
    func = getattr(qq.command, target_func)
    msg = func(_arg)
    if _cmd == 'more':
        return msg
    if len(msg.split('\n')) <= 1:
        return msg
    msg += mb.build_separator(msg)
    if commands[_cmd]['more']:
        msg += '\n-more 获取更多信息'
    if msg_tail != '':
        msg += f'{msg_tail}'
    msg += mb.build_tails()
    return msg


def handle(_cmd, _arg) -> str:
    global cmd
    global arg
    global index

    right_cmd = False
    sent_cmd = ''
    for c in commands:
        if _cmd not in commands[c]['cmd']:
            continue
        right_cmd = True
        sent_cmd = c
        break

    if not right_cmd:
        return ''

    if sent_cmd != 'more':
        cmd = sent_cmd
        arg = _arg
        index = 0

    return _handle(sent_cmd, arg)
