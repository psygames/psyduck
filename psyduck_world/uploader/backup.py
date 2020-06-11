from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList
from threading import Thread
import os
import time
import shutil

lzy = LanZouCloud()

dir_queue: ItemList = None
file_queue: ItemList = None


def login():
    global lzy
    cookie = {'ylogin': '1104264',
              'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'}
    code = lzy.login_by_cookie(cookie)
    if code == LanZouCloud.SUCCESS:
        return True
    return False


def all_file_to_queue():
    global dir_queue
    global file_queue

    dirs = lzy.get_dir_list()
    print(dirs)
    csdn = dirs.find_by_name('CSDN')
    csdn_dirs = lzy.get_dir_list(csdn.id)
    print(csdn_dirs)
    dir_queue = csdn_dirs
    csdn_files = lzy.get_file_list(csdn.id)
    print(csdn_files)
    file_queue = csdn_files


def download_all():
    save_dir = os.path.abspath('./downloads');
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    cur = 1.0
    total = len(file_queue) + len(dir_queue)
    for p in dir_queue:
        print(f'进度：{cur}/{total}')
        download_dir(p)
    for p in file_queue:
        print(f'进度：{cur}/{total}')
        dowload_file(p, download_dir)


def dowload_file(_file, dir):
    print(f'开始下载：{_file.name}，大小：{_file.size}')
    lzy.down_file_by_id(_file.id, dir)


def download_dir(_file):
    print(f'开始下载：{_file.name}')
    sub_files = lzy.get_file_list(_file.id)
    save_dir = os.path.abspath(f'./downloads/_temp')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for p in sub_files:
        dowload_file(p, save_dir)
    bat = f'{save_dir}/combine.bat'
    with open(f'{bat}', 'r') as f:
        f.readline()
        cmd = f.readline()
    cwd = os.getcwd() + '\n exit 1'
    os.chdir(save_dir)
    wnd = os.popen(cmd)
    os.chdir(cwd)
    wnd.close()
    shutil.move(f'{save_dir}/{_file.name}', f'{save_dir}/../{_file.name}')
    shutil.rmtree(f'{save_dir}')


def main():
    if not login():
        print('登陆错误')
        return
    all_file_to_queue()
    download_all()


if __name__ == '__main__':
    main()
