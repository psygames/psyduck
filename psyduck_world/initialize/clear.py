import core.config
import os
import shutil


def clear_caches():
    for fi in os.listdir(core.config.frozen_path('caches/options/')):
        if fi.startswith('_tmp_option_'):
            shutil.rmtree(core.config.frozen_path(f'caches/options/{fi}'))
            print(f'已清理 option: {fi}')
    for fi in os.listdir(core.config.frozen_path('caches/drivers/')):
        shutil.rmtree(f'caches/drivers/{fi}')
        print(f'已清理 driver: {fi}')
