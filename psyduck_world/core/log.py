import datetime


def info(name, _str):
    _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{_time} > [{name}] {_str}')
