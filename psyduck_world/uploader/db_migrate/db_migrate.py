from uploader.db_migrate import db_helper
from core import db

db.init()
_count = db_helper.count_all('')
_all = db_helper.find_all('', 0, _count)
index = 1
for a in _all:
    b: db_helper.Download = a
    # db.download_create(b.id, 'admin', 'y85171642', b.url, b.title, b.type, b.size, b.tag, b.description, b.filename,
    #                   b.coin, b.stars, b.upload_date, b.qq_group, b.qq_num, b.qq_name, b.download_url, b.created_date)
    print(f'导入 {index} 条：{b.filename}')
    index += 1
