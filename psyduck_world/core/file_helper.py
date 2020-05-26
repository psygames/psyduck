import os
import shutil
import core.path
import time


def _option_path(name):
    return core.path.frozen_path(f'caches/options/{name}')


def lock_option(name):
    _path = _option_path(name + '.lock')
    if not os.path.isfile(_path):  # 无文件时创建
        fd = open(_path, mode='w', encoding='utf-8')
        fd.close()


def unlock_option(name):
    _path = _option_path(name + '.lock')
    os.remove(_path)


def is_lock_option(name):
    return os.path.exists(_option_path(name + '.lock'))


def wait_check_lock(name):
    timeout = 60
    while timeout > 0:
        if not is_lock_option(name):
            return False
        timeout -= 1
        time.sleep(1)
    print(f'option 文件已锁定: {name}')
    return True


def move_option(src_name, des_name):
    if wait_check_lock(src_name):
        return False
    if wait_check_lock(src_name):
        return False

    lock_option(src_name)
    lock_option(des_name)
    _src_path = _option_path(src_name)
    _des_path = _option_path(des_name)
    if os.path.exists(_des_path):
        shutil.rmtree(_des_path)
    shutil.move(_src_path, _src_path)
    unlock_option(src_name)
    unlock_option(des_name)
    return True


def copy_option(src_name, des_name):
    if wait_check_lock(src_name):
        return False
    if wait_check_lock(src_name):
        return False

    lock_option(src_name)
    lock_option(des_name)
    _src_path = _option_path(src_name)
    _des_path = _option_path(des_name)
    if os.path.exists(_des_path):
        shutil.rmtree(_des_path)
    shutil.copytree(_src_path, _des_path)
    unlock_option(src_name)
    unlock_option(des_name)
    return True


def remove_option(name):
    if wait_check_lock(name):
        return False
    lock_option(name)
    _path = _option_path(name)
    shutil.rmtree(_path)
    unlock_option(name)
    return True
