from ..mud.exceptions import Crapup


def occur(terminal, active=False):
    if not active:
        return
    terminal.next_turn()


def ctrlc(terminal, active=False):
    print("^C")
    if terminal.user.in_fight:
        return
    terminal.user.loseme()
    try:
        raise Crapup("Byeeeeeeeeee  ...........", terminal=terminal)
    except Crapup as e:
        print(e)
        exit(0)


def oops(terminal, active=False):
    terminal.user.loseme()
    exit(255)
