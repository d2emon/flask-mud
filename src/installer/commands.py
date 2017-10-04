from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
# from .models import User, Role


from .hmk import hmk
from .makeworld import compile as compile_makeworld
from .ogenerate import compile as compile_ogenerate
from .makeuaf import compile as compile_makeuaf
from .mud_exe import compile as compile_mud_exe
from .mud1 import compile as compile_mud_1


manager = Manager(usage="Application installer")


def mkdir(dirname):
    print(">>> mkdir %s" % (dirname, ))


def catnull(filename):
    print(">>> cat </dev/null >%s" % (filename, ))


def cp(src, dst):
    print(">>> cp %s %s" % (src, dst))


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
    print(hmk("files.h"))
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
    e = compile_makeworld()
    e()
    print("Game universe intialised")


@manager.command
def resetdata():
    """
    Generate reset data
    """
    print("Compiling reset data compiler")
    e = compile_ogenerate()
    e()
    cp("ob.out", "reset_data")
    print("Reset data generated")


@manager.command
def generateuaf():
    """
    Generate uaf
    """
    print("Compiling uaf generator")
    e = compile_makeuaf()
    e("uaf.rand")
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
