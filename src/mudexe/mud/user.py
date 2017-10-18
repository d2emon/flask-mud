from global_vars import logger
from datetime import datetime
import random


from auth.models import User as UserModel


from ..gamego.signals import alarm
from ..models import Message, Person
from ..models.player import Player, SEX_FEMALE
from ..models.location import STARTING_LOCATIONS, Location
from ..models.item import Item, Door
from .exceptions import Crapup, GoError
from .textbuff import TextBuffer
from .tty import special
from .world import World


# ???
def gamrcv(msg):
    logger().debug("<<< gamrcv(%s)", msg)


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
    in_fight = 0
    # ???
    fighting = None
    # ???
    wpnheld = -1
    # ???
    ail_dumb = False
    # ???
    has_farted = False
    # ???
    wd_it = ""
    # ???
    wd_him = ""
    # ???
    wd_her = ""
    # ???
    wd_them = ""
    # ???
    wd_there = ""
    # ???
    in_ms = ""
    # ???
    out_ms = ""

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
        self.curmode = 1  # 0
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
        self.person = Person.initme(self.model)
        # self.person = Person.query.by_user(self.model)

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

    def load(self):
        if self.player is None:
            return False
        if self.person is None:
            return False
        self.location = self.player.location
        self.message_id = self.player.message_id
        self.room = Location.query.get(self.location)
        return True

    def prepare_game(self):
        print(self)

        self.message_id = None
        self.put_player()
        self.rte()
        self.world.closeworld()

        self.message_id = None

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
        if not self.interrupt:
            return

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
        rooms = STARTING_LOCATIONS
        self.person = Person.initme(self.model)
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
        room = random.choice(rooms)
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
        self.world.dumpstuff(self.player, self.location)

    def trapch(self, chan=None):
        if chan is None:
            chan = self.location

        self.world.openworld()
        self.player.location = chan
        # ???
        self.player.save()
        # ???
        self.look()

    def deathroom(self, room):
        if not room.deathroom:
            return
        self.ail_blind = False
        if self.person.is_wizzard:
            self.buff.bprintf("<DEATH ROOM>\n")
        else:
            self.buff.bprintf(self.look_room_description(room))
            self.death()
            raise DeathRoom

    def death(self):
        self.i_setup = False
        self.world.openworld()
        self.dumpitems()
        if self.player.visibility < 10000:
            bk = "%s has departed from AberMUDII\n" % (self.name)
            self.sendsys(user, -10113, 0, bk)
        if not self.zapped:
            self.person.saveme(self, zapped=self.zapped)
        self.player.delete()
        self.world.closeworld()

        sntn = self
        self.buff.chksnp(sntn, user)

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

    def is_dark(self, room):
        if self.person.is_wizzard:
            return False
        return not room.has_light

    def cansee(self, room):
        if self.ail_blind:
            return False
        return not self.is_dark(room)

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

    def look(self, room_id=None):
        """
        Lords ????
        """
        if room_id is None:
            room_id = self.location

        self.world.closeworld()

        room = Location.search(room_id)

        if self.person.is_wizzard:
            self.wd_there = room.name

        self.world.openworld()

        if room.nobr:
            self.brmode = False

        if room.deathroom:
            self.deathroom(room)

        onlook()
        return {
            "room": room,
            "description": self.look_room_description(room),
            "objects": self.look_room_objects(room),
            "people": self.look_room_people(room),
        }
        # self.buff.bprintf("\n".join([
        #     roomtext["title"],
        #     roomtext["description"],
        #     roomtext["objects"],
        #     roomtext["people"],
        # ]))

    def look_room_description(self, room):
        if self.brmode:
            return ""
        if self.is_dark(room):
            return "It is dark"
        return room.description

    def look_room_objects(self, room):
        if not self.cansee(room):
            return []
        return room.list_objects(self)

    def look_room_people(self, room):
        if not self.cansee(room):
            return []
        if not self.curmode:
            return []
        return room.list_people(self)

    def wd_people(self, p):
        """
        Assign Him her etc according to who it is
        """
        # if p.id > 15 and p != Player.query.fpbns("riatha") and p != Player.query.fpbns("shazareth"):
        #     self.wd_it = p.name
        #     return
        if p.sex == SEX_FEMALE:
            self.wd_her = p.name
        else:
            self.wd_him = p.name
        self.wd_them = self.name

    def go(self, direction):
        EXITS = [
            "north",
            "east",
            "south",
            "west",
            "up",
            "down",
        ]

        if self.in_fight > 0:
            raise GoError("You can't just stroll out of a fight!\nIf you wish to leave a fight, you must FLEE in a direction")
        # if objects[32].iscarrby(player) and players[25].location = player.location and player[25].name:
        #     raise GoError("<c>The Golem</c> bars the doorway!")
        # if chkcrip():
        #     return
        room = Location.search(self.location)
        new_room_id = room.exits(direction)
        if new_room_id > -2000 and new_room_id < -999:
            door = Door(new_room_id)
            new_room_id = door.location

        new_room = Location.search(new_room_id)
        self.on_go(new_room, direction)

        block = "<s user=\"%s\">%s has gone %s %s.\n</s>" % (
            self.player.id,
            self.name,
            EXITS[direction],
            self.out_ms
        )
        self.sendsys(self, -10000, text=block)

        self.location = new_room_id

        block = "<s user=\"%s\">%s %s\n</s>" % (
            self.player.id,
            self.name,
            self.in_ms
        )
        self.sendsys(self, -10000, text=block)

        self.trapch(self.location)

    def quit(self):
        # if isforce:
        #     raise Exception("You can't be forced to do that")
        self.rte()
        self.world.openworld()

        if self.in_fight:
            raise Exception("Not in the middle of a fight!")

        self.buff.bprintf("Ok")

        xx = "%s has left the game\n" % (self.name)
        self.sendsys(self, -10000, text=xx)

        xx = "[ Quitting Game : %s ]\n" % (self.name)
        self.sendsys(self, -10113, 0, text=xx)

        self.dumpitems()
        self.player.strength = -1
        self.player.delete()
        self.world.closeworld()
        self.curmode = 0
        self.location = 0
        self.person.saveme(self, zapped=self.zapped)
        # raise Crapup("Goodbye")

    # Events
    def on_go(self, location=None, direction=0):
        if location is None:
            return
        if self.has_blocking_figure(direction, location):
            raise GoError("<p>The Figure</p> holds you back\n<p>The Figure</p> says 'Only true sorcerors may pass'\n")
        location.on_go(self.player, direction)

    @property
    def is_shielded(self):
        for o in [
            Item(id=113),
            Item(id=114),
            Item(id=89),
        ]:
            if o.iswornby(self.player):
                return True
        return False

    @property
    def is_sorceror(self):
        for o in [
            Item(id=101),
            Item(id=102),
            Item(id=103),
        ]:
            if o.iswornby(self.player):
                return True
        return False

    def has_blocking_figure(self, direction, room):
        if direction != 2:
            return False
        i = Player.query.fpbns("figure")
        if i is None:
            return False
        if i == self.player:
            return False
        if room.id != self.location:
            return False
        if self.is_sorceror:
            return False
        return True
