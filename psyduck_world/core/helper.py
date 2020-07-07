import selenium.webdriver
import time
import platform
import os
from core import path
import shutil
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from core import file_helper
from datetime import datetime


class HelperResult:
    success = False
    result = None
    is_exception = False
    hint = False

    def __init__(self, success: bool, result, is_exception: bool):
        self.success = success
        self.result = result
        self.is_exception = is_exception

        if not success:
            if is_exception:
                print(f'{result} (exception)')
            else:
                print(f'{result}')


class Helper:
    driver = None
    is_driver_busy = False
    is_disposed = False
    zip_save_path = path.frozen_path('caches/zips')
    download_path = path.frozen_path('caches/downloads')
    drivers_path = path.frozen_path('caches/drivers')
    options_path = path.frozen_path('caches/options')
    option_name = ''
    tmp_driver_dir = ''
    tmp_option_path = ''

    def init(self, _option_name='', mobile_mode=True) -> HelperResult:
        try:
            if file_helper.is_lock_option(_option_name):
                print(f'初始化 Helper 失败, option 已被锁定 {_option_name}')
                return self._fail_result('option 已被锁定')
            file_helper.lock_option(_option_name)
            self.is_driver_busy = True
            self.is_disposed = False
            self.__get_tmp_driver()
            self.option_name = _option_name
            self.tmp_option_path = os.path.join(self.options_path, _option_name)
            _driver_path = os.path.join(self.tmp_driver_dir, 'chromedriver')
            self.download_path = os.path.join(self.download_path, datetime.now().strftime('%Y%m%d%H%M%S%f'))
            self.download_path = self.download_path.replace('\\', '/')
            if platform.system() == 'Windows':
                self.download_path = self.download_path.replace('/', '\\')
                _driver_path += ".exe"
            if not os.path.exists(_driver_path):
                print(f'chromedriver not found {_driver_path}')
                return self._fail_result('chromedriver not found.')

            options = selenium.webdriver.ChromeOptions()
            options.add_argument("user-data-dir=" + self.tmp_option_path)
            options.add_argument('--mute-audio')
            options.add_argument('--disable-gpu')
            options.add_argument("--log-level=3")
            if mobile_mode:
                mobile_emulation = {"deviceName": "Nexus 7"}
                options.add_experimental_option("mobileEmulation", mobile_emulation)

            prefs = {
                "disable-popup-blocking": False,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "download.default_directory": self.download_path,
                "profile.default_content_settings.popups": 0,
                'profile.default_content_setting_values': {'notifications': 2},
            }

            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)

            cap = DesiredCapabilities.CHROME
            cap["pageLoadStrategy"] = "none"

            os.chmod(_driver_path, 0o777)
            self.driver = selenium.webdriver.Chrome(options=options, executable_path=_driver_path,
                                                    desired_capabilities=cap)
            self.driver.set_window_size(500, 800)
            self.reset_timeout()
            return self._success_result()
        except:
            return self._except_result()

    def __get_tmp_driver(self):
        import datetime
        _name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        self.tmp_driver_dir = path.frozen_path(f'caches/drivers/{_name}')
        shutil.copytree(path.frozen_path('driver'), self.tmp_driver_dir)

    def reset_timeout(self):
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)

    def scroll_to(self, horizontal, vertical):
        js = f"window.scrollTo({horizontal},{vertical})"
        self.driver.execute_script(js)

    def get(self, url, timeout=10, retry=5):
        self.driver.get(url)
        time.sleep(1)
        time_counter = 0
        retry_counter = 0
        while retry_counter < retry:
            while time_counter < timeout:
                result = self.driver.execute_script("return document.readyState")
                if result == 'complete':
                    return
                if result == 'interactive':
                    time.sleep(3)
                    return
                time_counter += 1
                time.sleep(1)
            retry_counter += 1
            print('timeout retry %d -> %s' % (retry_counter, url))
        raise Exception('timeout retry %d all failed -> %s' % (retry, url))

    def find(self, xpath):
        import selenium.common.exceptions
        try:
            el = self.driver.find_element_by_xpath(xpath)
        except selenium.common.exceptions.NoSuchElementException:
            return None
        return el

    def find_all(self, xpath):
        return self.driver.find_elements_by_xpath(xpath)

    def find_count(self, xpath):
        return len(self.find_all(xpath))

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def dispose(self, rm_option=True, close_delay=0.1):
        print(f'销毁浏览器（清空Option: {rm_option}）')
        self.is_disposed = True
        if self.driver is not None:
            time.sleep(close_delay)
            self.driver.close()
            time.sleep(close_delay)
            self.driver.quit()
            time.sleep(close_delay)
            self.driver = None
        if self.is_driver_busy:
            file_helper.unlock_option(self.option_name)
        self.is_driver_busy = False
        if os.path.exists(self.tmp_driver_dir):
            time.sleep(0.1)
            shutil.rmtree(self.tmp_driver_dir)
        if rm_option and os.path.exists(self.tmp_option_path):
            time.sleep(0.1)
            shutil.rmtree(self.tmp_option_path)

    def is_busy(self):
        return self.is_driver_busy

    def _result(self, success, result, is_exception) -> HelperResult:
        return HelperResult(success, result, is_exception)

    def _success_result(self, result=None):
        return self._result(True, result, False)

    def _fail_result(self, result=None):
        return self._result(False, result, False)

    def _except_result(self):
        import traceback
        traceback.print_exc()
        return self._result(False, traceback.format_exc(), True)

    def get_scan_qr(self) -> HelperResult:
        try:
            self.get('https://passport.csdn.net/login')
            self.driver.switch_to.frame('iframe_id')
            qr = self.find('//img[@class="qrcode lightBorder"]')
            src = qr.get_attribute('src')
            self.driver.switch_to.default_content()
            return self._success_result(src)
        except:
            return self._except_result()

    def get_verify_code(self, phone) -> HelperResult:
        try:
            _input = self.find('//input[@id="phone"]')
            _input.clear()
            _input.send_keys(phone)
            btn = self.find('//button[@class="btn btn-confirm btn-control"]')
            btn.click()
            time.sleep(2)
            err = self.find('//div[@id="js_err_dom"]')
            is_err = err is not None and err.get_attribute('class') == 'col-xs-12 col-sm-12 col-pl-no text-error'
            if is_err:
                err_info = err.text.strip()
                res = self._success_result(err_info)
                res.hint = True
                return res

            sent = self.find('//button[@class="btn btn-confirm btn-control"]')
            if sent.text.strip().endswith('s'):
                return self._success_result()

            return self._fail_result('get_verify_code unknown error')
        except:
            return self._except_result()

    def set_verify_code(self, code) -> HelperResult:
        try:
            _input = self.find('//input[@id="code"]')
            _input.clear()
            _input.send_keys(code)
            btn = self.find('//button[@data-type="accountSecur"]')
            btn.click()
            time.sleep(2)
            err = self.find('//div[@id="js_err_dom"]')
            is_err = err is not None and err.get_attribute('class') == 'col-xs-12 col-sm-12 col-pl-no text-error'
            if is_err:
                err_info = err.text.strip()
                res = self._success_result(err_info)
                res.hint = True
                return res

            # 系统检测到 xxx 疑似被盗，请尽快修改密码
            a = self.find('//a[text()="以后再说"]')
            if a is not None:
                a.click()
                time.sleep(2)
                if self.driver.current_url.startswith('https://passport.csdn.net/sign'):
                    return self._fail_result('set_verify_code unknown error')

            return self._success_result()
        except:
            return self._except_result()

    def is_login_wait_for_verify(self) -> HelperResult:
        try:
            _res = self.driver.current_url.startswith('https://passport.csdn.net/sign')
            return self._success_result(_res)
        except:
            return self._except_result()

    def is_login_wait_for_qr_scan(self) -> HelperResult:
        try:
            _res = self.driver.current_url.startswith('https://passport.csdn.net/login')
            return self._success_result(_res)
        except:
            return self._except_result()

    def is_login_success(self) -> HelperResult:
        try:
            _url = self.driver.current_url
            _res = _url.startswith('https://i.csdn.net/#/uc/profile') or _url.startswith('https://www.csdn.net/')
            return self._success_result(_res)
        except:
            return self._except_result()

    def get_username(self) -> HelperResult:
        try:
            self.get('https://i.csdn.net/#/uc/profile')
            username = self.find('//span[@class="id_name"]').text[3:]
            return self._success_result(username)
        except:
            return self._except_result()

    def check_login(self) -> HelperResult:
        try:
            self.get("https://i.csdn.net/#/uc/profile")
            _res = self.driver.current_url.find('https://i.csdn.net/#/uc/profile') != -1
            return self._success_result(_res)
        except:
            return self._except_result()

    def get_user_info(self) -> HelperResult:
        try:
            info = {}
            self.get('https://my.csdn.net/')
            info['nickname'] = self.find('//h3[@class="person_nick_name"]').text
            info['point'] = int(self.find('//div[@class="own_t_l fl"]/label/em').text)
            info['coin'] = int(self.find('//label[@class="own_t_l_lab"]/em').text)
            info['head'] = self.find('//img[@alt="img"]').get_attribute('src')
            self.get('https://mp.csdn.net/console/vipService')
            time.sleep(3)  # 异步加载的界面，等一会
            vip = {}
            vip_title_tag = self.find('//h3[@class="server--status-title"]')
            vip_title = ''
            if vip_title_tag is not None:
                vip_title = vip_title_tag.text
            if vip_title == '当前 vip 情况':
                vip['is_vip'] = True
                vip['count'] = int(self.find('//li[@class="vipserver-count"]/span').text)
                vip['date'] = datetime.strptime(self.find('//li[@class="vipserver-time"]').text[8:], '%Y-%m-%d')
            else:
                vip['is_vip'] = False
                vip['count'] = 0
                vip['date'] = datetime(1970, 1, 1)
            info['vip'] = vip
            return self._success_result(info)
        except:
            return self._except_result()

    def logout(self) -> HelperResult:
        try:
            self.get('https://passport.csdn.net/account/logout')
            return self._success_result()
        except:
            return self._except_result()

    def get_download_info(self, url) -> HelperResult:
        try:
            if self.driver.current_url != url:
                self.get(url)
            title = self.find('//div[@class="resource_title"]').text
            desc = self.find('//div[@class="resource_description"]/p').text
            stars = 0
            for i in range(1, 6):
                if self.find(f'//span[@class="starts"]/i[{i}]').get_attribute('class') == 'fa fa-star':
                    stars = i - 1
                    break
            point = int(self.find('//div[@class="resource_msg"]/span[1]').text.strip()[:-1])
            _type = self.find('//div[@class="resource_msg"]/span[2]').text.strip()
            size = self.find('//div[@class="resource_msg"]/span[3]').text.strip()
            _str_time = self.find('//div[@class="resource_msg"]/span[4]').text.strip()
            upload_time = datetime.strptime(_str_time, '%Y-%m-%d')
            uploader = self.find('//div[@class="user_name"]/a').text
            return self._success_result({'url': url, 'title': title, 'description': desc, 'type': _type, 'size': size,
                                         'star': stars, 'point': point, 'upload_time': upload_time,
                                         'uploader': uploader})
        except:
            return self._except_result()

    def download(self, url, callback) -> HelperResult:
        try:
            step = 'begin download'
            callback(step)

            step = 'url cut #'
            callback(step)
            if url.find('#') != -1:
                url = url[0:url.index('#')]

            step = 'valid url'
            callback(step)
            if not self.__valid_download_url(url):
                return self._fail_result("无效的下载地址")

            step = 'get id'
            callback(step)
            _id = url[url.rfind('/') + 1:]

            step = 'goto url'
            callback(step)
            self.get(url)

            step = 'find btn'
            callback(step)
            btn = self.find('//a[@class="btn-block-link btn-border-red do_download"]')
            if btn is None:
                return self._fail_result("该资源没有下载通道")

            step = 'get info'
            callback(step)
            res = self.get_download_info(url)
            if not res.success:
                return self._except_result()

            info = res.result
            info['id'] = _id

            step = 'clear download dir'
            callback(step)
            self.__clear_download_dir()

            step = 'click download button'
            callback(step)
            btn.click()

            step = 'check redirect'
            callback(step)
            time.sleep(1)
            if self.driver.current_url != url:
                return self._fail_result('redirect')
            step = 'check block'
            callback(step)
            time.sleep(0.1)
            block = self.find('//div[@id="st_toastBox"]').get_attribute('style').find('block') != -1
            block = block or self.find('//div[@id="st_toastBox"]').get_attribute('style').find('z-index') != -1
            if block:
                info = self.find('//span[@id="st_toastContent"]').text
                return self._fail_result(info)

            step = 'get size'
            callback(step)
            size_str = self.find('//div[@class="resource_msg"]/span[3]')
            if size_str is None:
                return self._fail_result('get size fail')
            size_str = size_str.text
            _size = 0
            if size_str.endswith('KB'):
                _size = float(size_str[:-2]) * 1024
            elif size_str.endswith('MB'):
                _size = float(size_str[:-2]) * 1024 * 1024
            elif size_str.endswith('GB'):
                _size = float(size_str[:-2]) * 1024 * 1024 * 1024
            elif size_str.endswith('B'):
                _size = float(size_str[:-1])

            step = 'downloading'
            self.__wait_for_download(step, int(_size), callback)

            step = 'zip file'
            callback(step)
            self.__zip_file(_id)

            step = 'extend info'
            callback(step)
            info['filename'] = os.path.basename(self.__get_tmp_download_file())

            step = 'remove download dir'
            callback(step)
            self.__remove_download_dir()

            step = 'finish'
            callback(step)
            return self._success_result(info)
        except:
            return self._except_result()

    def __valid_download_url(self, url: str):
        if url.find('download.csdn.net/download/') != -1:
            return True
        return False

    def __remove_download_dir(self):
        if not os.path.exists(self.download_path):
            return
        shutil.rmtree(self.download_path)

    def __clear_download_dir(self):
        self.__remove_download_dir()
        os.mkdir(self.download_path)

    def __get_tmp_download_file(self):
        files = os.listdir(self.download_path)
        if len(files) <= 0:
            raise Exception('下载文件不存在！')
        elif len(files) > 1:
            raise Exception('下载目录存在多余文件！')
        return os.path.join(self.download_path, files[0])

    def __wait_for_download(self, step, total_size, callback):
        _sleep_step = 0.5

        # wait for create file
        wait_time = 5
        while wait_time > 0 and len(os.listdir(self.download_path)) <= 0:
            callback(step, 0, total_size)
            wait_time -= _sleep_step
            time.sleep(_sleep_step)

        # wait for download
        wait_time = 20
        last_size = os.path.getsize(self.__get_tmp_download_file())
        while wait_time > 0 and self.__is_downloading():
            cur_size = os.path.getsize(self.__get_tmp_download_file())
            callback(step, cur_size, total_size)
            if cur_size == last_size:
                wait_time -= _sleep_step
            else:
                wait_time = 20
            time.sleep(_sleep_step)

        cur_size = os.path.getsize(self.__get_tmp_download_file())
        callback(step, cur_size, cur_size)

        if self.__is_downloading():
            raise Exception('文件下载失败，请重试！')

    def __is_downloading(self):
        fi = self.__get_tmp_download_file()
        return fi.endswith('.crdownload') or fi.endswith('.tmp')

    def __zip_file(self, _id):
        import zipfile
        zip_path = os.path.join(self.zip_save_path, "{0}.zip".format(_id))
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print('zip exist, then delete!')
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            file_path = self.__get_tmp_download_file()
            zipf.write(file_path, os.path.basename(file_path))
