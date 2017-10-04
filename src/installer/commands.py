from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
# from .models import User, Role


from global_vars import logger


from .hmk import hmk
from .makeworld import makeworld
from .ogenerate import ogenerate
from .makeuaf import makeuaf
from .mud_exe import compile as compile_mud_exe
from .mud1 import compile as compile_mud_1


manager = Manager(usage="Application installer")


def mkdir(dirname):
    logger().debug("mkdir %s" % (dirname, ))


def catnull(filename):
    logger().debug("cat </dev/null >%s" % (filename, ))


def cp(src, dst):
    logger().debug("cp %s %s" % (src, dst))


# Compilers
@manager.command
def makedirs():
    """
    Make directories
    """
    print("Making directories")
    mkdir("TEXT")
    mkdir("SNOOP")
    mkdir("EXAMINES")
    mkdir("TEXT/ROOMS")


@manager.command
def initfiles():
    """
    Initialize files
    """
    print("Initialising files")
    catnull("mud_syslog")
    catnull("reset_t")
    catnull("reset_n")
    catnull("user_file")


@manager.command
def compileh():
    """
    Compile .h constructor
    """
    print("Compiling .h constructor")
    logger().debug("./hmk >%s", "files.h")
    settings = hmk()
    logger().debug(settings)
    print(".h built")


@manager.command
def compilemudexe():
    """
    Compile mud.exe
    """
    print("Compiling mud.exe")
    compile_mud_exe()


@manager.command
def compilemud1():
    """
    Compile mud.1
    """
    print("Compiling mud.1")
    compile_mud_1()


@manager.command
def worldmake():
    """
    Initialize game universe
    """
    print("Compiling world maker")
    makeworld()
    print("Game universe intialised")


@manager.command
def resetdata():
    """
    Generate reset data
    """
    print("Compiling reset data compiler")
    ogenerate()
    cp("ob.out", "reset_data")
    print("Reset data generated")


@manager.command
def generateuaf():
    """
    Generate uaf
    """
    print("Compiling uaf generator")
    makeuaf("uaf.rand")
    print("Ok")


@manager.command
def install1():
    """
    Install application. Part 1
    """
    makedirs()
    initfiles()
    compileh()
    compilemudexe()
    compilemud1()
    print("Done")


@manager.command
def install2():
    """
    Install application. Part 2
    """
    worldmake()
    resetdata()
    generateuaf()
    print("Now set up a password for arthur the archwizard")


@manager.command
def install():
    """
    Install application
    """
    install1()
    install2()


# Menu Items
@manager.option('-n', '--name', dest='username', default=None)
def change_password(username=None, **kwargs):
    return
