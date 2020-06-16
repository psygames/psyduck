import core.helper
import core.path
from datetime import datetime
from core import db
from core import file_helper


class DownloadProcedure:
    act = {}
    over = False
    csdn = ''
    url = ''
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, act):
        self.act = act
        self.url = act['message']['url']
        self.csdn = act['message']['csdn']
        self.helper = core.helper.Helper()
        self.current_func = self.process_start

    def process_start(self):
        print('下载初始化...')
        _des_option = f'_tmp_option_download_{self.csdn}'
        if not file_helper.has_option(self.csdn):
            self.fail(f'option not exist')
            return
        res = file_helper.copy_option(self.csdn, _des_option)
        if not res:
            self.fail(f'option error')
            return
        res = self.helper.init(_des_option)
        if not res:
            self.fail(f'option error')
            return
        self.current_func = self.goto_validate

    def stop(self):
        self._over()

    def _over(self):
        self.over = True
        self.current_func = None
        if self.helper is not None:
            self.helper.dispose()

    def set_state(self, state, message, result):
        db.act_set(self.act['id'], state, message, result)
        self.act['state'] = state
        self.act['message'] = message
        self.act['result'] = result

    def update(self):
        self.check_timeout()
        if self.current_func is not None:
            self.current_func()

    def check_timeout(self):
        if (datetime.now() - self.act['time']).seconds >= 3600:
            print('下载超时')
            self.set_state('fail', self.act['message'], 'timeout')
            self._over()

    def goto_validate(self):
        print('开始验证登陆状态')
        is_login = self.helper.check_login()
        if is_login:
            self.goto_download()
        else:
            self.expired()

    def goto_download(self):

        def _download_callback(step, size=None):
            print(f'{step}: {size}')

        res = self.helper.download(self.url, _download_callback)
        print(res)

    def expired(self):
        print(f'验证登陆状态（失效）: {self.csdn}')
        self._over()
        self.set_state('done', self.act['message'], 'expired')
        db.user_set_state(self.act['uid'], self.csdn, 'expired')

    def fail(self, msg):
        print(f'下载发生错误（{msg}）: {self.csdn}')
        self._over()
        self.set_state('fail', self.act['message'], msg)

    def done(self):
        print(f'下载完成: {self.csdn}')
        self._over()
        self.set_state('done', self.act['message'], 'on')
        db.user_set_state(self.act['uid'], self.csdn, 'on')
