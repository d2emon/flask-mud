from global_vars import logger
from ..gamego.signals import alarm
from .textbuff import TextBuffer
from .room import Room
from .tty import Terminal


# ???
def eorte():
    logger().debug("<<< eorte()")


# ???
def gamrcv(msg):
    logger().debug("<<< gamrcv(%s)", msg)


# ???
def initme():
    logger().debug("<<< initme()")


# ???
def randperc():
    logger().debug("<<< randperc()")
    return 25


# ???
def onlook():
    logger().debug("<<< onlook()")


# ???
def chksnp():
    logger().debug("<<< chksnoop()")


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
    # ???
    my_str = 0
    # ???
    my_lev = 0
    # ???
    my_sex = 0
    # ???
    ail_blind = False
    # ???
    curmode = False
    # ???
    brmode = False
    # ???
    zapped = False
    # ???
    in_fight = 0
    # ???
    fighting = None
    # ???
    convflg = 0

    def __init__(self, name):
        self.name = name  # globme
        self.i_setup = False
        self.cms = -1
        self.mynum = 0
        self.curch = 0
        self.iamon = False
        self.lasup = 0
        self.curmode = 0
        # Other
        self.player = PlayerData()
        self.buff = TextBuffer()
        self.terminal = Terminal("MUD_PROGRAM_NAME", self.name)
        self.terminal.buff = self.buff
        self.world = None

    @property
    def fullname(self):
        if self.name == "Phantom":
            return "The %s" % (self.name)
        else:
            return self.name

    # ???
    def cuserid(self):
        logger().debug("<<< cuserid(%s)", self)
        return 0

    def putmeon(self, world=None):
        self.iamon = False
        world.openworld()
        f = False
        if self.fpbn() is not None:
            self.terminal.crapup("You are already on the system - you may only be on once at a time")
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

    def start_game(self):
        self.curmode = 1
        rooms = [-5, -183]
        initme()
        self.world.openworld()
        self.player.strength = self.my_str
        self.player.lev = self.my_lev
        if self.my_lev < 10000:
            self.player.vis = 0
        else:
            self.player.vis = -1
        self.player.sexall = self.my_sex
        self.player.helping = -1
        us = self.cuserid()
        xy = "<s user=\"%s\">%s  has entered the game\n</s>" % (self.name, self.name)
        xx = "<s user=\"%s\">[ %s  has entered the game ]\n</s>" % (self.name, self.name)
        self.sendsys(self, -10113, text=xx)
        self.rte()
        if randperc() > 50:
            room = rooms[0]
        else:
            room = rooms[1]
        self.curch = room
        self.trapch(room)
        self.sendsys(self, -10000, text=xy)

    # ???
    def sendsys(self, to_user, msg_code, channel=None, text=""):
        if channel is None:
            channel = self.curch
        logger().debug("<<< sendsys(%s, %s, %s, %s, %s)", self, to_user, msg_code, channel, text)

    # ???
    def dumpitems(self):
        logger().debug("<<< dumpitems()")

    # ???
    def saveme(self):
        logger().debug("<<< saveme()")

    def trapch(self, chan):
        self.world.openworld()
        self.player.loc = chan
        self.lookin()

    def lookin(self, room=None):
        """
        Lords ????
        """
        if room is None:
            room = self.curch
        self.world.closeworld()
        r = Room(room)
        if self.ail_blind:
            self.buff.bprintf("You are blind... you can't see a thing!\n")
        if self.my_lev > 9:
            self.buff.bprintf(r.showname())
        self.buff.bprintf(r.look(self))
        self.buff.bprintf("\n")
        if r.deathroom:
            self.deathroom()
        onlook()

    def loseme(self):
        alarm.sig_aloff()  # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.i_setup = False
        self.world.openworld()
        self.dumpitems()
        if self.player.vis < 10000:
            bk = "%s has departed from AberMUDII\n" % (self.name)
            self.sendsys(self, -10113, 0, bk)
        self.world.players[self.mynum] = None
        self.world.closeworld()
        if not self.zapped:
            self.saveme()
        chksnp()

    def deathroom(self):
        if self.my_lev > 9:
            self.buff.bprintf("<DEATH ROOM>\n")
        else:
            self.loseme()
            self.terminal.crapup("bye bye.....\n")

    @property
    def prmpt(self):
        prmpt = ""
        if self.debug_mode:
            prmpt += "#"
        if self.my_lev > 9:
            prmpt += "----"
        if self.convflg == 0:
            prmpt += ">"
        elif self.convflg == 1:
            prmpt += "\""
        elif self.convflg == 2:
            prmpt += "*"
        else:
            prmpt += "?"
        if self.player.vis:
            prmpt = "(%s)" % prmpt
        return "\r" + prmpt

    def fight_next_round(self):
        if self.fighting:
            f = self.world.player[self.fighting]
            if f is None:
                self.in_fight = 0
                self.fighting = None
            elif f.loc != self.curch:
                self.in_fight = 0
                self.fighting = None
        if self.in_fight:
            self.in_fight -= 1

    def apply_convflg(self, work):
        if not self.convflg:
            return work
        if self.convflg == 1:
            return "say %s" % (work)
        else:
            return "tss %s" % (work)
