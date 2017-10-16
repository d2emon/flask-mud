from app import db
from sqlalchemy import desc
from global_vars import logger


from ..objsys import Item


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
    objects = [Item()] * 5

    def openroom(self, mode="r"):
        # blob = "%s%d" % (ROOMS, -n)
        # x = fopen(blob, mod)
        # return x
        return None

    # ???
    def closeroom(self):
        logger().debug("<<< fclose(%s)", self)

    # ???
    def showwthr(self):
        logger().debug("<<< showwthr()")
        wthr = Item()
        wthr.desc.append("WEATHER")
        return wthr

    # ???
    def getstr(self):
        logger().debug("<<< getstr(%s)", self)
        return None

    # ???
    def isdark(self):
        logger().debug("<<< is_dark()")
        return False

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
        from . import Player

        return Player.query.all()

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

    def no_file(self):
        self.deathroom = False
        self.nobr = False
        self.description = "\nYou are on channel %s\n" % (self.id)
        return

    def showname(self, user):
        res = str(self.name)
        if user.person.level > 9999:
            res += "[ %s ]" % (self)
        user.wd_there = self.name
        res += "\n"
        return res

    def list_objects(self, user):
        """
        lisobs
        """
        res = []
        res += self.objects_at(1, include_destroyed=user.person.is_wizzard, debug=user.debug_mode, user=user)
        res += [self.showwthr(), ]
        res += self.objects_at(0, include_destroyed=user.person.is_wizzard, debug=user.debug_mode, user=user)
        return res

    def objects_at(self, flannel, **kwargs):
        """
        lojal2
        """
        include_destroyed = kwargs.get('include_destroyed', False)
        debug = kwargs.get('debug', False)
        user = kwargs.get('user')

        res = []
        for a in self.objects:
            a.desc.append("Item description")
            a.loc = self.id
            a.flannel = flannel
            if a.flannel != flannel:
                continue
            desc = a.lojal2(
                self.id,
                include_destroyed=include_destroyed,
                debug_mode=debug,
            )
            if desc:
                res.append(desc)
                if user is not None:
                    user.wd_it = a.name
        return res

    def list_people(self, user=None):
        """
        lispeople
        """
        res = []
        from . import SEX_FEMALE

        for a in self.players:
            # res.append(a.showto(user))
            u = a.showto(user)
            if u:
                res.append(u)
                if u.sex == SEX_FEMALE:
                    user.wd_her = u.name
                else:
                    user.wd_him = u.name
        return res

    def cansee(self, user):
        return not self.isdark() and not user.ail_blind

    def look(self, user):
        if self.isdark():
            self.closeroom()
            user.world.openworld()
            return "It is dark\n"
        self.closeroom()
        user.world.openworld()
        return self.description

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
        objects = []
        for c in objects:
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
