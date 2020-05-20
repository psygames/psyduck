from core import helper, db
import threading
import time

name = "下载管理器"
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
        # main()


def main():
    _id = 0
    try:
        helper.init()
        item = db.zero_get_one()
        _id = item['id']
        while item is not None:
            db.zero_set_state(_id, 1)  # downloading
            result = helper.auto_download(item['url'])
            if result['success']:
                db.zero_set_state(_id, 3)  # downloaded
                print(f'{_id} => {result}')
            elif result['exception']:
                db.zero_set_state(_id, 0)  # revert downloading
                print(f'{_id} => {result} {item["url"]}')
                break
            else:
                db.zero_set_state(_id, 2)  # download failed
                db.zero_set_info(_id, result['message'])
                print(f'{_id} => {result} {item["url"]}')

            item = db.zero_get_one()
            _id = item['id']
    except:
        if _id != 0:
            db.zero_set_state(_id, 0)  # revert downloading
    finally:
        helper.dispose()
