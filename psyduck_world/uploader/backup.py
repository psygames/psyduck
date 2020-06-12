from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

lzy = LanZouCloud()

dir_queue: ItemList = ItemList()
file_queue: ItemList = ItemList()

executor = ThreadPoolExecutor(max_workers=5)
tasks = []


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

    print('获取文件列表...')
    dirs = lzy.get_dir_list()
    csdn = dirs.find_by_name('CSDN')

    csdn_dirs = lzy.get_dir_list(csdn.id)
    dir_queue = csdn_dirs

    # csdn_files = lzy.get_file_list(csdn.id)
    # file_queue = csdn_files


def lock(_file):
    _file = f'{_file}.lock'
    open(_file, mode='w').close()


def unlock(_file):
    _file = f'{_file}.lock'
    os.remove(_file)


def clear():
    save_dir = os.path.abspath('./downloads')
    for f in os.listdir(save_dir):
        if f.endswith('.lock'):
            _lock = f'{save_dir}/{f}'
            _file = f'{_lock[:-5]}'
            if os.path.exists(_file):
                os.remove(_file)
            os.remove(_lock)
    _temp = f'{save_dir}/_temp'
    if os.path.exists(_temp):
        shutil.rmtree(_temp)


def download_all():
    save_dir = os.path.abspath('./downloads')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    cur = 1.0
    total = len(file_queue) + len(dir_queue)
    for p in file_queue:
        print(f'进度：{cur}/{total}')
        dowload_file(p, save_dir)
        cur += 1
    for p in dir_queue:
        print(f'进度：{cur}/{total}')
        download_dir(p, save_dir)
        cur += 1


def dowload_file(_file, _dir):
    final_file = os.path.abspath(f'{_dir}/{_file.name}')
    if os.path.exists(final_file):
        print(f'已存在：{_file.name}')
        return
    lock(final_file)
    print(f'开始下载：{_file.name}，大小：{_file.size}')
    lzy.down_file_by_id(_file.id, _dir)
    unlock(final_file)


def download_dir(_file, _dir):
    final_file = os.path.abspath(f'{_dir}/{_file.name}')
    if os.path.exists(final_file):
        print(f'已存在：{_file.name}')
        return
    sub_files = lzy.get_file_list(_file.id)
    if len(sub_files) == 0:
        print(f'空文件夹：{_file.name}')
        return

    lock(final_file)
    print(f'开始下载：{_file.name}')
    _temp_save_dir = os.path.abspath(f'./downloads/_temp')
    if not os.path.exists(_temp_save_dir):
        os.mkdir(_temp_save_dir)
    for p in sub_files:
        dowload_file(p, _temp_save_dir)

    merge = open(final_file, mode='wb')
    for i in range(1, 1000):
        part = f'{_temp_save_dir}/{_file.name[:-4]}.part{i}.zip'
        if not os.path.exists(part):
            break
        part_file = open(part, mode='rb')
        merge.write(part_file.read())
        part_file.close()
    merge.close()
    shutil.rmtree(_temp_save_dir)
    unlock(final_file)


def main():
    try:
        if not login():
            print('登陆错误')
            return
        clear()
        all_file_to_queue()
        download_all()
    except KeyboardInterrupt:
        pass
    except:
        main()


if __name__ == '__main__':
    main()
