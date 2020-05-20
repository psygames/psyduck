import threading
import time

name = "上传管理器"
log = False


def run():
    threading.Thread(name=name, target=main_loop).start()


def main_loop():
    loop = 0
    while True:
        loop += 1
        if log:
            print(f"{name} 轮询 {loop}")
        time.sleep(1)
        main()


def main():
    pass
