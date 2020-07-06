from aiocqhttp import CQHttp, Event
from qq import config
from qq import short_url
from qq import command
from core import db

bot = CQHttp(access_token=config.token, secret=config.secret)


def find_csdn_download_url(text):
    index = text.find('https://download.csdn.net/download/')
    if index != -1:
        d_end = index + len('https://download.csdn.net/download/')
        spindex = text[d_end:].find('/')
        if spindex != -1 and len(text[d_end + spindex + 1:]) > 0:
            id_len = 0
            for i in range(d_end + spindex + 1, len(text)):
                if '9' >= text[i] >= '0':
                    id_len += 1
                else:
                    break
            if id_len > 0:
                return text[index:d_end + spindex + 1 + id_len]
    return None


def find_csdn_download_id(text):
    url = find_csdn_download_url(text)
    if url is not None:
        return url[url.rfind('/') + 1:]
    return None


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

    msg = command.handle(cmd, arg)
    if msg == '':
        return
    await bot.send(event, msg)
    return

    if cmd == '-help' or cmd == '-?':
        msg = '● 个人信息　-personal'
        msg += '\n● 排行榜　　-rank [index]'
        msg += '\n● 查询文件　-find [keyword]'
        msg += '\n● 文件信息　-info [id]'
        msg += '\n● 更多信息　-more'
        msg += sep_s()
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        msg += '\n* 输入CSDN下载页链接下载'
        # msg += source_code_tail()
        # msg += donate_tail()
        # msg += export_tail()
        last_cmd = cmd
        print(len(msg))
        await bot.send(event, msg)

    if cmd == '-user':
        await bot.send(event, '功能开发中...')

    if cmd == '-rank':
        await bot.send(event, '功能开发中...')

    if cmd == '-find':
        last_cmd = cmd
        last_index = 0
        result = db.download_search(arg, last_index)
        msg = build_find_msg(result, last_index)
        print(len(msg))
        await bot.send(event, msg)


'''
    if cmd == '-info':
        result = db_helper.get_download(arg_int)
        if result is not None:
            msg = build_download_info(result)
            last_cmd = cmd
            last_arg_str = arg_str
            last_arg_int = arg_int
            await bot.send(context, msg)
        else:
            await bot.send(context, '文件不存在。')

    if cmd == '-donors':
        msg = build_donors(arg_int)
        last_cmd = cmd
        last_arg_int = arg_int
        await bot.send(context, msg)

    if cmd == '-personal':
        msg = build_personal(qq_num, qq_group, qq_name)
        await bot.send(context, msg)

    if cmd == '-more':
        if last_cmd == '-find':
            last_arg_int += 10
            result = db_helper.find_all(last_arg_str, last_arg_int)
            count = db_helper.count_all(last_arg_str)
            msg = build_find_msg(result, count, last_arg_int)
            await bot.send(context, msg)
        if last_cmd == '-rank':
            last_arg_int += 10
            result = db_helper.rank_qq(last_arg_int)
            msg = build_rank_msg(result, last_arg_int)
            await bot.send(context, msg)
        if last_cmd == '-info':
            result = db_helper.get_download(last_arg_int)
            if result is not None:
                msg = build_download_detail_info(result)
                await bot.send(context, msg)
        if last_cmd == '-donors':
            last_arg_int += 10
            msg = build_donors(last_arg_int)
            await bot.send(context, msg)
        if last_cmd == '-help' or last_cmd == '-?':
            msg = '● 用户信息　-user'
            msg += '\n● 捐赠名单　-donors'
            msg += sep_s()
            msg += '\n* 输入CSDN下载页链接下载'
            msg += source_code_tail()
            msg += donate_tail()
            msg += export_tail()
            await bot.send(context, msg)

    download_id = find_csdn_download_id(context['message'])
    if download_id is not None:
        if helper.__already_download(download_id) and db_helper.exist_download(download_id):
            msg = build_download_info(db_helper.get_download(download_id))
            await bot.send(context, msg)
            return

    download_url = find_csdn_download_url(context['message'])
    if download_url is not None:
        can_download, msg = helper.check_download_limit(qq_num, qq_group)
        if not can_download:
            await bot.send(context, msg)
            return

        if helper.is_busy():
            await bot.send(context, '资源正在下载中，请稍后...')
            return
        await bot.send(context, '开始下载...')
        try:
            helper.init()
            download_info = helper.auto_download(download_url, qq_num, qq_name, qq_group)
            msg = download_info['message']
            if download_info['success']:
                result = db_helper.get_download(download_info['info']['id'])
                msg = build_download_info(result)
                last_cmd = '-info'
                last_arg_int = int(result.id)
            elif donate_tail() != '':
                msg += sep_s()
                msg += donate_tail()
            await bot.send(context, msg)
        finally:
            helper.dispose()
'''


def source_code_tail():
    if config.source_code_url != '':
        return '\n* 工具源码 %s' % short_url.get(config.source_code_url)
    return ''


def donate_tail():
    if config.donate_url != '':
        return '\n* 黄鸭捐助 %s' % short_url.get(config.donate_url)
    return ''


def export_tail():
    if config.export_url != '':
        return '\n* 资源导出 %s' % short_url.get(config.export_url)
    return ''


def build_tails():
    return ''


def build_download_detail_info(result):
    info = result['info']
    msg = info['title']
    msg += '\n评分\t：{}{}'.format('★' * info['star'], '☆' * (5 - info['star']))
    msg += '\n所需\t：{} 积分/C币'.format(info['point'])
    msg += '\n大小\t：{}'.format(info['size'])
    msg += '\n下载\t：{}'.format(build_url(result['share_url']))
    msg += '\nID\t：{}'.format(result['id'])
    msg += '\n类型\t：{}'.format(info['type'])
    msg += '\n文件名\t：{}'.format(info['filename'])
    msg += '\n上传时间：{}'.format(info['upload_time'].strftime("%Y-%m-%d %H:%M:%S"))
    msg += '\n下载时间：{}'.format(result['create_time'].strftime("%Y-%m-%d %H:%M:%S"))
    msg += '\n原始链接：{}'.format(info['url'])
    msg += '\n详细描述：{}'.format(info['description'])
    return msg


def build_download_info(result):
    info = result['info']
    title = info['title']
    if text_size(title) > 20:
        title = text_sub_size(title, 20) + '...'
    msg = title
    msg += '\n评分：{}{}'.format('★' * info['star'], '☆' * (5 - info['star']))
    msg += '\n所需：{} 积分/C币'.format(info['point'])
    msg += '\n大小：{}'.format(info['size'])
    msg += '\n下载：{}'.format(build_url(result['share_url']))
    msg += sep_l()
    msg += '\n-more 获取更多信息'
    msg += build_tails()
    return msg


def build_url(url):
    if config.short_url:
        return short_url.get(url)
    return url


def build_find_msg(result, index):
    if len(result) <= 0:
        return '未找到符合条件的结果。'
    msg = '搜索结果（{0}~{1}）：'.format(index + 1, index + len(result))
    for d in result:
        info = d['info']
        title = info['title']
        _len = 16
        if text_size(title) > _len:
            title = text_sub_size(title, _len) + '...'
        _id_sep = '  ' * (8 - len(str(d['id'])))
        msg += '\nID({}){}：{}'.format(d['id'], _id_sep, title)
    msg += sep_l()
    msg += '\n-more 获取更多信息'
    msg += '\n-info [id] 下载/查看文件信息'
    return msg


def text_sub_size(text, size):
    for i in range(len(text)):
        if text_size(text[0:i]) >= size:
            return text[0:i]
    return text


def text_size(text):
    if text == '':
        return 0
    txt_len = len(text)
    txt_len_utf8 = len(text.encode('utf-8'))
    size = int((txt_len_utf8 - txt_len) / 4 + txt_len / 2)
    return size


def build_rank_msg(result, start_index=0):
    if len(result) <= 0:
        return '没有更多信息了。'
    msg = '排行榜（{}~{}）：'.format(start_index + 1, start_index + len(result))
    index = start_index + 1
    for fo in result:
        name = build_name_str(fo[1]['name'])
        msg += '\n{}.{}\t{}次\t(共消耗{}积分)'.format(index, name, fo[1]['count'], fo[1]['coin'])
        index += 1
    msg += sep_l()
    msg += '\n-more 获取更多信息'
    return msg


def build_name_str(name):
    name = '【{}】{}'.format(name, (10 - text_size(name)) * '　')
    return name


def build_donors(start_index=0):
    if start_index >= len(config.donate_list):
        return '没有更多信息了。'
    _len = min(10, len(config.donate_list) - start_index)
    msg = '捐赠名单 共{}条（{}~{}）：'.format(len(config.donate_list), start_index + 1, start_index + _len)
    total = 0
    for i in range(0, len(config.donate_list)):
        total += float(config.donate_list[i]['money'])
    for i in range(start_index, start_index + _len):
        donor = config.donate_list[i]
        name = build_name_str(donor['name'])
        rmb = donor['money']
        msg += '\n{}\t￥{}'.format(name, rmb)
    msg += sep_l()
    msg += '\n{}\t￥{}'.format(build_name_str('共计'), total)
    msg += '\n-more 获取更多信息'
    return msg


def build_personal(qq_num, qq_group, name):
    msg = '{}'.format(name)
    vip_level = 0
    for donor in config.donate_list:
        if donor['qq'] == qq_num:
            vip_level = int(donor['money'] ** 0.3)
            break

    if vip_level > 0:
        msg += '【VIP%d】' % vip_level
    else:
        msg += '【普通】'

    _d_used = db_helper.count_daily(qq_num, qq_group)
    _d_total = helper.daily_download_count(qq_num)
    msg += '\n本日剩余下载次数：{}/{}次'.format(_d_total - _d_used, _d_total)
    _w_used = db_helper.count_weekly(qq_num, qq_group)
    _w_total = helper.weekly_download_count(qq_num)
    msg += '\n本周剩余下载次数：{}/{}次'.format(_w_total - _w_used, _w_total)
    _m_used = db_helper.count_monthly(qq_num, qq_group)
    _m_total = helper.monthly_download_count(qq_num)
    msg += '\n本月剩余下载次数：{}/{}次'.format(_m_total - _m_used, _m_total)
    return msg


def sep_s():
    return '\n' + '-' * 29


def sep_l():
    return '\n' + '-' * 56


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


'''
@bot.on_request('group')
# 上面这句等价于 @bot.on('request.group', 'request.friend')
async def handle_group_request(context):
    if context['message'] == 'Psyduck~':
        return {'approve': True}
    # 验证信息不符，拒绝
    return {'approve': False, 'reason': '请输入正确的入群口令'}
'''


def main():
    db.init()
    bot.run(host=config.host, port=config.port)
