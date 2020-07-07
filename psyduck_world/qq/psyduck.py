from collections import Awaitable

from aiocqhttp import CQHttp, Event
from qq import config
from qq import short_url
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
        await bot.send(event, f"您没有权限使用大黄鸭，请加群：{config.group_num}")


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

    url = find_csdn_download_url(message)
    if url is not None:
        if qq_num in config.super_user or qq_group in config.super_group:
            await utils.run_async_funcs([async_download], event, url)
            return
        else:
            await bot.send(event, '您没有权限下载，请联系管理员下载。')
            return

    msg = command.handle(cmd, arg)
    if msg == '':
        return
    await bot.send(event, msg)


def find_csdn_download_url(text):
    index = text.find('download.csdn.net/download/')
    if index != -1:
        d_end = index + len('download.csdn.net/download/')
        sp = text[d_end:].find('/')
        if sp != -1 and len(text[d_end + sp + 1:]) > 0:
            id_len = 0
            for i in range(d_end + sp + 1, len(text)):
                if '9' >= text[i] >= '0':
                    id_len += 1
                else:
                    break
            if id_len > 0:
                return 'https://' + text[index:d_end + sp + 1 + id_len]
    return None


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
    db.init()
    bot.run(host=config.host, port=config.port)
