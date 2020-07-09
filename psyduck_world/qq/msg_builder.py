from qq import config
from qq import short_url


def separator(n: int = 10):
    return '\n' + '-' * n


def _cut_text(text, size):
    for i in range(len(text)):
        if _text_size(text[0:i + 1]) >= size:
            return text[0:i + 1] + '...'
    return text


def _char_size(c):
    if u'\u4e00' <= c <= u'\u9fa5':
        return 2.167
    else:
        _size = {'a': 1.167, 'b': 1.333, 'c': 1.167, 'd': 1.333, 'e': 1.167, 'f': 0.833, 'g': 1.333, 'h': 1.333,
                 'i': 0.5, 'j': 0.5, 'k': 1.167, 'l': 0.5, 'm': 2, 'n': 1.333, 'o': 1.333, 'p': 1.333, 'q': 1.333,
                 'r': 0.833, 's': 1, 't': 0.833, 'u': 1.333, 'v': 1.167, 'w': 1.667, 'x': 1.167, 'y': 1.167, 'z': 1,
                 'A': 1.5, 'B': 1.333, 'C': 1.5, 'D': 1.667, 'E': 1.167, 'F': 1.167, 'G': 1.667, 'H': 1.667, 'I': 0.667,
                 'J': 0.833, 'K': 1.333, 'L': 1.167, 'M': 2.167, 'N': 1.833, 'O': 1.833, 'P': 1.333, 'Q': 1.833,
                 'R': 1.333, 'S': 1.333, 'T': 1.167, 'U': 1.667, 'V': 1.5, 'W': 2.167, 'X': 1.333, 'Y': 1.333,
                 'Z': 1.333,
                 '.': 0.5, ',': 0.5, ':': 0.5, '[': 0.667, ']': 0.667, '(': 0.667, ')': 0.667, '{': 0.667, '}': 0.667,
                 '+': 1.667, '=': 1.667,
                 '~': 1.667, '!': 0.667, "@": 2.167, '#': 1.333, '$': 1.333, "%": 2, '^': 1.667, '&': 1.833, '*': 1,
                 '_': 1, '|': 0.667, '\\': 0.833, '/': 1, '?': 1, '<': 1.667, '>': 1.667, '"': 1, '\'': 0.5, ';': 0.5,
                 }
        if c in _size:
            return _size[c]
    return 1


def _text_size(text):
    if text == '':
        return 0
    txt_len = 0
    for c in text:
        txt_len += _char_size(c)
    import math
    return math.ceil(txt_len)


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


def build_separator(msg):
    _len = 0
    for m in msg.split('\n'):
        _len = max(_len, _text_size(m))
    return separator(_len)


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
    title = _cut_text(title, 40)
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
    rank = 1
    for d in result:
        info = d['info']
        title = info['title']
        title = _cut_text(title, 40)
        msg += f'\n{rank}. {title}'
        rank += 1
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
