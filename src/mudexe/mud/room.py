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
        logger().debug("<<< openroom(%d, %s)", self, mode)
        return None

    # ???
    def closeroom(self):
        logger().debug("<<< fclose(%s)", self)

    # ???
    def lodex(self):
        logger().debug("<<< lodex(%s)", self)

    # ???
    def lisobs(self):
        logger().debug("<<< lisobs()")

    # ???
    def lispeople(self):
        logger().debug("<<< lispeople()")

    # ???
    def getstr(self):
        logger().debug("<<< getstr(%s)", self)
        return None

    # ???
    def isdark(self):
        logger().debug("<<< is_dark()")
        return True

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
            res += self.lisobs()
            if user.curmode:
                res += self.lispeople()
        return res
