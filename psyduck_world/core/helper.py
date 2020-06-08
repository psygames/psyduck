import selenium.webdriver
import time
import platform
import os
from core import path
import shutil
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from core import file_helper


class Helper:
    driver: selenium.webdriver.Chrome = None
    is_driver_busy = False
    zip_save_path = path.frozen_path('caches/zips')
    download_path = path.frozen_path('caches/downloads')
    drivers_path = path.frozen_path('caches/drivers')
    options_path = path.frozen_path('caches/options')
    option_name = ''
    tmp_driver_dir = ''
    tmp_option_path = ''

    def __get_tmp_driver(self):
        import datetime
        _name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        self.tmp_driver_dir = path.frozen_path(f'caches/drivers/{_name}')
        shutil.copytree(path.frozen_path('driver'), self.tmp_driver_dir)

    def init(self, _option_name='', mobile_mode=True):
        if file_helper.is_lock_option(_option_name):
            print(f'初始化 Helper 失败, option 已被锁定 {_option_name}')
            return False
        file_helper.lock_option(_option_name)
        self.is_driver_busy = True
        self.__get_tmp_driver()
        self.option_name = _option_name
        self.tmp_option_path = os.path.join(self.options_path, _option_name)
        _driver_path = os.path.join(self.tmp_driver_dir, 'chromedriver')
        if platform.system() == 'Windows':
            _driver_path += ".exe"
        if not os.path.exists(_driver_path):
            raise Exception('chromedriver not exist at {}'.format(_driver_path))

        options = selenium.webdriver.ChromeOptions()
        options.add_argument("user-data-dir=" + self.tmp_option_path)
        options.add_argument('--mute-audio')
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")
        if mobile_mode:
            options.add_argument("--user-agent=iphone x")

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
        self.driver = selenium.webdriver.Chrome(options=options, executable_path=_driver_path, desired_capabilities=cap)
        self.driver.set_window_size(500, 800)
        self.reset_timeout()
        return True

    def reset_timeout(self):
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)

    def scroll_to(self, horizontal, vertical):
        js = f"window.scrollTo({horizontal},{vertical})"
        self.driver.execute_script(js)

    def is_busy(self):
        return self.is_driver_busy

    def get_scan_qr(self):
        if self.driver is None:
            return ''
        self.get('https://passport.csdn.net/login')
        self.scroll_to(520, 0)
        self.driver.switch_to.frame('iframe_id')
        qr = self.find('//img[@class="qrcode lightBorder"]')
        if qr is None:
            return ''
        src = qr.get_attribute('src')
        self.driver.switch_to.default_content()
        return src

    def get_verify_code(self, phone):
        if self.driver is None:
            return
        _input = self.find('//input[@id="phone"]')
        _input.clear()
        _input.send_keys(phone)
        btn = self.find('//button[@class="btn btn-confirm btn-control"]')
        btn.click()

    def set_verify_code(self, code):
        if self.driver is None:
            return
        _input = self.find('//input[@id="code"]')
        _input.clear()
        _input.send_keys(code)
        btn = self.find('//button[@data-type="accountSecur"]')
        btn.click()
        time.sleep(1)
        a = self.find('//a[text()="以后再说"]')
        if a is not None:
            a.click()

    def is_login_wait_for_verify(self):
        if self.driver is None:
            return False
        return self.driver.current_url.startswith('https://passport.csdn.net/sign')

    def is_login_wait_for_qr_scan(self):
        if self.driver is None:
            return False
        return self.driver.current_url.startswith('https://passport.csdn.net/login')

    def is_login_success(self):
        if self.driver is None:
            return False
        return self.driver.current_url.startswith(
            'https://i.csdn.net/#/uc/profile') or self.driver.current_url.startswith('https://www.csdn.net/')

    def get_username(self):
        self.get('https://i.csdn.net/#/uc/profile')
        username = self.find('//span[@class="id_name"]').text[3:]
        return username

    def get(self, url, timeout=10, retry=3):
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

    def dispose(self, rm_option=True):
        if self.driver is not None:
            time.sleep(0.1)
            self.driver.close()
            time.sleep(1)
            self.driver.quit()
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

    def check_login(self):
        self.get("https://i.csdn.net/#/uc/profile")
        if self.driver.current_url.find('https://i.csdn.net/#/uc/profile') != -1:
            return True
        return False

    def logout(self):
        self.get('https://passport.csdn.net/account/logout')

    def auto_download(self, url):
        step = 'begin download'
        try:
            step = 'url cut #'
            if url.find('#') != -1:
                url = url[0:url.index('#')]

            step = 'valid url'
            if not self.__valid_download_url(url):
                return self.__download_result(False, "无效的下载地址")

            step = 'check login'
            if not self.check_login():
                pass

            step = 'get url'
            self.get(url)

            step = 'set id'
            _id = url[url.rfind('/') + 1:]

            step = 'find btn'
            btn = self.find('//a[@class="do_download btn-block-link btn-border-red"]')
            if btn is None:
                return self.__download_result(False, "该资源没有下载通道")

            step = 'clear download dir'
            self.__clear_download_dir()

            step = 'click download button'
            btn.click()

            step = 'check redirect'
            time.sleep(1)
            if self.driver.current_url != url:
                return self.__download_result(False, 'redirect')

            step = 'check block'
            time.sleep(0.1)
            block = self.find('//div[@id="st_toastBox"]').get_attribute('style').find('opacity:') != -1
            if block:
                info = self.find('//span[@id="st_toastContent"]').text
                return self.__download_result(False, info)

            step = 'wait for download'
            self.__wait_for_download()

            step = 'zip file'
            self.__zip_file(_id)

            step = 'save to db'
            self.__save_to_db(_id)

            step = 'finish'
            return self.__download_result(True, "success")
        except:
            import traceback
            traceback.print_exc()
            return self.__download_result(False, step, True)

    def __valid_download_url(self, url):
        # 暂时屏蔽验证
        return True

    def __clear_download_dir(self):
        for f in os.listdir(self.download_path):
            os.remove(os.path.join(self.download_path, f))

    def __get_tmp_download_file(self):
        files = os.listdir(self.download_path)
        if len(files) <= 0:
            raise Exception('下载文件不存在！')
        elif len(files) > 1:
            raise Exception('下载目录存在多余文件！')
        return os.path.join(self.download_path, files[0])

    def __wait_for_download(self):
        time.sleep(2)  # wait for create file
        wait_time = 20
        last_size = os.path.getsize(self.__get_tmp_download_file())
        while wait_time > 0 and self.__get_tmp_download_file().endswith('.crdownload'):
            cur_size = os.path.getsize(self.__get_tmp_download_file())
            if cur_size == last_size:
                wait_time -= 1
            else:
                wait_time = 20
            time.sleep(1)

        if self.__get_tmp_download_file().endswith('.crdownload'):
            raise Exception('文件下载失败，请重试！')

    def __zip_file(self, _id):
        import zipfile
        zip_path = os.path.join(self.zip_save_path, "{0}.zip".format(_id))
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print('zip exist, then delete!')
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            file_path = self.__get_tmp_download_file()
            zipf.write(file_path, os.path.basename(file_path))

    def __save_to_db(self, _id):
        pass

    def __download_result(self, success, message='', exception=False):
        return {'success': success, 'message': message, "exception": exception}
