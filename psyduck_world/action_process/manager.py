import action_process.login.login_process
import action_process.validate.validate_process


def init():
    pass


# api
def update():
    action_process.login.login_process.update()
    action_process.validate.validate_process.update()


def stop():
    action_process.login.login_process.stop()
    action_process.validate.validate_process.stop()
