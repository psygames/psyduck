import core.helper
import core.path
from datetime import datetime
from core import db
from core import file_helper


class UpdateProcedure:
    act = {}
    over = False
    csdn = ''
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, act):
        self.act = act
        self.csdn = act['message']
        self.helper = core.helper.Helper()
        self.current_func = self.process_start

    def process_start(self):
        print('更新用户信息初始化...')
        _des_option = f'_tmp_option_validate_{self.csdn}'
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

    def set_state(self, state, result):
        db.act_set_state(self.act['id'], state, result)
        self.act['state'] = state
        self.act['result'] = result

    def update(self):
        self.check_timeout()
        if self.current_func is not None:
            self.current_func()

    def check_timeout(self):
        if (datetime.now() - self.act['time']).seconds >= 30:
            print('操作超时')
            self._over()
            self.set_state('fail', 'timeout')

    def goto_validate(self):
        print('运行浏览器操作')
        is_login = self.helper.check_login()
        if is_login:
            res = self.helper.get_user_info()
            if not res['success']:
                self.fail('获取用户信息失败')
            info = res['result']
            db.user_set_info(self.act['uid'], self.csdn, info)
            self.done()
        else:
            self.expired()

    def expired(self):
        print(f'账户状态（过期）: {self.csdn}')
        self._over()
        self.set_state('done', 'expired')
        db.user_set_state(self.act['uid'], self.csdn, 'expired')

    def fail(self, msg):
        print(f'更新用户信息时发生错误（{msg}）: {self.csdn}')
        self._over()
        self.set_state('fail', msg)

    def done(self):
        print(f'账户状态（有效）: {self.csdn}')
        self._over()
        self.set_state('done', 'on')
        db.user_set_state(self.act['uid'], self.csdn, 'on')
