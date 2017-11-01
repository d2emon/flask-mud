class Crapup(Exception):
    """
    crapup("Sorry AberMUD is currently unavailable")
    crapup("Cannot find World file")
    """
    def __init__(self, msg, terminal=None):
        self.msg = msg
        self.terminal = terminal

    def crapup(self, msg=None, terminal=None):
        dashes = "-" + "=-" * 80

        if terminal is None:
            terminal = self.terminal
        if msg is None:
            msg = self.msg

        if terminal is not None:
            terminal.pbfr()
            terminal.buff.pr_due = 0  # So we dont get a prompt after the exit

        res = "\n".join([
            "",
            dashes,
            "",
            msg,
            "",
            dashes,
        ])
        return res
        # print(res)
        # exit(0)

    def __str__(self):
        return self.crapup()


class GoError(Exception):
    """
    """
    def __init__(self, msg="You can't go that way"):
        self.msg = msg

    def __str__(self):
        return self.msg
