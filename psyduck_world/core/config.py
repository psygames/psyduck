import os
import sys


def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):  # Handles PyInstaller
        return os.path.dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__).split('core')[0]  # 没打包前的py目录


def frozen_path(_path):
    if os.path.isabs(_path):
        return _path
    return os.path.join(app_path(), _path)
