import os


def abspath(path):
    return os.path.join(os.path.split(os.path.realpath(__file__))[0], path)
