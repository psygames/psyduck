import core.db
import initialize.clear


def init():
    initialize.clear.clear_caches()
    core.db.init()
    return True

