from action_process.login import login_process
from action_process.download import download_process
from action_process.update import update_process


def init():
    pass


# api
def update():
    login_process.update()
    download_process.update()
    update_process.update()


def stop():
    login_process.stop()
    download_process.stop()
    update_process.stop()
