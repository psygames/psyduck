import core.helper
import core.path
from datetime import datetime
from core import db
import os
import shutil
from core import file_helper


class ValidateProcedure:
    act = {}
    over = False
    csdn = 'null'
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, act):
        self.act = act
        self.csdn = act['message']
        self.helper = core.helper.Helper()
        self.current_func = self.process_start

    def process_start(self):
        print('验证登陆初始化...')
        _des_option = f'_tmp_option_validate_{self.csdn}'
        res = file_helper.copy_option(self.csdn, _des_option)
        if not res:
            return
        res = self.helper.init(_des_option)
        if not res:
            return
        self.current_func = self.goto_validate

    def stop(self):
        self._over()

    def _over(self):
        self.over = True
        self.current_func = None
        if self.helper is not None:
            self.helper.dispose()

    def set_state(self, state, message='', file=''):
        if self.act['id'] != 'fake_validate':
            db.act_set(self.act['id'], state, message, file)
        self.act['state'] = state
        self.act['message'] = message
        self.act['file'] = file

    def update(self):
        self.check_timeout()
        if self.current_func is not None:
            self.current_func()

    def check_timeout(self):
        if (datetime.now() - self.act['time']).seconds >= 30:
            self.set_state('fail', 'timeout')
            self._over()
            print('验证超时')

    def goto_validate(self):
        print('开始验证登陆状态')
        is_login = self.helper.check_login()
        if is_login:
            self.done()
        else:
            self.expired()

    def expired(self):
        self._over()
        self.set_state('done', 'expired')
        db.user_set_state(self.act['uid'], self.csdn, 'expired')
        print(f'验证登陆状态（失效）: {self.csdn}')

    def fail(self, msg):
        self._over()
        self.set_state('fail', msg)
        print(f'验证登陆状态发生错误（{msg}）: {self.csdn}')

    def done(self):
        self._over()
        self.set_state('done', 'on')
        db.user_set_state(self.act['uid'], self.csdn, 'on')
        print(f'验证登陆状态（有效）: {self.csdn}')
