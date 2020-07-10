from collections import Awaitable

from aiocqhttp import CQHttp, Event
from qq import config
from core import log
from qq import command
from core import db
from aiocqhttp import utils

bot = CQHttp(access_token=config.token, secret=config.secret)

last_cmd = ''
last_index = 0


def is_at_me(message):
    if message.find('[CQ:at,qq=%s]' % config.qq_num) != -1:
        return True
    return False


def rm_at_me(message):
    return message.replace('[CQ:at,qq=%s]' % config.qq_num, '')


def _is_all_number(_str: str):
    if _str is None or _str == '':
        return False
    for a in _str:
        if not '0' <= a <= '9':
            return False
    return True


@bot.on_message('private')
async def handle_msg_private(event: Event):
    qq_num = int(event.sender['user_id'])
    if qq_num in config.admin_list:
        await handle_msg_group(event)
    else:
        log.info('屏蔽私聊', event.message, qq_num)
        await bot.send(event, f"您没有使用权限，请加群：{config.group_num}")


@bot.on_message('group')
async def handle_msg_group(event: Event):
    global last_cmd
    global last_index

    message = event.message

    if is_at_me(message):
        message = rm_at_me(message)

    message = message.strip()
    cmd = message.split(' ')[0]
    arg = message[len(cmd):].strip()

    qq_num = event.sender['user_id']
    qq_name = event.sender['nickname']
    if 'card' in event.sender and event.sender['card'] != '':
        qq_name = event.sender['card']
    qq_group = -1
    if 'group_id' in event:
        qq_group = event['group_id']

    _id = find_csdn_download_id(message)
    if _id is not None:
        log.info('download', _id, f'group: {qq_group}, qq: {qq_num}')
        if db.download_get(_id) is not None:
            msg = command.handle('-info', _id)
            await bot.send(event, msg)
            return
        elif qq_num in config.super_user or qq_group in config.super_group:
            url = find_csdn_download_url(message)
            await utils.run_async_funcs([async_download], event, url)
            return
        else:
            await bot.send(event, '您没有权限下载，请联系管理员下载。')
            return

    msg = command.handle(cmd, arg)
    if msg == '':
        return
    log.info('command', message, f'group: {qq_group}, qq: {qq_num}')
    await bot.send(event, msg)


def find_csdn_download_id(text):
    def __get_id(_index):
        _index = text.find('/', _index)
        if _index == -1:
            return None
        _index += 1
        for i in range(_index, len(text)):
            if not '9' >= text[i] >= '0':
                return text[_index:i]
        return None

    prefixes = ['download.csdn.net/download/', 'download.csdn.net/detail/']
    for p in prefixes:
        index = text.find(p)
        if index != -1:
            return __get_id(index + len(p))
    return None


def find_csdn_download_url(text):
    _id = find_csdn_download_id(text)
    if _id is None:
        return None
    return f'https://download.csdn.net/download/{_id}'


async def async_download(event, url):
    import asyncio
    from qq import download
    success, token = download.download(url)
    if not success:
        await bot.send(event, token)
        return

    await bot.send(event, '开始下载...')
    while 1:
        await asyncio.sleep(1)
        state, result = download.download_get_state(token)
        if state == 'fail':
            await bot.send(event, result)
            return
        if state == 'done':
            msg = command.handle('-info', result)
            await bot.send(event, msg)
            return


@bot.on_notice('group_increase')
# 上面这句等价于 @bot.on('notice.group_increase')
async def handle_group_increase(context):
    info = await bot.get_group_member_info(group_id=context['group_id'],
                                           user_id=context['user_id'])
    nickname = info['nickname']
    name = nickname if nickname else '新人'
    await bot.send(context,
                   message='欢迎【{}】加入本群～\n友情提示：本群可以免费下载CSDN资源哦！\n-help 查看帮助'.format(name),
                   at_sender=False, auto_escape=True)


@bot.on_request()
# 上面这句等价于 @bot.on('request.group', 'request.friend')
async def handle_group_request(event: Event):
    if event.name != 'request.group.invite':
        return
    if event.user_id in config.admin_list:
        return {'approve': True}
    return {'approve': False, 'reason': f'您没有邀请权限。'}


def main():
    try:
        db.init()
        bot.run(host=config.host, port=config.port)
    except KeyboardInterrupt:
        pass
