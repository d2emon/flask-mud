from flask_script import Manager
# from flask_script import Manager, prompt, prompt_pass
# from . import app, db
from app import app
# from .models import User, Role
import os


from global_vars import logger


from .hmk import hmk
from .makeworld import makeworld
from .ogenerate import ogenerate
from .makeuaf import makeuaf
from .mud_exe import compile as compile_mud_exe
from .mud1 import compile as compile_mud_1


from mudexe.models.location import Location


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


@manager.command
def loadrooms():
    """
    Load Rooms
    """
    for i in range(1, 1125):
        print("Loading room %d" % (i))
        filename = os.path.join(app.config.get('ROOMS_FOLDER', 'rooms'), str(i))
        print(filename)
        l = Location.query.get(i)
        if l is None:
            l = Location()
            l.id = i
        l.name = "Channel %d" % (i)
        try:
            l.load_from_file(filename)
        except FileNotFoundError:
            pass
        print(l.id, l.name)
        print(l.north, l.east, l.south, l.west, l.up, l.down)
        print(l.nobr, l.deathroom)
        print(l.description)
        l.save()
