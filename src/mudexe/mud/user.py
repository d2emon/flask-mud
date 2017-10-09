from global_vars import logger
from ..gamego.signals import alarm
from ..models import Message, User as UserModel, Person, SEX_MALE, SEX_FEMALE
from .textbuff import TextBuffer
from .room import Room
from .tty import Terminal, special
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
    ail_blind = False
    # ???
    curmode = False
    # ???
    in_fight = 0
    # ???
    fighting = None

    def __init__(self, name):
        self.name = name  # globme
        self.model = UserModel.query.filter_by(name=self.name).first()
        if self.model is None:
            self.model = UserModel(name=self.name)
            self.model.save()

        self.message_id = None  # cms
        self.location = 0  # curch

        self.i_setup = False
        self.mynum = 0
        self.iamon = False
        self.lasup = 0
        self.curmode = 0
        self.convflg = 0
        self.debug_mode = True  # False
        self.tdes = 0
        self.rdes = 0
        self.vdes = 0
        self.ades = 0
        self.zapped = False
        self.brmode = False

        # Other
        self.player = None
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

    def prepare_game(self):
        self.message_id = None
        self.putmeon()
        self.rte()
        self.world.closeworld()
        self.message_id = None
        self.special(".g")
        self.i_setup = True

    def special(self, cmd):
        special(cmd, self)

    def putmeon(self):
        self.iamon = False
        self.player = self.world.find_empty(self)
        self.mynum = self.player.id
        self.player.save()
        self.iamon = True
        return True

    def rte(self):
        self.world.openworld()
        if self.message_id is None:
            self.message_id = Message.query.findend()
        messages = Message.query.readmsg(self.message_id)
        self.message_id = Message.query.findend()
        for message in messages:
            self.mstoout(message)
        self.update()
        eorte()
        self.rdes = 0
        self.tdes = 0
        self.vdes = 0

    def update(self):
        xp = self.message_id - self.lasup
        if xp < 0:
            xp = -xp
        if xp < 10:
            return
        self.world.openworld()
        self.player.message_id = self.message_id
        self.lasup = self.message_id

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
        self.location = room
        self.trapch(room)
        self.sendsys(self, -10000, text=xy)

    def sendsys(self, to_user, msg_code, channel=None, text=""):
        if channel is None:
            channel = self.location
        # if msg_code != -9900 and msg_code != -10021:
        #     block[64] = text
        # else:
        #     block[64] = i[0]
        #     block[65] = i[1]
        #     block[66] = i[2]
        self.send2(to_user, msg_code, channel, text)

    def send2(self, to_user, msg_code, channel, text):
        if to_user is not None:
            to_user = to_user.player
        msg = Message(
            from_player=self.player,
            to_player=to_user,
            message_code=msg_code,
            # channel=channel,
            text=text,
        )
        msg.save()
        # number = self.world.findend() - self.world.findstart()
        # if number >= 199:
        #     self.cleanup()
        #     longwthr()

    def dumpitems(self):
        self.world.dumpstuff(self.mynum, self.location)

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

    def saveme(self):
        # self.person.strength = self.my_str
        # self.person.level = self.my_lev
        self.person.sex = self.player.sex
        # self.person.sco = self.my_sco
        if self.zapped:
            return
        self.buff.bprintf("\nSaving %s\n" % (self.name))
        self.person.save()

    def trapch(self, chan):
        self.world.openworld()
        self.player.location = chan
        self.lookin()

    def lookin(self, room=None):
        """
        Lords ????
        """
        if room is None:
            room = self.location
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
        if not self.zapped:
            self.saveme()
        self.player.delete()
        self.world.closeworld()

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
            elif f.location != self.location:
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
