"""
Fast File Controller v0.1
"""
from global_vars import logger
# from blib import sec_read, sec_write
from .exceptions import Crapup
from ..models import Player


class MudUnaviable(Crapup):
    """
    crapup("Sorry AberMUD is currently unavailable")
    crapup("Cannot find World file")
    """
    def __init__(self):
        Crapup.__init__(self, "Sorry AberMUD is currently unavailable")


class MudFull(Exception):
    """
    print("\nSorry AberMUD is full at the moment")
    """
    def __str__(self):
        return "Sorry AberMUD is full at the moment"


class AlreadyOnMud(Crapup):
    def __init__(self):
        Crapup.__init__(self, "You are already on the system - you may only be on once at a time")


# ???
def seeplayer(p):
    logger().debug("<<< seeplayer(%s)", p)
    return True


class World():
    NOBS = 194
    NUSERS = 49
    # ???
    maxu = 255

    def __init__(self):
        self.players = [None] * self.NUSERS  # ublock
        self.filrf = None
        self.numobs = self.NOBS
        self.objinfo = [None] * self.NOBS

        self.usr_start = 350
        self.usr_len = 16
        self.usr_count = 48
        self.obj_start = 400
        self.obj_len = 4
        self.obj_count = self.numobs
        self.msg_len = 128
        self.msg_count = 1

    def openworld(self):
        print("G" + "<" * 150 + "DB")
        if self.filrf is not None:
            return self.filrf
        # self.filrf = openlock("/usr/tmp/-iy7AM", "r+")
        self.filrf = 1
        if self.filrf is None:
            raise MudUnaviable()
        """
        sec_read(
            self.filrf,
            self.objinfo,
            self.obj_start,
            self.obj_len * self.obj_count
        )
        sec_read(
            self.filrf,
            self.ublock,
            self.usr_start,
            self.usr_len * self.usr_count
        )
        """
        return self.filrf

    def closeworld(self):
        print("G" + ">" * 150 + "DB")
        if self.filrf is None:
            return
        # player.save()
        """
        sec_write(
            self.filrf,
            self.objinfo,
            self.obj_start,
            self.obj_len * self.obj_count
        )
        sec_write(
            self.filrf,
            self.ublock,
            self.usr_start,
            self.usr_len * self.usr_count
        )
        """
        # fcloselock(self.filrf)
        self.filrf = None

    def find_empty(self, name):
        if self.fpbn(name):
            raise AlreadyOnMud()
        if len(Player.query.all()) > self.maxu:
            raise MudFull()

    def fpbn(self, name):
        # extern char wd_them[],wd_him[],wd_her[],wd_it[];
        s = self.fpbns(name)
        if s is None:
            return s
        if not seeplayer(s):
            return None
        return s

    def fpbns(self, name):
        return Player.query.filter_by(name=name).first()

    def dumpstuff(self, n, loc):
        for b in self.objects:
            if b.iscarrby(n):
                b.loc = (loc, 0)
