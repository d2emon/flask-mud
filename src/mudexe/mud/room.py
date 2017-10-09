from global_vars import logger


class Room():
    def __init__(self, room_id):
        self.room_id = room_id
        self.deathroom = False
        self.nobr = False
        self.description = ""

    # ???
    def showname(self):
        logger().debug("<<< showname(%d)", self)

    # ???
    def openroom(self, mode="r"):
        logger().debug("<<< openroom(%s, %s)", self, mode)
        return None

    # ???
    def closeroom(self):
        logger().debug("<<< fclose(%s)", self)

    # ???
    def lodex(self):
        logger().debug("<<< lodex(%s)", self)

    # ???
    def showwthr(self):
        logger().debug("<<< showwthr()")

    # ???
    def getstr(self):
        logger().debug("<<< getstr(%s)", self)
        return None

    # ???
    def isdark(self):
        logger().debug("<<< is_dark()")
        return True

    def lisobs(self, user):
        res = ""
        res += self.lojal2(1, user)
        res += self.showwthr()
        res += self.lojal2(0, user)

    def lojal2(self, n, user):
        res = ""
        objects = []
        for a in objects:
            res += a.lojal2(n, user)
        return res

    def lispeople(self, user=None):
        res = ""
        players = []
        for a in players:
            res += a.showto(user)
        return res

    def load(self, un1):
        if un1 is None:
            self.deathroom = False
            self.nobr = False
            self.description = "\nYou are on channel %s\n" % (self)
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

    def cansee(self, user):
        return not self.isdark() and not user.ail_blind

    def look(self, user):
        res = ""
        un1 = self.openroom()
        self.load(un1)
        if self.nobr:
            user.brmode = False
        if self.deathroom:
            user.ail_blind = False
        if self.isdark():
            res += "It is dark\n"
        if not user.ail_blind and not user.brmode:
            res += self.description

        self.closeroom()
        user.world.openworld()
        if self.cansee(user):
            res += self.lisobs(user)
            if user.curmode:
                res += self.lispeople(user)
        return res
