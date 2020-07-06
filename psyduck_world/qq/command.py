from qq import msg_builder as mb
from core import db
import qq

commands = {
    'search': {'name': '搜索资源', 'cmd': ['-find', '搜索'], 'more': True, 'display': True},
    'info': {'name': '查看信息', 'cmd': ['-info', '查看'], 'more': True, 'display': True},
    'mine': {'name': '我的信息', 'cmd': ['-mine', '我的'], 'more': False, 'display': True},
    'help': {'name': '查看帮助', 'cmd': ['-help', '帮助'], 'more': True, 'display': True},
    'more': {'name': '更多信息', 'cmd': ['-more', '更多'], 'more': False, 'display': False},
}

cmd = ''
arg = ''
index = 0
msg_tail = ''


def _search(keyword):
    global msg_tail
    result = db.download_search(keyword, index, 3)
    msg = mb.build_search(result, index)
    msg_tail += '\n-info 1 查看文件信息'
    return msg


def _info(_arg):
    pass


def _download(_arg):
    pass


def _help(_arg):
    global msg_tail
    msg = ''
    for c in commands:
        if not commands[c]['display']:
            continue
        name = commands[c]['name']
        _cmd = commands[c]['cmd'][0]
        msg += f'● {name}\t {_cmd}\n'
    msg = msg[:-1]
    msg_tail = '\n* 输入CSDN下载页链接下载'
    return msg


def _mine(_arg):
    pass


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
    if commands[_cmd]['more']:
        msg += mb.separator()
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
    for c in commands:
        if _cmd in commands[c]['cmd']:
            right_cmd = True
            cmd = c
            break

    if not right_cmd:
        return ''

    arg = _arg
    index = 0
    return _handle(cmd, arg)
