"""
Fast File Controller v0.1
"""
# from global_vars import logger
# from blib import sec_read, sec_write
from .exceptions import Crapup
from ..models import Message
from ..models.player import Player, PINIT


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


class World():
    NOBS = 194
    NUSERS = 49
    # ???
    maxu = 255

    def __init__(self):
        self.players = []  # [None] * self.NUSERS  # ublock
        self.filrf = None
        self.numobs = self.NOBS
        self.objects = []  # [None] * self.NOBS  # objinfo

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

    @property
    def is_full(self):
        return len(Player.query.all()) > self.maxu

    @property
    def is_need_cleaning(self):
        return (Message.query.findend() - Message.query.findfirst()) >= 199

    def put_player(self, user):
        """
        PutMeOn
        """
        user.iamon = False
        self.openworld()

        if Player.query.fpbn(user.model.username):
            raise AlreadyOnMud()

        if self.is_full:
            raise MudFull()

        player = Player(user=user.model)
        player.puton(user)

        user.iamon = True
        return player

    def dumpstuff(self, user, location):
        for b in self.objects:
            if b.iscarrby(user):
                b.location = location
                b.carrf = 0

    def reset_objects(self):
        """
        Load objinfo
        """
        # b = openlock(RESET_DATA, "r")
        # objinfo = b.sec_read(0, 4 * numobs)
        # b.fcloselock()
        pass

    def reset_players(self):
        for p in Player.query.all():
            p.delete()

        for id, c in enumerate(PINIT):
            p = Player.init_data(id, c)
            p.save()

    def reset(self):
        self.reset_objects()

        # Write reset time
        # i = time()
        # a = fopen(RESET_T, "w")
        # a.fprintf("Last Reset At %s\n" % (ctime(i)))
        # a.fclose()
        # a = fopen(RESET_N, "w")
        # a.fprintf("%ld\n" % (i))
        # a.fclose(a)

        self.reset_players()
