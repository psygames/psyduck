procedures = []


# login
def login_procedure_update():
    for p in procedures:
        if p.over:
            procedures.remove(p)
            continue
        p.update()


def update():
    login_procedure_update()


def stop():
    for p in procedures:
        p.stop()
    procedures.clear()
