from ..mud.exceptions import Crapup


interrupt = False


def occur(user, active=False):
    global interrupt
    if not active:
        return
    interrupt = True
    user.next_turn()
    interrupt = False


def ctrlc(user, active=False):
    print("^C")
    if user.in_fight:
        return
    user.loseme()
    try:
        raise Crapup("Byeeeeeeeeee  ...........", terminal=user.terminal)
    except Crapup as e:
        print(e)
        exit(0)


def oops(user, active=False):
    user.loseme()
    exit(255)
