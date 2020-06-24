import core.helper
from datetime import datetime
from core import db
import core.path
from core import file_helper


class LoginProcedure:
    act = {}
    over = False
    helper: core.helper.Helper = None
    current_func = None

    def __init__(self, act):
        self.act = act
        self.helper = core.helper.Helper()
        self.current_func = self.process_start

    def stop(self):
        self._over()

    def _over(self, rm_option=True):
        self.over = True
        self.current_func = None
        if not self.helper.is_disposed:
            if not rm_option:
                self.helper.dispose(rm_option, 2)
            else:
                self.helper.dispose(rm_option)

    def set_state(self, state, result):
        db.act_set_state(self.act['id'], state, result)
        self.act['state'] = state
        self.act['result'] = result

    def update(self):
        self.check_timeout()
        if self.current_func is not None:
            self.current_func()

    def check_timeout(self):
        if (datetime.now() - self.act['time']).seconds >= 300:
            self._fail('timeout')
            print('登录超时')

    def process_start(self):
        print('登陆初始化...')
        res = self.helper.init(f'_tmp_option_login_{self.act["uid"]}', False)
        if not res.success:
            self._fail('初始化失败')
            return
        self.current_func = self.goto_login

    def goto_login(self):
        print('获取二维码')
        res = self.helper.get_scan_qr()
        if not res.success:
            self._fail('取登陆二维码失败')
            return
        self.set_state('scan', res.result)
        print('等待扫码')
        self.current_func = self.wait_scan

    def wait_scan(self):
        res = self.helper.is_login_wait_for_qr_scan()
        if not res.success:
            self._fail('check is_login_wait_for_qr_scan fail')
            return
        if not res.result:
            self.current_func = self.scan_next
            print('扫码完成')

    def scan_next(self):
        if self.helper.is_login_wait_for_verify():
            self.set_state('verify_get', self.act['result'])
            self.current_func = self.wait_verify
            print('等待验证')
        elif self.helper.is_login_success():
            self.current_func = self._done
            print('登录完成')

    def wait_verify(self):
        res = self.helper.is_login_wait_for_verify()
        if not res.success:
            self._fail('check is_login_wait_for_verify fail')
            return
        if not res.result:
            self.current_func = self.verify_next
            print('验证完成')

    def get_verify_code(self, phone):
        res = self.helper.is_login_wait_for_verify()
        if not res.success:
            self._fail('check is_login_wait_for_verify fail')
            return
        if not res.result:
            return

        res = self.helper.get_verify_code(phone)
        if not res.success:
            self._fail('get_verify_code fail')
            return

        if res.hint:
            self.set_state('verify_get_hint', res.result)
        else:
            self.set_state('verify_set', self.act['result'])

    def set_verify_code(self, code):
        res = self.helper.is_login_wait_for_verify()
        if not res.success:
            self._fail('check is_login_wait_for_verify fail')
            return
        if not res.result:
            return

        res = self.helper.set_verify_code(code)
        if not res.success:
            self._fail('set_verify_code fail')
            return

        if res.hint:
            self.set_state('verify_set_hint', res.result)
        else:
            self.set_state('wait_for_done', self.act['result'])

    def verify_next(self):
        res = self.helper.is_login_success()
        if not res.success:
            self._fail('check is_login_success fail')
            return
        if res.result:
            self.current_func = self._done

    def _fail(self, message):
        print(f'登录失败：{message}')
        self.set_state('fail', message)
        self._over()

    def _done(self):
        res = self.helper.get_username()
        if not res.success:
            self._fail('获取 CSDN 用户名')
            print('获取 CSDN 用户名失败: ' + self.act['uid'])
            return
        csdn = res.result

        res2 = self.helper.get_user_info()
        if not res2.success:
            self._fail('获取 CSDN 用户信息失败')
            print('获取 CSDN 用户信息失败: ' + self.act['uid'])
            return
        info = res2.result

        self._over(False)
        file_helper.move_option(self.helper.option_name, csdn)
        print('登录完成: ' + csdn)
        self.set_state('done', info)
        db.user_set_state(self.act['uid'], csdn, 'on')
        db.user_set_info(self.act['uid'], csdn, info)
