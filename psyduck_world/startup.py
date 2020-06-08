from initialize import initialize
import action_process.startup
import downloader.startup
import uploader.startup
import time
import webserver.startup


def test():
    # test options
    from core import helper
    helper = helper.Helper()
    helper.init(f'y85171642')
    print(f"重复验证登陆Option有效性 : {helper.check_login()}")
    helper.dispose(False)


def main():
    result = initialize.init()
    if not result:
        print("初始化失败！")
    action_process.startup.run()
    # webserver.startup.run()
    # downloader.startup.run()
    # uploader.startup.run()
    print('启动完成！')
    loop = 0
    while True:
        loop += 1
        # print(f"主线程 轮询 {loop}")
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        action_process.startup.stop()
