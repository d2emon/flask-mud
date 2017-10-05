from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
# from .models import User, Role


from global_vars import logger
from mudexe.mud.user import User


from mudexe.gamego.signals import sig_init, sig_ctrlc
from mudexe.talker import talker


manager = Manager(usage="Main application")


# ???
argv_p = []
# ???
tty = 0


@manager.option('-n', '--name', dest='username', default=None)
def play(username=None, **kwargs):
    """
    Play game
    """
    global tty, argv_p
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
    user = User(username)
    print("Hello %s" % (user.fullname))
    logger().info("GAME ENTRY: %s[%s]", user.fullname, user.cuserid(None))
    talker(user)

    sig_ctrlc()
