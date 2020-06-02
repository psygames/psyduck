import core.path
import os
import shutil


def clear_caches():
    for fi in os.listdir(core.path.frozen_path('caches/options/')):
        if os.path.isdir(core.path.frozen_path(f'caches/options/{fi}')) and fi.startswith('_tmp_option_'):
            shutil.rmtree(core.path.frozen_path(f'caches/options/{fi}'))
            print(f'已清理 option: {fi}')
        elif os.path.isfile(core.path.frozen_path(f'caches/options/{fi}')) and fi.endswith('.lock'):
            os.remove(core.path.frozen_path(f'caches/options/{fi}'))
            print(f'已清理 option: {fi}')
    for fi in os.listdir(core.path.frozen_path('caches/drivers/')):
        shutil.rmtree(core.path.frozen_path(f'caches/drivers/{fi}'))
        print(f'已清理 driver: {fi}')
