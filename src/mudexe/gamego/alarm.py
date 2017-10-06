from . import crapup


interrupt = False


def occur(user, active=False):
    global interrupt
    if not active:
        return
    user.world.openworld()
    interrupt = True
    user.rte()
    interrupt = False
    # on_timing()
    user.world.closeworld()
    # key_reprint()


def ctrlc(user, active=False):
    print("^C")
    if user.in_fight:
        return
    user.loseme()
    crapup("Byeeeeeeeeee  ...........")


def oops(user, active=False):
    user.loseme()
    exit(255)
