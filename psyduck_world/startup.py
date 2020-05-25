from initialize import initialize
import action_process.startup
import downloader.startup
import uploader.startup
import time


def main():
    result = initialize.init()
    if not result:
        print("初始化失败！")
    action_process.startup.run()
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
        action_process.startup.stop()
