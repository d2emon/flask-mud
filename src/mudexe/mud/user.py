from global_vars import logger
from datetime import datetime


from auth.models import User as UserModel


from ..gamego.signals import alarm
from ..models import Message, Player, Person
from .exceptions import Crapup
from .textbuff import TextBuffer
from .room import Room
from .tty import special
from .world import World


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


# ???
def gamecom(msg):
    logger().debug("<<< gamecom(%s)", msg)


# ???
def calibme():
    logger().debug("<<< calibme()")


# ???
def hitplayer(enemy, weapon):
    logger().debug("<<< hitplayer(%s, %s)", enemy, weapon)


# ???
def dosumm(ades):
    logger().debug("<<< dosumm(%s)", ades)


# ???
def forchk():
    logger().debug("<<< forchk()")


class DeathRoom(Crapup):
    def __init__(self):
        Crapup.__init__(self, "bye bye.....")


class User():
    # ???
    ail_blind = False
    # ???
    curmode = False
    # ???
    in_fight = 0
    # ???
    fighting = None
    # ???
    wpnheld = -1
    # ???
    ail_dumb = False

    def __init__(self, name):
        self.name = name  # globme
        self.model = UserModel.query.by_username(self.name)
        if self.model is None:
            self.model = UserModel(username=self.name)
            self.model.save()

        self.message_id = None  # cms
        self.location = 0  # curch

        self.i_setup = False
        # self.mynum = 0
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
        self.interrupt = False
        self.last_io_interrupt = None
        self.me_ivct = 0
        self.me_drunk = 0
        self.me_cal = 0

        # Other
        self.buff = TextBuffer()
        # self.terminal = Terminal("MUD_PROGRAM_NAME", self.name)
        # self.terminal.set_user(self)
        self.world = World()
        self.player = Player.query.by_user(self.model)
        self.person = Person.query.by_user(self.model)

    # ???
    def on_timing(self):
        logger().debug("<<< on_timing()")
        return 0

    def time_to_interrupt(self):
        if self.last_io_interrupt is None:
            self.last_io_interrupt = datetime.now()
            return True

        timeleft = datetime.now() - self.last_io_interrupt
        if timeleft.seconds > 2:
            self.last_io_interrupt = datetime.now()
            return True

        return self.interrupt

    def prepare_game(self):
        self.message_id = None
        self.put_player()
        self.rte()
        self.world.closeworld()

        self.message_id = None
        self.special(".g")
        self.i_setup = True

    def special(self, cmd):
        special(cmd, self)

    def put_player(self):
        """
        PutMeOn
        """
        self.iamon = False
        self.player = self.world.put_player(self)
        self.iamon = True
        return self.player

    def rte(self):
        self.world.openworld()
        if self.message_id is None:
            self.message_id = Message.query.findend()
        messages = Message.query.readmsg(self.message_id)
        self.message_id = Message.query.findend()
        for message in messages:
            self.mstoout(message)
        self.update()
        self.eorte()
        self.rdes = 0
        self.tdes = 0
        self.vdes = 0

    def eorte(self):
        self.interrupt = self.time_to_interrupt()
        if self.interrupt:
            self.last_io_interrupt = datetime.now()

        # Tick invisibility counter
        self.invisibility_next_round()

        # Calibration needed
        if self.me_cal:
            self.me_cal = 0
            calibme()

        # Is summonned
        if self.tdes:
            dosumm(self.ades)

        # Is fighting
        self.fight_next_round(interrupt=self.interrupt)

        # if objects[18].iswornby(self.player) or randperc() < 10:
        #     self.person.strength += 1
        #     if self.i_setup:
        #         calibme()

        forchk()

        self.drunk_next_round()
        self.interrupt = False

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

    def sendsys(self, to_player, message_code, channel=None, text=""):
        if channel is None:
            channel = self.location
        # if msg_code != -9900 and msg_code != -10021:
        #     block[64] = text
        # else:
        #     block[64] = i[0]
        #     block[65] = i[1]
        #     block[66] = i[2]
        self.send2(to_player, message_code, channel, text)

    def send2(self, to_player, message_code, channel, text):
        if to_player is not None:
            to_player = to_player.player
        msg = Message(
            from_player=self.player,
            to_player=to_player,
            message_code=message_code,
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
            person.sex = self.terminal.asksex()
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

    def loseme(self):
        alarm.sig_aloff()
        # No interruptions while you are busy dying
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
        if self.person.is_wizzard:
            self.buff.bprintf("<DEATH ROOM>\n")
        else:
            self.loseme()
            raise DeathRoom

    @property
    def prmpt(self):
        convflgs = {
            0: ">",
            1: "\"",
            2: "*",
        }
        prmpt = ""
        if self.debug_mode:
            prmpt += "#"
        if self.person.is_wizzard:
            prmpt += "----"
        prmpt += convflgs.get(self.convflg, "?")
        if self.player.visibility:
            prmpt = "(%s)" % prmpt
        return "\r" + prmpt

    def end_fight(self):
        self.in_fight = 0
        self.fighting = None

    def fight_next_round(self, interrupt=False):
        if self.fighting is None:
            return

        enemy = Player.query.get(self.fighting)
        if enemy is None:
            self.end_fight()
        elif enemy.location != self.location:
            self.end_fight()

        if self.in_fight:
            self.in_fight -= 1

        if interrupt:
            if self.in_fight:
                self.in_fight = 0
                hitplayer(self.fighting, self.wpnheld)

    def invisibility_next_round(self):
        """
        Invisibility counter
        """
        if self.me_ivct:
            self.me_ivct -= 1
        if self.me_ivct == 1:
            self.player.visibility = 0

    def drunk_next_round(self):
        if self.me_drunk > 0:
            self.me_drunk -= 1
            if not self.ail_dumb:
                self.hiccup()

    def apply_convflg(self, work):
        if self.convflg == 0:
            return work
        elif self.convflg == 1:
            return self.say(work)
        else:
            return self.tss(work)

    def next_turn(self):
        self.interrupt = True
        self.rte()
        self.interrupt = False
        self.on_timing()

    # Actions
    def say(self, message=""):
        return "say %s" % (message)

    def tss(self, message=""):
        return "tss %s" % (message)

    def hiccup(self):
        return gamecom("hiccup")

    def look(self, room=None):
        """
        Lords ????
        """
        if room is None:
            room = self.location

        self.world.closeworld()

        r = Room(room)

        blind_msg = ""
        if self.ail_blind:
            blind_msg = "You are blind... you can't see a thing!\n"

        roomname = ""
        if self.person.is_wizzard:
            roomname = r.showname(self)

        description = r.look(self)

        if r.nobr:
            self.brmode = False

        if r.deathroom:
            self.ail_blind = False

        if self.ail_blind:
            description = ""

        if self.brmode:
            description = ""

        text = "%s%s%s\n" % (
            blind_msg,
            roomname,
            r.look(self),
        )
        self.buff.bprintf(text)
        if r.deathroom:
            self.ail_blind = False
            self.deathroom()

        obs = ""
        people = ""
        if r.cansee(self):
            obs = r.lisobs(self)
            if self.curmode:
                pepople = self.lispeople(self)
        self.buff.bprintf("%s%s" % (obs, people))

        onlook()
