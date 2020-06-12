from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList
from threading import Thread
import os
import time
import shutil
from core import db

lzy = LanZouCloud()

file_list: ItemList = ItemList()
dir_list: ItemList = ItemList()
file_dir = os.path.abspath('./downloads')
upload_folder_id = -1
db.init()


def login():
    print('登陆账号...')
    global lzy
    cookie = {'ylogin': '1104264',
              'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'}

    cookie = {'ylogin': '1494080',
              'phpdisk_info': 'ADVXYQ1mVW1VZ1I6D2UGVVE1AgkAaF0yBDUBYwE2VGNYa1ZnAGYDPVBnDldbOAA7U2IFZQswUTUBMwJlAWMCZABlV2YNalVtVWNSNQ9jBmVRZwJjADhdOAQxAWMBN1Q3WGRWYAA0AzZQMQ46WwgAa1M7BTULYFE3ATcCZQE0AjQANldg'}

    code = lzy.login_by_cookie(cookie)
    if code == LanZouCloud.SUCCESS:
        return True
    return False


def clear():
    pass


def init():
    global upload_folder_id
    lzy.ignore_limits()
    print('初始化...')
    dirs = lzy.get_dir_list()
    upload_folder_id = dirs.find_by_name('psyduck').id


def catch_all():
    global file_list
    global dir_list
    file_list = lzy.get_file_list(upload_folder_id)
    dir_list = lzy.get_dir_list(upload_folder_id)


def upload_all():
    cur = 1
    total = len(os.listdir(file_dir))
    for fi in os.listdir(file_dir):
        _id = fi[:-4]
        data = db.download_get(_id)
        print(f'进度：{cur}/{total}')
        upload_file(os.path.join(file_dir, fi), data)
        cur += 1


def save_share_url(_id, file_id, is_file):
    info = lzy.get_share_info(file_id, is_file)
    if info.code != LanZouCloud.SUCCESS:
        print(f'获取分享链接失败！({info.code})')
    db.download_add_share_url(_id, info.url)


def upload_file(file_path, data):
    _id = data['id']
    if data is None:
        print(f'数据库中未找到文件：{_id}')
        return
    if file_list.find_by_name(f'{_id}.zip') is not None:
        save_share_url(_id, file_list.find_by_name(f'{_id}.zip').id, True)
        print(f'已上传文件：{_id}')
        return
    if dir_list.find_by_name(f'{_id}.zip') is not None:
        _merge_dir = dir_list.find_by_name(f'{_id}.zip')
        save_share_url(_id, _merge_dir.id, False)
        _merge_files = lzy.get_file_list(_merge_dir.id)
        _temp_uploaded = False
        for _merge_item in _merge_files:
            if _merge_item.name.endswith('.txt'):
                _temp_uploaded = True
        if _temp_uploaded:
            print(f'已上传大文件：{_id}')
            return

    def _uploading_c(file_name, total_size, now_size):
        uploading_callback(file_name, total_size, now_size, data)

    def _uploaded_c(fid, is_file):
        uploaded_callback(fid, is_file, data)

    print(f'开始上传：{data["id"]} {data["csdn"]["size"]}')
    code = lzy.upload_file(file_path, upload_folder_id, callback=_uploading_c, uploaded_handler=_uploaded_c)
    if code != LanZouCloud.SUCCESS:
        print(f'上传失败({code})：{data["id"]}')


def uploading_callback(file_name, total_size, now_size, data):
    # print(f'{file_name}：上传中[{now_size}/{total_size}]...')
    pass


def uploaded_callback(fid, is_file, data):
    save_share_url(data["id"], fid, is_file)
    lzy.set_passwd(fid, '', is_file)
    desc = f'{data["csdn"]["title"]}\n{data["csdn"]["description"]}'
    lzy.set_desc(fid, desc, is_file)
    print(f'上传完成：{data["id"]}')


def main():
    try:
        if not login():
            print('登陆错误')
            return
        clear()
        init()
        catch_all()
        upload_all()
    except KeyboardInterrupt:
        pass
    except:
        import traceback
        traceback.print_exc()
        main()


if __name__ == '__main__':
    main()
