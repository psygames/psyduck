from action_process.login import login_process
from action_process.validate import validate_process
from action_process.update import update_process


def init():
    pass


# api
def update():
    login_process.update()
    validate_process.update()
    update_process.update()


def stop():
    login_process.stop()
    validate_process.stop()
    update_process.stop()
