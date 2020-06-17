import core.helper
import core.path
from datetime import datetime
from core import db
from core import file_helper
from uploader import upload


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
        self.goto_validate()

    def stop(self):
        self._over()

    def _over(self):
        self.over = True
        self.current_func = None
        if self.helper is not None:
            self.helper.dispose()

    def set_state(self, state, result):
        db.act_set(self.act['id'], state, self.act['message'], result)
        self.act['state'] = state
        self.act['result'] = result

    def update(self):
        pass

    def goto_validate(self):
        print('开始验证登陆状态')
        is_login = self.helper.check_login()
        if is_login:
            self.goto_download()
        else:
            self.fail('账户过期')

    def goto_download(self):

        def _download_callback(step, now_size=None, total_size=None):
            if step == 'downloading':
                p = {'now_size': now_size, 'total_size': total_size}
                self.set_state('download', p)
                print(p)
            else:
                self.set_state('download', step)

        res = self.helper.download(self.url, _download_callback)
        if res['success']:
            self.goto_upload()
        else:
            self.fail(res['message'])

    def goto_upload(self):
        self.set_state('upload', '')
        upload.upload()
        pass

    def fail(self, msg):
        print(f'下载发生错误（{msg}）: {self.csdn}')
        self._over()
        self.set_state('fail', msg)

    def done(self, url):
        print(f'下载完成: {self.csdn}')
        self._over()
        self.set_state('done', url)
