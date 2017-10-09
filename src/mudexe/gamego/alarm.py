from ..mud.exceptions import Crapup


def occur(user, active=False):
    if not active:
        return
    user.next_turn()


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
