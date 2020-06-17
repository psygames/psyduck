from selenium import webdriver
import time
import platform
import os
from core import path
import shutil
from core import file_helper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:
    # dirs
    zips_path = path.frozen_path('caches/zips')
    downloads_path = path.frozen_path('caches/downloads')
    drivers_path = path.frozen_path('caches/drivers')
    options_path = path.frozen_path('caches/options')
    origin_driver_dir = path.frozen_path('driver')

    # fields
    driver = None
    is_driver_busy = False
    mobile_mode = False

    option_name = ''

    tmp_driver_dir = ''
    tmp_driver_path = ''
    tmp_option_path = ''

    def init(self, option_name='', mobile_mode=True):
        self.is_driver_busy = True
        self.option_name = option_name
        self.mobile_mode = mobile_mode

        self.make_tmp_driver()
        self.make_tmp_option()
        self.set_driver()

    def make_tmp_driver(self):
        import datetime
        _name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        _tmp_driver_dir = path.frozen_path(f'caches/drivers/{_name}')
        os.mkdir(_tmp_driver_dir)
        _driver_name = self.get_driver_name()
        _origin_driver_path = os.path.join(self.origin_driver_dir, _driver_name)
        self.tmp_driver_path = os.path.join(_tmp_driver_dir, _driver_name)
        shutil.copy(_origin_driver_path, _tmp_driver_dir)

    def make_tmp_option(self):
        import datetime
        _special_option_name = self.get_option_prefix() + self.option_name
        self.tmp_option_path = os.path.join(self.options_path, _special_option_name)
        if os.path.exists(self.tmp_option_path):
            _suffix = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            _tmp_path = os.path.join(self.options_path, f'{_special_option_name}_{_suffix}')
            shutil.copytree(self.tmp_option_path, _tmp_path)
            self.tmp_option_path = _tmp_path

    def get_driver_name(self) -> str:
        return ''

    def get_option_prefix(self) -> str:
        return ''

    def set_driver(self):
        pass

    def goto(self, url):
        self.driver.get(url)

    def scroll_to(self, horizontal, vertical):
        js = f"window.scrollTo({horizontal},{vertical})"
        self.driver.execute_script(js)


class Firefox(Browser):
    def set_driver(self):
        from selenium.webdriver.firefox.options import Options
        # option
        options = Options()
        options.add_argument("-profile")
        options.add_argument(self.tmp_option_path)

        # profile
        profile = webdriver.FirefoxProfile(self.tmp_option_path)
        profile.set_preference('browser.download.dir', self.downloads_path)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-msdownload");

        self.driver = webdriver.Firefox(options=options, executable_path=self.tmp_driver_path, firefox_profile=profile)
        print(self.driver)

    def get_driver_name(self) -> str:
        return 'geckodriver.exe'


class Chrome(Browser):
    def set_driver(self):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("user-data-dir=" + self.tmp_option_path)  # 自定义Option

        self.downloads_path = self.downloads_path.replace('/', '\\')
        prefs = {
            "download.default_directory": self.downloads_path,
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options, executable_path=self.tmp_driver_path, )
        print(self.driver)

    def get_driver_name(self) -> str:
        return 'chromedriver.exe'


def test():
    b = Chrome()
    b.init('y85171642')
    b.goto('http://www.baidu.com')


if __name__ == '__main__':
    test()
