from global_vars import logger
from ..gamego import crapup
from .textbuff import TextBuffer


# ???
def eorte():
    logger().debug("<<< eorte()")


# ???
def gamrcv(msg):
    logger().debug("<<< gamrcv(%s)", msg)


class PlayerData():
    def load(self, ct):
        self.ct = ct
        self.name = ""
        self.loc = 0
        self.pos = -1
        self.lev = 1
        self.vis = 0
        self.strength = -1
        self.wpn = -1
        self.sex = 0


class User():
    # ???
    debug_mode = True
    # ???
    rdes = 0
    # ???
    vdes = 0
    # ???
    tdes = 0

    def __init__(self, name):
        self.name = name  # globme
        self.i_setup = False
        self.cms = -1
        self.mynum = 0
        self.curch = 0
        self.iamon = False
        self.lasup = 0
        # Other
        self.player = PlayerData()
        self.buff = TextBuffer()
        self.world = None

    @property
    def fullname(self):
        if self.name == "Phantom":
            return "The %s" % (self.name)
        else:
            return self.name

    # ???
    def cuserid(self, user):
        logger().debug("<<< cuserid(%s)" % (user, ))
        return 0

    def putmeon(self, world=None):
        self.iamon = False
        world.openworld()
        f = False
        if self.fpbn() is not None:
            crapup("You are already on the system - you may only be on once at a time")
        self.mynum = world.find_empty(self.player)
        self.world = world

        self.player.load(self.mynum)
        self.player.name = self.name
        self.player.loc = self.curch
        self.player.pos = -1
        self.player.lev = 1
        self.player.vis = 0
        self.player.strength = -1
        self.player.wpn = -1
        self.player.sex = 0
        self.iamon = True
        return True

    def rte(self):
        self.world.openworld()
        if self.cms == -1:
            self.cms = self.world.findend()
        too = self.world.findend()
        ct = self.cms
        # while ct < too:
        # while ct >= too:
        for ct in range(self.cms, too):
            msg = self.world.readmsg(ct)
            self.mstoout(msg)
        self.cms = ct
        self.update()
        eorte()
        self.rdes = 0
        self.tdes = 0
        self.vdes = 0

    def fpbn(self):
        logger().debug("<<< fpbn(%s)", self.name)
        return None

    def update(self):
        xp = self.cms - self.lasup
        if xp < 0:
            xp = -xp
        if xp < 10:
            return
        self.world.openworld()
        self.player.pos = self.cms
        self.lasup = self.cms

    def mstoout(self, msg):
        # Print appropriate stuff from data block
        if self.debug_mode:
            self.buff.bprintf("\n<%d>" % (msg.msg_code))
        if msg.msg_code < -3:
            self.sysctrl(msg)
        else:
            self.buff.bprintf(msg.text)

    def sysctrl(self, msg):
        gamrcv(msg)
