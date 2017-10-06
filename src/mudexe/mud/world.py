"""
Fast File Controller v0.1
"""
from global_vars import logger
# from blib import sec_read, sec_write


class MudUnaviable(Exception):
    """
    crapup("Sorry AberMUD is currently unavailable")
    crapup("Cannot find World file")
    """
    def __str__(self):
        return "Sorry AberMUD is currently unavailable"


class MudFull(Exception):
    """
    print("\nSorry AberMUD is full at the moment")
    """
    def __str__(self):
        return "Sorry AberMUD is full at the moment"


class MudMessage():
    """
    Mud Message
    """
    def __init__(self, msg_code=0, text=""):
        self.msg_code = msg_code
        self.text = text


class World():
    # ???
    maxu = 255
    # ???
    ublock = []
    # ???
    numobs = 16
    # ???
    objinfo = []

    def __init__(self):
        self.players = [None] * self.maxu
        self.filrf = None

        self.usr_start = 350
        self.usr_len = 16
        self.usr_count = 48
        self.obj_start = 400
        self.obj_len = 4
        self.obj_count = self.numobs

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

    def find_empty(self, player):
        for p in range(len(self.players)):
            if self.players[p] is None:
                self.players[p] = player
                return p
        raise MudFull()

    def findstart(self):
        """
    long bk[2];
    sec_read(unit,bk,0,1);
    return(bk[0]);
        """
        logger().debug("<<< findstart()")
        return 0

    def findend(self):
        """
    long bk[3];
    sec_read(unit,bk,0,2);
    return(bk[1]);
        """
        logger().debug("<<< findend()")
        return 0

    def readmsg(self, num):
        # long buff[64],actnum;
        # sec_read(channel,buff,0,64);
        # actnum = num * 2 - buff[0]
        # sec_read(channel,block,actnum,128);
        return MudMessage(-5000, "Test")
