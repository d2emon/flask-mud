from global_vars import logger
from . import crapup


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
__timeout = 2


def signal(sig_id, sig):
    global __signals
    __signals[sig_id] = sig
    logger().debug("<<< signal(%d, %s)", sig_id, sig)


def alarm(t):
    global __timeout
    __timeout = t
    logger().debug("<<< alarm(%d)", t)


sig_active = False


def sig_alon():
    global sig_active
    sig_active = True
    signal(SIGALRM, sig_occur)
    alarm(2)


"""
unblock_alarm()
{
extern int sig_occur();
signal(SIGALRM,sig_occur);
if(sig_active) alarm(2);
}

block_alarm()
{
signal(SIGALRM,SIG_IGN);
}
"""


def sig_aloff():
    global sig_active
    sig_active = False
    signal(SIGALRM, SIG_IGN)
    alarm(2147487643)


interrupt = False


def sig_occur():
    # extern char globme[];
    global interrupt
    if not sig_active:
        return
    sig_aloff()
    # openworld()
    interrupt = True
    # rte(globme)
    interrupt = False
    # on_timing()
    # closeworld()
    # key_reprint()
    sig_alon()


def sig_init():
    signal(SIGHUP, sig_oops)
    signal(SIGINT, sig_ctrlc)
    signal(SIGTERM, sig_ctrlc)
    signal(SIGTSTP, SIG_IGN)
    signal(SIGQUIT, SIG_IGN)
    signal(SIGCONT, sig_oops)


def sig_oops():
    sig_aloff()
    # loseme()
    exit(255)


def sig_ctrlc():
    # extern in_fight;
    print("^C")
    # if in_fight:
    #     return
    sig_aloff()
    # loseme()
    crapup("Byeeeeeeeeee  ...........")
