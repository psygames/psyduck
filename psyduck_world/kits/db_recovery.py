import sys
import json
import os
from datetime import datetime
from datetime import date

sys.path.append('../')

from core import db
from core import path


def json_loads(_str):
    dic = json.loads(_str)

    def set_dt(_dic):
        for k in _dic:
            if type(_dic[k]) is str and _dic[k].startswith('ISODate(') and _dic[k].endswith('Z)'):
                _dic[k] = datetime.strptime(_dic[k], 'ISODate(%Y-%m-%dT%H:%M:%S.%fZ)')
            elif type(_dic[k]) is dict:
                set_dt(_dic[k])

    for a in dic:
        set_dt(a)

    return dic


_path = path.frozen_path('kits/backup.db')
if not os.path.exists(_path):
    print(f'未找到备份文件：{_path}')
    exit(0)

f = open(_path, mode='r', encoding='utf8')
_str = f.read()
f.close()
_dic = json_loads(_str)
print(f'共 {len(_dic)} 条数据')
print('开始恢复...')
db.init()
new = 0
up = 0
for d in _dic:
    if db.download_get(d['id']) is None:
        db.download.insert_one(d)
        new += 1
    else:
        pass
        up += 1
        # db.download.update_one({'id': d['id']}, {'$set': d})
print(f'恢复完成：新增 {new} 条，更新 {up} 条')
