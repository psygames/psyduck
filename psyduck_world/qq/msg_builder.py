from qq import config
from qq import short_url


def separator():
    return '\n' + '——' * 6


def separator_long():
    return '\n' + '——' * 12


def _cut_text(text, size):
    if _text_size(text) <= size:
        return text
    for i in range(len(text)):
        if _text_size(text[0:i]) >= size:
            return text[0:i]
    return text + '...'


def _text_size(text):
    if text == '':
        return 0
    txt_len = len(text)
    txt_len_utf8 = len(text.encode('utf-8'))
    size = int((txt_len_utf8 - txt_len) / 4 + txt_len / 2)
    return size


def _build_url(url):
    if config.short_url:
        return short_url.get(url)
    return url


def source_code_tail():
    if config.source_code_url != '':
        return '\n* 工具源码 %s' % short_url.get(config.source_code_url)
    return ''


def donate_tail():
    if config.donate_url != '':
        return '\n* 黄鸭捐助 %s' % short_url.get(config.donate_url)
    return ''


def build_tails():
    return ''


def _build_info_detail(result):
    info = result['info']
    msg = info['title']
    msg += '\n评分\t：{}{}'.format('★' * info['star'], '☆' * (5 - info['star']))
    msg += '\n所需\t：{} 积分/C币'.format(info['point'])
    msg += '\n大小\t：{}'.format(info['size'])
    msg += '\n下载\t：{}'.format(_build_url(result['share_url']))
    msg += '\nID\t：{}'.format(result['id'])
    msg += '\n类型\t：{}'.format(info['type'])
    msg += '\n文件名\t：{}'.format(info['filename'])
    msg += '\n上传时间：{}'.format(info['upload_time'].strftime("%Y-%m-%d %H:%M:%S"))
    msg += '\n下载时间：{}'.format(result['create_time'].strftime("%Y-%m-%d %H:%M:%S"))
    msg += '\n原始链接：{}'.format(info['url'])
    msg += '\n详细描述：{}'.format(info['description'])
    return msg


def build_info(result, index):
    if index > 0:
        return _build_info_detail(result)
    info = result['info']
    title = info['title']
    title = _cut_text(title, 20)
    msg = title
    msg += '\n评分：{}{}'.format('★' * info['star'], '☆' * (5 - info['star']))
    msg += '\n所需：{} 积分/C币'.format(info['point'])
    msg += '\n大小：{}'.format(info['size'])
    msg += '\n下载：{}'.format(_build_url(result['share_url']))
    return msg


def build_search(result, index):
    if len(result) <= 0:
        return '未找到符合条件的结果。'
    msg = '搜索结果（{0}~{1}）：'.format(index + 1, index + len(result))
    for d in result:
        info = d['info']
        title = info['title']
        title = _cut_text(title, 16)
        _id_sep = '  ' * (8 - len(str(d['id'])))
        msg += '\nID({}){}：{}'.format(d['id'], _id_sep, title)
    return msg


def build_mine(result, index):
    name = result['name']
    msg = f'{name} (功能暂未开放)'
    vip_level = 0
    if vip_level > 0:
        msg += '【VIP%d】' % vip_level
    else:
        msg += '【普通】'
    msg += f'\n本月剩余下载次数：{0}次'
    return msg
