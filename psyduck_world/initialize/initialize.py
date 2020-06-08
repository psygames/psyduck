import core.db
import initialize.clear
import os
import core.path


def init():
    create_dir()
    initialize.clear.clear_caches()
    core.db.init()
    core.db.act_reset()
    # core.db.act_test()
    return True


def create_dir():
    dirs = [
        core.path.frozen_path('caches/'),
        core.path.frozen_path('caches/downloads/'),
        core.path.frozen_path('caches/drivers/'),
        core.path.frozen_path('caches/zips/'),
        core.path.frozen_path('caches/options/'),
    ]

    for _dir in dirs:
        if not os.path.exists(_dir):
            os.mkdir(_dir)
