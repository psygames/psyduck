from datetime import datetime


def info(name, msg, desc):
    _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{_time} -> [{name}] {msg} ({desc})')
