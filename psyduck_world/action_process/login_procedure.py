import core.helper
from datetime import datetime
import core.path
from core import file_helper


class LoginProcedure:
    uid = ''
    state = ''
    result = ''
    time = None
    over = False
    busy = False
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, uid):
        self.uid = uid
        self.helper = core.helper.Helper()
        self.current_func = self.process_start

    def process_start(self):
        print('登陆初始化...')
        self.busy = True
        self.time = datetime.now()
        res = self.helper.init(f'_tmp_option_login_{self.uid}')
        if not res:
            return
        self.current_func = self.goto_login

    def stop(self):
        self._over()

    def _over(self, rm_option=True):
        self.over = True
        self.current_func = None
        self.busy = False
        if self.helper is not None:
            self.helper.dispose(rm_option)

    def set_state(self, state, result):
        self.state = state
        self.result = result

    def update(self):
        self.check_timeout()
        if self.current_func is not None:
            self.current_func()

    def check_timeout(self):
        if (datetime.now() - self.time).seconds >= 120:
            self.set_state('fail', 'timeout')
            self._over()
            print('登录超时')

    def goto_login(self):
        print('获取二维码')
        qr = self.helper.get_scan_qr()
        if qr is None or qr == '':
            self.set_state('fail',  'get qrcode fail')
            self._over()
            print('获取登陆二维码失败')
            return
        self.set_state('scan', qr)
        print('等待扫码')
        self.current_func = self.wait_scan

    def wait_scan(self):
        if not self.helper.is_login_wait_for_qr_scan():
            self.current_func = self.scan_next
            print('扫码完成')

    def scan_next(self):
        if self.helper.is_login_wait_for_verify():
            self.set_state('verify', self.result)
            self.current_func = self.wait_verify
            print('等待验证')
        elif self.helper.is_login_success():
            self.current_func = self.done
            print('登录完成')

    def wait_verify(self):
        if not self.helper.is_login_wait_for_verify():
            self.current_func = self.verify_next
            print('验证完成')

    def get_verify_code(self, phone):
        if not self.helper.is_login_wait_for_verify():
            return
        self.helper.get_verify_code(phone)

    def set_verify_code(self, code):
        if not self.helper.is_login_wait_for_verify():
            return
        self.helper.set_verify_code(code)

    def verify_next(self):
        if self.helper.is_login_success():
            self.current_func = self.done

    def done(self):
        csdn = self.helper.get_username()
        if csdn is None or csdn == '':
            self.set_state('fail', 'get csdn user info fail')
            self._over()
            print('获取 CSDN 用户信息失败: ' + self.uid)
            return
        self.set_state('done', self.result)
        self._over(False)
        file_helper.move_option(self.helper.option_name, csdn)
        print('登录完成: ' + csdn)
