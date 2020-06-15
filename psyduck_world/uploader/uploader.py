import ctypes
import inspect

from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList
import os
from datetime import datetime
from core import db
from core import path
import time
import shutil

db.init()


class Uploader:
    lzy = LanZouCloud()
    name = ''
    file_list: ItemList = ItemList()
    dir_list: ItemList = ItemList()
    file_dir = os.path.abspath(path.frozen_path('caches/downloads'))
    cookies = {}
    upload_folder_id = -1
    max_thread_count = 5
    update_share_url = False
    set_share_url = False
    upload_use_copy = True
    upload_index = 0
    upload_total = 0
    temp_copy_dir = ''
    need_catch_all = True

    def __init__(self, setting):
        self.name = setting['name']
        self.cookies = setting['cookies']
        self.set_share_url = setting['set_share_url']
        self.update_share_url = setting['update_share_url']
        self.temp_copy_dir = os.path.join(self.file_dir, f'__{self.name}__')

    def start(self):
        while 1:
            try:
                if not self.init():
                    self.log('初始化失败！')
                else:
                    self.catch_all()
                    self.upload_all()
            except:
                import traceback
                self.log(traceback.format_exc())
            time.sleep(1)

    def init(self):
        self.log('初始化...')
        self.clear()
        self.lzy.ignore_limits()
        if not self.login():
            self.log('登陆错误')
            return False
        return True

    def clear(self):
        self.log('清除临时文件...')
        if os.path.exists(self.temp_copy_dir):
            shutil.rmtree(self.temp_copy_dir)

    def login(self):
        self.log('登陆账号...')
        code = self.lzy.login_by_cookie(self.cookies)
        if code == LanZouCloud.SUCCESS:
            return True
        return False

    def log(self, _str):
        _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{_time} > [{self.name}] {_str}')

    def catch_all(self):
        if not self.need_catch_all:
            return
        self.log('拉取数据中...')
        dirs = self.lzy.get_dir_list()
        self.upload_folder_id = dirs.find_by_name('psyduck').id
        self.file_list = self.lzy.get_file_list(self.upload_folder_id)
        self.dir_list = self.lzy.get_dir_list(self.upload_folder_id)

    def upload_all(self):
        self.log('开始上传...')
        self.need_catch_all = False
        self.upload_index = 0
        self.upload_total = len(os.listdir(self.file_dir))
        for fi in os.listdir(self.file_dir):
            if not fi.endswith('.zip'):
                continue
            _id = fi[:-4]
            data = db.download_get(_id)
            # self.log(f'进度：{cur}/{total}')
            self.upload_file(os.path.join(self.file_dir, fi), data)
            self.upload_index += 1
        self.log('全部上传完成！')

    def save_share_url(self, _id, file_id, is_file):
        if not self.set_share_url:
            return
        info = self.lzy.get_share_info(file_id, is_file)
        if info.code != LanZouCloud.SUCCESS:
            self.log(f'获取分享链接失败！({info.code})')
            return
        self.log(f'更新分享链接({self.upload_index}/{self.upload_total})：{_id} {info.url}')
        db.download_set_share_url(_id, info.url)

    def upload_file(self, file_path, data):
        # 数据校验
        if data is None:
            self.log(f'数据库中未找到文件：{os.path.basename(file_path)}')
            return

        _id = data['id']

        # 文件校验
        if self.file_list.find_by_name(f'{_id}.zip') is not None:
            if self.update_share_url:
                self.save_share_url(_id, self.file_list.find_by_name(f'{_id}.zip').id, True)
            # self.log(f'已上传文件：{_id}')
            return
        if self.dir_list.find_by_name(f'{_id}.zip') is not None:
            _merge_dir = self.dir_list.find_by_name(f'{_id}.zip')
            _merge_files = self.lzy.get_file_list(_merge_dir.id)
            _temp_uploaded = False
            for _merge_item in _merge_files:
                if _merge_item.name.endswith('.txt'):
                    _temp_uploaded = True
            if _temp_uploaded:
                if self.update_share_url:
                    self.save_share_url(_id, _merge_dir.id, False)
                # self.log(f'已上传大文件：{_id}')
                return
            else:
                self.log(f'已损坏的大文件：{_id}')

        # 文件拷贝
        if not os.path.exists(self.temp_copy_dir):
            os.mkdir(self.temp_copy_dir)
        _copy_path = os.path.join(self.temp_copy_dir, os.path.basename(file_path))
        shutil.copy(file_path, _copy_path)

        # 文件上传
        self.log(f'开始上传({self.upload_index}/{self.upload_total})：{data["id"]} {data["csdn"]["size"]}')
        code = self.lzy.upload_file(_copy_path, self.upload_folder_id, callback=self.uploading_callback,
                                    uploaded_handler=self.uploaded_callback)

        if code != LanZouCloud.SUCCESS:
            self.log(f'上传失败({code})：{_id}')
        else:
            self.log(f'上传完成：{_id}')

        # 文件清理
        if os.path.exists(_copy_path):
            self.log(f'清理临时文件：{os.path.basename(_copy_path)}')
            os.remove(_copy_path)

        # catch all
        self.need_catch_all = True

    def uploading_callback(self, file_name, total_size, now_size):
        # self.log(f'{file_name}：上传中[{now_size}/{total_size}]...')
        pass

    def uploaded_callback(self, fid, is_file):
        _id = ''
        if is_file:
            _id = self.lzy.get_file_info_by_id(fid).name[:-4]
        else:
            _id = self.lzy.get_folder_info_by_id(fid).folder.name[:-4]
        data = db.download_get(_id)
        self.save_share_url(_id, fid, is_file)
        self.lzy.set_passwd(fid, '', is_file)
        desc = f'{data["csdn"]["title"]}\n{data["csdn"]["description"]}'
        self.lzy.set_desc(fid, desc, is_file)

    def dispose(self):
        pass


def main():
    settings = [
        {
            'name': 'admin',
            'set_share_url': True,
            'update_share_url': False,
            'cookies': {
                'ylogin': '1104264',
                'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'
            }
        },
        {
            'name': 'admin_backup',
            'set_share_url': False,
            'update_share_url': False,
            'cookies': {
                'ylogin': '1494080',
                'phpdisk_info': 'ADVXYQ1mVW1VZ1I6D2UGVVE1AgkAaF0yBDUBYwE2VGNYa1ZnAGYDPVBnDldbOAA7U2IFZQswUTUBMwJlAWMCZABlV2YNalVtVWNSNQ9jBmVRZwJjADhdOAQxAWMBN1Q3WGRWYAA0AzZQMQ46WwgAa1M7BTULYFE3ATcCZQE0AjQANldg'
            }
        },
    ]
    u_index = 0
    u = None
    try:
        u = Uploader(settings[u_index])
        u.start()
    except KeyboardInterrupt:
        if u is not None:
            u.dispose()


if __name__ == '__main__':
    main()
