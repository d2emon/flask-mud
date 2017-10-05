from global_vars import logger
from ..gamego import crapup
from .textbuff import TextBuffer


class PlayerData():
    def load(self, ct):
        self.ct = ct
        self.name = ""
        self.loc = 0
        self.pos = -1
        self.lev = 1
        self.vis = 0
        self.strength = -1
        self.wpn = -1
        self.sex = 0


class User():
    def __init__(self, name):
        self.name = name  # globme
        self.i_setup = False
        self.cms = -1
        self.mynum = 0
        self.curch = 0
        self.iamon = False
        # Other
        self.player = PlayerData()
        self.buff = TextBuffer()

    @property
    def fullname(self):
        if self.name == "Phantom":
            return "The %s" % (self.name)
        else:
            return self.name

    # ???
    def cuserid(self, user):
        logger().debug("<<< cuserid(%s)" % (user, ))
        return 0

    def putmeon(self, world=None):
        self.iamon = False
        world.openworld()
        f = False
        if self.fpbn() is not None:
            crapup("You are already on the system - you may only be on once at a time")
        self.mynum = world.find_empty(self.player)
        self.player.load(self.mynum)
        self.player.name = self.name
        self.player.loc = self.curch
        self.player.pos = -1
        self.player.lev = 1
        self.player.vis = 0
        self.player.strength = -1
        self.player.wpn = -1
        self.player.sex = 0
        self.iamon = True
        return True

    def rte(self):
        """
 char *name;
    {
    extern long cms;
    extern long vdes,tdes,rdes;
    extern FILE *fl_com;
    extern long debug_mode;
    FILE *unit;
    long too,ct,block[128];
    unit=openworld();
    fl_com=unit;
    if (unit==NULL) crapup("AberMUD: FILE_ACCESS : Access failed\n");
    if (cms== -1) cms=findend(unit);
    too=findend(unit);
    ct=cms;
    while(ct<too)
       {
       readmsg(unit,block,ct);
       mstoout(block,name);
       ct++;
       }
    cms=ct;
    update(name);
    eorte();
    rdes=0;tdes=0;vdes=0;
    }
        """

    def fpbn(self):
        logger().debug("<<< fpbn(%s)", self.name)
        return None
