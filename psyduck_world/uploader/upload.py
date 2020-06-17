from uploader.uploader import Uploader

settings = {
    'name': 'admin',
    'set_share_url': True,
    'update_share_url': False,
    'cookies': {
        'ylogin': '1104264',
        'phpdisk_info': 'UmcDMFEzUmpVZVM1WjRaCVMyDD0PXwFnDzQHYQI0VGZZbF9tVzAGPlJoA2ABUgdoW2pVNgpkUDIPNAg5BzIHMFI3A2NRYVJnVWFTNlo0WjdTMAw8D2ABMw9uBzECNVRkWW9fZFdgBjpSaQMxAW4HVFs6VW8KZVA3DzwIaQcxBzBSYgM5UTA%3D'
    }
}


def upload(file_path, uploading_callback, uploaded_callback):
    up = Uploader(settings)
    up.login()
    up.upload_file(file_path, uploading_callback, uploaded_callback)
