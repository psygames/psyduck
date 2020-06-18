import core.path
import os
import threading

name = "WebServer"
log = False


def run():
    threading.Thread(name=name, target=main).start()


def stop():
    threading.current_thread().join()


def main():
    py = core.path.frozen_path('webserver/manage.py runserver 0.0.0.0:8000')
    os.system(f'python {py}')
