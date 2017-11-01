from app import db
# from global_vars import logger


from .item import Item, Weather
from .player import Player


from ..mud.exceptions import GoError


class Zone():
    """
    Zone based name generator
    """
    def __init__(self, name="", min_loc=0, max_loc=99999):
        self.name = name
        self.min_loc = min_loc
        self.max_loc = max_loc

    def room_id(self, room_id):
        return room_id - self.min_loc + 1

    def roomname(self, room_id):
        return "%s%d" % (self.name, room_id)

    def __str__(self):
        return self.name


ZONES = [
    Zone("LIMBO", 0, 1),
    Zone("WSTORE", 1, 2),
    Zone("HOME", 2, 4),
    Zone("START", 4, 5),
    Zone("PIT", 5, 6),
    Zone("WIZROOM", 6, 19),
    Zone("DEAD", 19, 99),
    Zone("BLIZZARD", 99, 299),
    Zone("CAVE", 299, 399),
    Zone("LABRNTH", 399, 499),
    Zone("FOREST", 499, 599),
    Zone("VALLEY", 599, 699),
    Zone("MOOR", 699, 799),
    Zone("ISLAND", 799, 899),
    Zone("SEA", 899, 999),
    Zone("RIVER", 999, 1049),
    Zone("CASTLE", 1049, 1069),
    Zone("TOWER", 1069, 1099),
    Zone("HUT", 1099, 1101),
    Zone("TREEHOUSE", 1101, 1105),
    Zone("QUARRY", 1105, 2199),
    Zone("LEDGE", 2199, 2299),
    Zone("INTREE", 2299, 2499),
    Zone("WASTE", 2499, 99999),
]


STARTING_LOCATIONS = [5, 183]


class Location(db.Model):
    """
    Create a Location table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), info={'label': "Name"})  # 0
    north = db.Column(db.Integer, default=0, info={'label': "North"})
    east = db.Column(db.Integer, default=0, info={'label': "East"})
    south = db.Column(db.Integer, default=0, info={'label': "South"})
    west = db.Column(db.Integer, default=0, info={'label': "West"})
    up = db.Column(db.Integer, default=0, info={'label': "Up"})
    down = db.Column(db.Integer, default=0, info={'label': "Down"})
    deathroom = db.Column(db.Boolean, default=False, info={'label': "Death room"})
    nobr = db.Column(db.Boolean, default=False, info={'label': "No brief"})
    description = db.Column(db.UnicodeText(), info={'label': "Description"})

    __zone = None

    def openroom(self, mode="r"):
        # blob = "%s%d" % (ROOMS, -n)
        # x = fopen(blob, mod)
        # return x
        return None

    def closeroom(self):
        # logger().debug("<<< fclose(%s)", self)
        return None

    @property
    def zone(self):
        if self.__zone is not None:
            return self.__zone

        for z in ZONES:
            if self.id in range(z.min_loc, z.max_loc):
                self.__zone = z
                return self.__zone

        self.__zone = Zone("TCHAN")
        return self.__zone

    @property
    def players(self):
        return Player.query.all()

    @property
    def objects(self):
        return Item.at_location(self.id)

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load_exits(self, data):
        """
        lodex
        """
        # for a in range(len(DIRECTIONS)):
        #     self.ex_dat[a] = 0
        self.north = -int(data[0])
        self.east = -int(data[1])
        self.south = -int(data[2])
        self.west = -int(data[3])
        self.up = -int(data[4])
        self.down = -int(data[5])

    def load_from_file(self, filename):
        with open(filename) as f:
            data = f.readlines()
            self.load_exits(data)

            self.name = "%s %d" % (self.zone, self.zone.room_id(self.id))
            # self.name = data[6]
            self.nobr = False
            self.deathroom = False
            self.description = ""
            for s in data[6:]:
                if s.strip() == "#DIE":
                    self.deathroom = True
                elif s.strip() == "#NOBR":
                    self.nobr = True
                else:
                    self.description += s
                self.getstr()

    @classmethod
    def search(cls, id=0):
        l = cls.query.get(id)

        if l is not None:
            return l

        l = cls(id=id)
        l.deathroom = False
        l.nobr = False
        l.description = "\nYou are on channel %s\n" % (id)
        return l

    def list_objects(self, user):
        """
        lisobs
        """
        weather = self.weather
        res = []
        res += self.objects_at(
            flannel=1,
            include_destroyed=user.person.is_wizzard,
            debug=user.debug_mode,
            user=user
        )
        if weather:
            res.append(weather)
        res += self.objects_at(
            flannel=0,
            include_destroyed=user.person.is_wizzard,
            debug=user.debug_mode,
            user=user
        )
        return res

    def objects_at(self, **kwargs):
        """
        lojal2
        """
        user = kwargs.get('user')

        res = Item.at_location(self.id, **kwargs)
        if not res:
            return res

        if user is not None:
            user.wd_it = res[-1].name
        return res

    def list_people(self, user=None):
        """
        lispeople
        """
        res = Player.query.visible_to(user).all()
        if not res:
            return res

        if user is not None:
            user.wd_people(res[-1])
        return res

    def lobjsat(self, user):
        self.aobjsat(1, user)

    def aobjsat(self, mode, user):
        """
        Carried Loc !
        """
        res = ""
        d = 0
        e = False
        f = 0
        for c in self.objects:
            if mode == 1 and not c.iscarrby(self):
                continue
            if mode == 3 and not c.iscontin(self):
                continue
            e = True
            o_txt = c.name
            if user.debug_mode:
                x = "%d" % (c.id)
                o_txt += "{%-3s}" % (x)
            if c.iswornby(self):
                o_txt += " <worn>"
            if c.is_dest:
                o_txt = "(%s)" % (o_txt)
            o_txt += " "
            f += len(o_txt)
            if f > 79:
                f = 0
                res += "\n"
            res += o_txt
            d += 4
        if not e:
            return "Nothing\n"
        res += "\n"
        return res

    @property
    def weather(self):
        if not self.outdoors:
            return None
        return Weather(self.climate)

    @property
    def outdoors(self):
        if self.id in [100, 101, 102]:
            return True
        # elif self.id == 183:
        #     return False
        elif self.id == 170:
            return False
        else:
            if self.id > 168 and self.id < 191:
                return True
            if self.id > 172 and self.id < 181:
                return True
        return False

    @property
    def climate(self):
        if self.id > 178 and self.id < 199:
            return 1
        if self.id >= 100 and self.id <= 178:
            return 2
        return 0

    @property
    def dark(self):
        if self.id == 1100 or self.id == 1101:
            return False
        if self.id >= 1113 and self.id <= 1123:
            return True
        if self.id < 300 or self.id > 399:
            return False
        return True

    @property
    def has_light(self):
        if not self.dark:
            return True

        if Item.light_at_location(self.id) is None:
            return True
        return False

    def on_go(self, user, direction):
        if self.has_intense_heat:
            if not user.shielded:
                raise GoError("The intense heat drives you back")
            else:
                user.buff.bprintf("The shield protects you from the worst of the lava stream's heat")

        if self.id <= 0:
            raise GoError()

    @property
    def has_intense_heat(self):
        return self.id == 139

    def exits(self, exit_id):
        if exit_id == 0:
            return self.north
        elif exit_id == 1:
            return self.east
        elif exit_id == 2:
            return self.south
        elif exit_id == 3:
            return self.west
        elif exit_id == 4:
            return self.up
        elif exit_id == 5:
            return self.down
        return 0
