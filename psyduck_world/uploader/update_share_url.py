import uploader.lanzou_tool as lzy
import core.db as db


def main():
    db.init()

    folder_lst = lzy.list_files("CSDN", False)
    i = 0
    n = len(folder_lst)
    for fd in folder_lst:
        i += 1
        name = fd.name
        _id = name[:-4]
        url = lzy.get_share_url(fd.id, False)
        ok = db.download_set_share_url(_id, url)
        if ok:
            print(f"修复成功[{i}/{n}]：{name} => {url}")
        else:
            print(f"修复失败[{i}/{n}]：{name} => {url}")

    file_list = lzy.list_files("CSDN", True)
    i = 0
    n = len(file_list)
    for fi in file_list:
        i += 1
        name = fi.name
        _id = name[:-4]
        url = lzy.get_share_url(fi.id, True)
        ok = db.download_set_share_url(_id, url)
        if ok:
            print(f"修复成功[{i}/{n}]：{name} => {url}")
        else:
            print(f"修复失败[{i}/{n}]：{name} => {url}")


if __name__ == '__main__':
    main()
