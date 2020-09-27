from lanzou.api import LanZouCloud
from lanzou.api.models import ItemList

lzy = LanZouCloud()

root_dirs: ItemList = ItemList()
dir_list: ItemList = ItemList()
file_list: ItemList = ItemList()

is_login = False


def _login():
    global is_login
    global lzy
    print("开始登陆...")
    cookie = {'ylogin': '1104264',
              'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'}
    code = lzy.login_by_cookie(cookie)
    if code == LanZouCloud.SUCCESS:
        print("登陆成功！")
        is_login = True
        return True
    print("登陆失败！")
    return False


def list_files(root_folder_name, is_file=True):
    global dir_list
    global file_list
    global root_dirs

    if not is_login:
        _login()
    if not is_login:
        return

    print('获取文件列表...')
    root_dirs = lzy.get_dir_list()
    target_dir = root_dirs.find_by_name(root_folder_name)
    if is_file:
        return lzy.get_file_list(target_dir.id)
    else:
        return lzy.get_dir_list(target_dir.id)


def get_share_url(fid, is_file=True):
    return lzy.get_share_info(fid, is_file).url


def main():
    lst1, lst2 = list_files("CSDN")
    for i in lst1:
        print(i)
    for ii in lst2:
        print(ii)


if __name__ == '__main__':
    main()
