from global_vars import logger


class MudUnaviable(Exception):
    """
    crapup("Sorry AberMUD is currently unavailable")
    """


class MudFull(Exception):
    """
    print("\nSorry AberMUD is full at the moment")
    """


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

    def __init__(self):
        self.players = [None] * self.maxu

    # ???
    def openworld(self):
        logger().debug("<<< openworld()")
        # raise MudUnaviable()
        return True

    # ???
    def closeworld(self):
        logger().debug("<<< closeworld()")

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
