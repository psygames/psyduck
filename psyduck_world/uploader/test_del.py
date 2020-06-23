from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

lzy = LanZouCloud()

dir_list: ItemList = ItemList()
file_list: ItemList = ItemList()


def login():
    global lzy
    cookie = {'ylogin': '1104264',
              'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'}
    code = lzy.login_by_cookie(cookie)
    if code == LanZouCloud.SUCCESS:
        return True
    return False


def all_file_to_queue():
    global dir_list
    global file_list

    print('获取文件列表...')
    dirs = lzy.get_dir_list()
    csdn = dirs.find_by_name('psyduck')

    dir_list = lzy.get_dir_list(csdn.id)
    file_list = lzy.get_file_list(csdn.id)


def test():
    for f in file_list:
        if f.name == '5265765.zip':
            print('找到文件！')

    fi = file_list.find_by_name('5265765.zip')
    if fi is not None:
        if lzy.delete(fi.id, True) == LanZouCloud.SUCCESS:
            print('删除成功')
        else:
            print('删除失败')
    else:
        print('未找到文件')


def main():
    try:
        if not login():
            print('登陆错误')
            return
        all_file_to_queue()
        test()
    except KeyboardInterrupt:
        pass
    except:
        main()


if __name__ == '__main__':
    main()
