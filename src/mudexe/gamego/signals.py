from global_vars import logger
# from . import crapup
from .alarm import occur, ctrlc, oops


SIGHUP = 0
SIGINT = 1
SIGTERM = 2
SIGTSTP = 3
SIGQUIT = 4
SIGCONT = 5
SIGALRM = 6


SIG_IGN = None


__signals = {
    SIGHUP: SIG_IGN,
    SIGINT: SIG_IGN,
    SIGTERM: SIG_IGN,
    SIGTSTP: SIG_IGN,
    SIGQUIT: SIG_IGN,
    SIGCONT: SIG_IGN,
    SIGALRM: SIG_IGN,
}


class Alarm():
    timeout = 2
    active = False

    def alarm(self, t):
        self.timeout = t
        logger().debug("<<< alarm(%d)", t)

    def sig_alon(self):
        self.active = True
        signal(SIGALRM, occur)
        self.alarm(2)

    def sig_aloff(self):
        self.active = False
        signal(SIGALRM, SIG_IGN)
        self.alarm(2147487643)

    def unblock_alarm(self):
        signal(SIGALRM, occur)
        if self.active:
            self.alarm(2)

    def block_alarm(self):
        signal(SIGALRM, SIG_IGN)


alarm = Alarm()


def signal(sig_id, sig):
    global __signals
    __signals[sig_id] = sig
    # logger().debug("<<< signal(%d, %s)", sig_id, sig)


def sig_init():
    signal(SIGHUP, oops)
    signal(SIGINT, ctrlc)
    signal(SIGTERM, ctrlc)
    signal(SIGTSTP, SIG_IGN)
    signal(SIGQUIT, SIG_IGN)
    signal(SIGCONT, oops)


def do_signal(sig_id, user):
    global alarm
    logger().debug("SIGNAL%s occured", sig_id)
    active = alarm.active
    s = __signals.get(sig_id)
    if s is None:
        return
    alarm.sig_aloff()
    res = s(user, active=active)
    alarm.sig_alon()
    return res
