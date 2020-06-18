import core.db
from action_process.download import download_procedure

procedures = []


def process_request():
    act = core.db.act_get('download', 'request')
    if act is None:
        return
    core.db.act_set_state(act['id'], 'process', act['result'])
    procedures.append(download_procedure.DownloadProcedure(act))


def procedure_update():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    process_request()
    procedure_update()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
