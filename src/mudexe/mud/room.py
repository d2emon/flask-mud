from global_vars import logger
from ..objsys import Item
from ..models import Player, SEX_FEMALE


class Zone():
    """
    Zone based name generator
    """
    def __init__(self, name="", min_loc=0, max_loc=99999):
        self.name = name
        self.min_loc = min_loc
        self.max_loc = max_loc

    def roomname(self, room_id):
        return "%s%d" % (self.name, room_id)


class Room():
    def __init__(self, room_id):
        self.room_id = room_id
        self.deathroom = False
        self.nobr = False
        self.description = ""
        self.ex_dat = [0] * 7
        self.zoname = [
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
    def name(self):
        zone, room_id = self.findzone()
        return zone.roomname(room_id)

    def openroom(self, mode="r"):
        # blob = "%s%d" % (ROOMS, -n)
        # x = fopen(blob, mod)
        # return x
        return None

    def load(self, un1=None):
        # un1 = self.openroom()
        if un1 is None:
            self.deathroom = False
            self.nobr = False
            self.description = "\nYou are on channel %s\n" % (self.room_id)
            return
        self.lodex()
        s = self.getstr()
        while s is not None:
            if s == "#DIE":
                self.deathroom = True
            else:
                if s == "#NOBR":
                    self.nobr = True
                else:
                    self.description += "%s\n" % (s)
            s = self.getstr()

    def findzone(self, room_id=None):
        if room_id is None:
            room_id = -self.room_id

        for z in self.zoname:
            if room_id in range(z.min_loc, z.max_loc):
                return z, room_id - z.min_loc
        return Zone("TCHAN"), 0

    def lodex(self):
        for a in range(7):
            self.ex_dat[a] = 0

    def showname(self, user):
        # extern char wd_there[];
        res = self.name
        if user.person.level > 9999:
            res += "[ %s ]" % (self)
        zone, room_id = self.findzone()
        wd_there = "%s %d" % (zone, room_id)
        res += "\n"
        return res

    def lisobs(self, user):
        res = []
        res += self.lojal2(1, user)
        res += [self.showwthr(), ]
        res += self.lojal2(0, user)
        return res

    def lojal2(self, flannel, user):
        res = []
        objects = [Item()] * 5
        for a in objects:
            a.desc.append("Item description")
            a.loc = self.room_id
            a.flannel = flannel
            if a.flannel != flannel:
                continue
            desc = a.lojal2(
                self.room_id,
                include_destroyed=user.person.is_wizzard,
                debug_mode=user.debug_mode,
            )
            if desc:
                res.append(desc)
                user.wd_it = a.name
        return res

    def lispeople(self, user=None):
        res = []
        players = Player.query.all()
        for a in players:
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
        self.load()
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
