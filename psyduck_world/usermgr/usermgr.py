from core import db
import core.helper
from datetime import datetime


class LoginProcedure:
    act = {}
    over = False
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, act):
        self.act = act
        self.current_func = self.process_start

    def force_stop(self):
        self._over()

    def _over(self):
        self.over = True
        if self.helper is not None:
            self.helper.dispose()

    def set_state(self, state, message='', file=''):
        db.act_set(self.act['id'], state, message, file)
        self.act['state'] = state

    def update(self):
        if self.check_timeout():
            return
        self.current_func()

    def check_timeout(self):
        if self.act['state'] == 'fail' and self.act['message'] == 'timeout':
            return True
        if self.act['state'] == 'done':
            return False
        if (datetime.now() - self.act['time']).seconds >= 120:
            self.set_state('fail', 'timeout')
            self._over()
            print('登录超时')
            return True
        return False

    def process_start(self):
        print('初始化...')
        self.helper = core.helper.Helper()
        self.helper.init(f'{self.act["uid"]}_tmp_option')
        self.current_func = self.goto_login

    def goto_login(self):
        print('获取二维码')
        qr = self.helper.get_scan_qr()
        self.set_state('scan', file=qr)
        print('等待扫码')
        self.current_func = self.wait_scan

    def wait_scan(self):
        if not self.helper.is_login_wait_for_qr_scan():
            self.current_func = self.scan_next
            print('扫码完成')

    def scan_next(self):
        if self.helper.is_login_wait_for_verify():
            self.set_state('verify')
            self.current_func = self.wait_verify
            print('等待验证')
        elif self.helper.is_login_success():
            self.current_func = self.done
            print('登录完成')

    def wait_verify(self):
        if not self.helper.is_login_wait_for_verify():
            self.current_func = self.verify_next
            print('验证完成')

    def verify_next(self):
        if self.helper.is_login_success():
            self.current_func = self.done
            print('登录完成')

    def done(self):
        self.set_state('done')
        username = self.helper.get_username()
        self.helper.save_tmp_option(username)
        self._over()
        db.user_set(username, 'online')
        self.current_func = None


def loop_check():
    login_check()
    login_process()


def stop_all():
    for p in login_procedure:
        p.force_stop()
    login_procedure.clear()


login_procedure = []


def login_check():
    act = db.act_get('user', 'login', 'request')
    if act is None:
        return
    db.act_set(act['id'], 'process')
    login_procedure.append(LoginProcedure(act))


def login_process():
    for p in login_procedure:
        p.update()
