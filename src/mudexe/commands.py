from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
# from .models import User, Role


from global_vars import logger
from mudexe.gamego.signals import sig_init, sig_ctrlc


manager = Manager(usage="Main application")


# ???
argv_p = []
# ???
globme = ""
# ???
tty = 0


# ???
def cuserid(user):
    logger().debug("<<< cuserid(%s)" % (user, ))
    return 0


# ???
def talker(user):
    logger().debug("<<< talker(%s)" % (user, ))


@manager.option('-n', '--name', dest='username', default=None)
def play(username=None, **kwargs):
    """
    Play game
    """
    global globme, tty, argv_p
    sig_init()
    argv_p = username
    if username is None:
        print("Args!")
        exit(0)
    print("Entering Game ....")
    tty = 0
    # if tty == 4:
    #   initbbc()
    #   initscr()
    #   topscr()
    if username == "Phantom":
        globme = "The %s" % (username)
    else:
        globme = username
    print("Hello %s" % (globme))
    logger().info("GAME ENTRY: %s[%s]", globme, cuserid(None))
    talker(globme)

    sig_ctrlc()
