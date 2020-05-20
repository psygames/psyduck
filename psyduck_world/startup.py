from initialize import initialize
import usermgr.startup
import downloader.startup
import uploader.startup
import time


def main():
    result = initialize.init()
    if not result:
        print("初始化失败！")
    usermgr.startup.run()
    # downloader.startup.run()
    # uploader.startup.run()

    loop = 0
    while True:
        loop += 1
        # print(f"主线程 轮询 {loop}")
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        usermgr.startup.stop()
