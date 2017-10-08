from global_vars import logger
from ..gamego.signals import alarm
from ..models import Message, User as UserModel, Player, Person, SEX_MALE, SEX_FEMALE
from .textbuff import TextBuffer
from .room import Room
from .tty import Terminal
from .world import World


sexes = {
    'm': SEX_MALE,
    'f': SEX_FEMALE,
}


# ???
def eorte():
    logger().debug("<<< eorte()")


# ???
def gamrcv(msg):
    logger().debug("<<< gamrcv(%s)", msg)


# ???
def randperc():
    logger().debug("<<< randperc()")
    return 25


# ???
def onlook():
    logger().debug("<<< onlook()")


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
        self.model = UserModel.query.filter_by(name=self.name).first()
        if self.model is None:
            self.model = UserModel(name=self.name)
            self.model.save()

        self.i_setup = False
        self.cms = None
        self.mynum = 0
        self.curch = 0
        self.iamon = False
        self.lasup = 0
        self.curmode = 0

        # Other
        self.player = Player()
        self.buff = TextBuffer()
        self.terminal = Terminal("MUD_PROGRAM_NAME", self.name)
        self.terminal.set_user(self)
        self.world = World()

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

    def putmeon(self):
        self.iamon = False
        self.world.openworld()
        f = False
        self.mynum = self.world.find_empty(self.player)

        self.player = Player(user=self.model)
        self.player.name = self.name
        self.player.location = self.curch
        self.player.last_message = None
        self.player.level = 1
        self.player.visibility = 0
        self.player.strength = -1
        self.player.weapon = -1
        self.player.sex = 0
        self.iamon = True
        return True

    def rte(self):
        self.world.openworld()
        if self.cms is None:
            self.cms = Message.query.findend()
        messages = Message.query.readmsg(self.cms)
        self.cms = Message.query.findend()
        for msg in messages:
            self.mstoout(msg)
        self.update()
        eorte()
        self.rdes = 0
        self.tdes = 0
        self.vdes = 0

    def update(self):
        xp = self.cms - self.lasup
        if xp < 0:
            xp = -xp
        if xp < 10:
            return
        self.world.openworld()
        self.player.message_id = self.cms
        self.lasup = self.cms

    def mstoout(self, msg):
        """
        Print appropriate stuff from data block
        """
        if self.debug_mode:
            self.buff.bprintf("\n%s" % (msg))
        if msg.is_text:
            self.buff.bprintf(msg.text)
        else:
            self.sysctrl(msg)

    def sysctrl(self, msg):
        gamrcv(msg)

    def start_game(self):
        self.curmode = 1
        rooms = [-5, -183]
        self.initme()
        self.world.openworld()
        self.player.strength = self.person.strength
        self.player.level = self.person.level
        if self.person.level < 10000:
            self.player.visibility = 0
        else:
            self.player.visibility = -1
        self.player.sex = self.person.sex
        self.player.helping = -1
        xy = "<s user=\"%s\">%s  has entered the game\n</s>" % (self.model.id, self.name)
        xx = "<s user=\"%s\">[ %s  has entered the game ]\n</s>" % (self.model.id, self.name)
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

    def initme(self):
        person = Person.query.by_user(self.model).first()
        if person is None:
            self.buff.bprintf("Creating character....")
            person = Person(user=self.model)
            sex = None
            while sex is None:
                self.buff.bprintf("\nSex (M/F) : ")
                self.buff.pbfr(self)
                # self.terminal.keysetback()
                sex_id = self.terminal.getkbd(1).lower()
                # self.terminal.keysetup()
                sex = sexes.get(sex_id)
                if sex is None:
                    self.buff.bprintf("M or F")
            person.sex = sex
        person.save()
        self.person = person
        return person

    # ???
    def saveme(self):
        logger().debug("<<< saveme()")

    def trapch(self, chan):
        self.world.openworld()
        self.player.location = chan
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
        if self.person.level > 9:
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
        if self.player.visibility < 10000:
            bk = "%s has departed from AberMUDII\n" % (self.name)
            self.sendsys(self, -10113, 0, bk)
        self.world.players[self.mynum] = None
        self.world.closeworld()
        if not self.zapped:
            self.saveme()

        sntn = self
        self.buff.chksnp(sntn, self)

    def deathroom(self):
        if self.person.level > 9:
            self.buff.bprintf("<DEATH ROOM>\n")
        else:
            self.loseme()
            self.terminal.crapup("bye bye.....\n")

    @property
    def prmpt(self):
        prmpt = ""
        if self.debug_mode:
            prmpt += "#"
        if self.person.level > 9:
            prmpt += "----"
        if self.convflg == 0:
            prmpt += ">"
        elif self.convflg == 1:
            prmpt += "\""
        elif self.convflg == 2:
            prmpt += "*"
        else:
            prmpt += "?"
        if self.player.visibility:
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

    def do_loop(self):
        self.buff.pbfr(self)
        self.terminal.sendmsg(self)
        if self.buff.rd_qd:
            self.rte()
        self.buff.rd_qd = False
        self.world.closeworld()
        self.buff.pbfr(self)

    def next_turn(self):
        self.world.openworld()
        interrupt = True
        self.rte()
        interrupt = False
        # on_timing()
        self.world.closeworld()
        self.terminal.key_reprint()
