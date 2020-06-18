import sys
import json
from datetime import datetime

sys.path.append('../')

from core import db
from core import path


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('ISODate(%Y-%m-%dT%H:%M:%S.%fZ)')
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(dic):
    return json.dumps(dic, ensure_ascii=False, indent=4, cls=MyJSONEncoder)


db.init()
_dic = []
for d in db.download.find({}):
    d.pop('_id')
    _dic.append(d)
print(f'共 {len(_dic)} 条数据')
_str = json_dumps(_dic)
_path = path.frozen_path('kits/backup.db')
print('开始备份...')
f = open(path.frozen_path('kits/backup.db'), mode='w', encoding='utf8')
f.write(_str)
f.close()
print(f'备份完成：{_path}')
