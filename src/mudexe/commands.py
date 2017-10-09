from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
# from .models import User, Role


from global_vars import logger
from mudexe.mud.user import User


from mudexe.gamego.signals import do_signal, SIGALRM, SIGTERM, sig_init
from mudexe.talker import talker


manager = Manager(usage="Main application")


@manager.option('-n', '--name', dest='username', default=None)
def play(username=None, **kwargs):
    """
    Play game
    """
    if username is None:
        raise Exception("Args!")

    sig_init()
    print("Entering Game ....")
    user = User(username)
    print("Hello %s" % (user.fullname))
    logger().info("GAME ENTRY: %s[%s]", user.fullname, user.cuserid())
    talker(user)

    for i in range(5):
        do_signal(SIGALRM, user)
    do_signal(SIGTERM, user)
