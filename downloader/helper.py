import selenium.webdriver
import time
import platform
import os
import config
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver: selenium.webdriver.Chrome = None

is_driver_busy = False

zip_save_path = config.zip_save_path
download_path = config.chrome_download_path
driver_path = config.chrome_driver_path
option_path = config.chrome_option_path


def create_dir():
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    if not os.path.exists(zip_save_path):
        os.mkdir(zip_save_path)


def init(_option_path=''):
    global is_driver_busy
    global driver
    is_driver_busy = True
    _driver_path = driver_path
    create_dir()
    if platform.system() == 'Windows':
        _driver_path += ".exe"
    if not os.path.exists(_driver_path):
        raise Exception('chromedriver not exist at {}'.format(_driver_path))

    if _option_path == '':
        _option_path = option_path

    options = selenium.webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + _option_path)
    options.add_argument('--mute-audio')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument("--user-agent=iphone x")

    prefs = {
        "disable-popup-blocking": False,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.default_directory": download_path,
        "profile.default_content_settings.popups": 0,
        'profile.default_content_setting_values': {'notifications': 2},
    }

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    cap = DesiredCapabilities.CHROME
    cap["pageLoadStrategy"] = "none"

    os.chmod(_driver_path, 0o777)
    driver = selenium.webdriver.Chrome(options=options, executable_path=_driver_path, desired_capabilities=cap)
    driver.set_window_size(500, 800)
    reset_timeout()


def reset_timeout():
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)


def is_busy():
    return is_driver_busy


def get(url, timeout=10, retry=3):
    driver.get(url)
    time.sleep(1)
    time_counter = 0
    retry_counter = 0
    while retry_counter < retry:
        while time_counter < timeout:
            result = driver.execute_script("return document.readyState")
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


def find(xpath):
    import selenium.common.exceptions
    try:
        el = driver.find_element_by_xpath(xpath)
    except selenium.common.exceptions.NoSuchElementException:
        return None
    return el


def find_all(xpath):
    return driver.find_elements_by_xpath(xpath)


def find_count(xpath):
    return len(find_all(xpath))


def set_window_size(width, height):
    driver.set_window_size(width, height)


def dispose():
    global driver
    global is_driver_busy
    if driver is not None:
        driver.stop_client()
        driver.quit()
        driver = None
    is_driver_busy = False


def check_login():
    get("https://i.csdn.net/#/uc/profile")
    if driver.current_url.find('https://i.csdn.net/#/uc/profile') != -1:
        return True
    return False


def logout():
    get('https://passport.csdn.net/account/logout')


def auto_login():
    while not check_login():
        print('自动登录...')
        if driver.current_url != 'https://passport.csdn.net/signwap':
            get('https://passport.csdn.net/signwap')

        input("请手动登录，并按任意键继续...")
        print('验证完成！尝试重新登录中...')
        continue


def auto_download(url):
    step = 'begin download'
    try:
        step = 'url cut #'
        if url.find('#') != -1:
            url = url[0:url.index('#')]

        step = 'valid url'
        if not __valid_download_url(url):
            return __download_result(False, "无效的下载地址")

        step = 'login'
        auto_login()

        step = 'get url'
        get(url)

        step = 'set id'
        _id = url[url.rfind('/') + 1:]

        step = 'find btn'
        btn = find('//a[@class="do_download btn-block-link btn-border-red"]')
        if btn is None:
            return __download_result(False, "该资源没有下载通道")

        step = 'clear download dir'
        __clear_download_dir()

        step = 'click download button'
        btn.click()

        step = 'check redirect'
        time.sleep(1)
        if driver.current_url != url:
            return __download_result(False, 'redirect')

        step = 'check block'
        time.sleep(0.1)
        block = find('//div[@id="st_toastBox"]').get_attribute('style').find('opacity:') != -1
        if block:
            info = find('//span[@id="st_toastContent"]').text
            return __download_result(False, info)

        step = 'wait for download'
        __wait_for_download()

        step = 'zip file'
        __zip_file(_id)

        step = 'save to db'
        __save_to_db(_id)

        step = 'finish'
        return __download_result(True, "success")
    except:
        import traceback
        traceback.print_exc()
        return __download_result(False, step, True)


def __valid_download_url(url):
    # 暂时屏蔽验证
    return True


def __clear_download_dir():
    for f in os.listdir(download_path):
        os.remove(os.path.join(download_path, f))


def __get_tmp_download_file():
    files = os.listdir(download_path)
    if len(files) <= 0:
        raise Exception('下载文件不存在！')
    elif len(files) > 1:
        raise Exception('下载目录存在多余文件！')
    return os.path.join(download_path, files[0])


def __wait_for_download():
    time.sleep(2)  # wait for create file
    wait_time = 20
    last_size = os.path.getsize(__get_tmp_download_file())
    while wait_time > 0 and __get_tmp_download_file().endswith('.crdownload'):
        cur_size = os.path.getsize(__get_tmp_download_file())
        if cur_size == last_size:
            wait_time -= 1
        else:
            wait_time = 20
        time.sleep(1)

    if __get_tmp_download_file().endswith('.crdownload'):
        raise Exception('文件下载失败，请重试！')


def __zip_file(_id):
    import zipfile
    zip_path = os.path.join(zip_save_path, "{0}.zip".format(_id))
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print('zip exist, then delete!')
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        file_path = __get_tmp_download_file()
        zipf.write(file_path, os.path.basename(file_path))


def __save_to_db(_id):
    import db
    if not db.zero_is_download(_id):
        db.zero_set_state(_id, 1)


def __download_result(success, message='', exception=False):
    return {'success': success, 'message': message, "exception": exception}
