from global_vars import logger
from ..gamego import crapup
from .textbuff import TextBuffer


# ???
def eorte():
    logger().debug("<<< eorte()")


# ???
def gamrcv(msg):
    logger().debug("<<< gamrcv(%s)", msg)


# ???
def initme():
    logger().debug("<<< initme()")


# ???
def randperc():
    logger().debug("<<< randperc()")
    return 25


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
    # ???
    debug_mode = True
    # ???
    rdes = 0
    # ???
    vdes = 0
    # ???
    tdes = 0
    # ???
    my_str = 0
    # ???
    my_lev = 0
    # ???
    my_sex = 0

    def __init__(self, name):
        self.name = name  # globme
        self.i_setup = False
        self.cms = -1
        self.mynum = 0
        self.curch = 0
        self.iamon = False
        self.lasup = 0
        self.curmode = 0
        # Other
        self.player = PlayerData()
        self.buff = TextBuffer()
        self.world = None

    @property
    def fullname(self):
        if self.name == "Phantom":
            return "The %s" % (self.name)
        else:
            return self.name

    # ???
    def cuserid(self):
        logger().debug("<<< cuserid(%s)", self)
        return 0

    def putmeon(self, world=None):
        self.iamon = False
        world.openworld()
        f = False
        if self.fpbn() is not None:
            crapup("You are already on the system - you may only be on once at a time")
        self.mynum = world.find_empty(self.player)
        self.world = world

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
        self.world.openworld()
        if self.cms == -1:
            self.cms = self.world.findend()
        too = self.world.findend()
        ct = self.cms
        # while ct < too:
        # while ct >= too:
        for ct in range(self.cms, too):
            msg = self.world.readmsg(ct)
            self.mstoout(msg)
        self.cms = ct
        self.update()
        eorte()
        self.rdes = 0
        self.tdes = 0
        self.vdes = 0

    def fpbn(self):
        logger().debug("<<< fpbn(%s)", self.name)
        return None

    def update(self):
        xp = self.cms - self.lasup
        if xp < 0:
            xp = -xp
        if xp < 10:
            return
        self.world.openworld()
        self.player.pos = self.cms
        self.lasup = self.cms

    def mstoout(self, msg):
        # Print appropriate stuff from data block
        if self.debug_mode:
            self.buff.bprintf("\n<%d>" % (msg.msg_code))
        if msg.msg_code < -3:
            self.sysctrl(msg)
        else:
            self.buff.bprintf(msg.text)

    def sysctrl(self, msg):
        gamrcv(msg)

    def start_game(self):
        self.curmode = 1
        rooms = [-5, -183]
        initme()
        self.world.openworld()
        self.player.strength = self.my_str
        self.player.lev = self.my_lev
        if self.my_lev < 10000:
            self.player.vis = 0
        else:
            self.player.vis = -1
        self.player.sexall = self.my_sex
        self.player.helping = -1
        us = self.cuserid()
        xy = "\001s%s\001%s  has entered the game\n\001" % (self.name, self.name)
        xx = "\001s%s\001[ %s  has entered the game ]\n\001" % (self.name, self.name)
        self.sendsys(self, -10113, text=xx)
        self.rte()
        if randperc() > 50:
            room = rooms[0]
        else:
            room = rooms[1]
        self.curch = room
        self.trapch(room)
        self.sendsys(self, -10000, text=xy)

    # ???
    def sendsys(self, to_user, msg_code, channel=None, text=""):
        if channel is None:
            channel = self.curch
        logger().debug("<<< sendsys(%s, %s, %s, %s, %s)", self, to_user, msg_code, channel, text)

    def trapch(self, chan):
        self.world.openworld()
        self.player.loc = chan
        self.lookin()

    def lookin(self, room=None):
        if room is None:
            room = self.curch
        """
 long room; /* Lords ???? */
    {
    extern char globme[];
    FILE *un1,un2;
    char str[128];
    long xxx;
    extern long brmode;
    extern long curmode;
    extern long ail_blind;
    long ct;
    extern long my_lev;
    closeworld();
    if(ail_blind)
    {
        bprintf("You are blind... you can't see a thing!\n");
    }
    if(my_lev>9) showname(room);
    un1=openroom(room,"r");
    if (un1!=NULL)
    {
xx1:   xxx=0;
       lodex(un1);
       if(isdark())
       {
           fclose(un1);
           bprintf("It is dark\n");
           openworld();
           onlook();
           return;
        }
       while(getstr(un1,str)!=0)
          {
          if(!strcmp(str,"#DIE"))
             {
             if(ail_blind) {rewind(un1);ail_blind=0;goto xx1;}
             if(my_lev>9)bprintf("<DEATH ROOM>\n");
             else
                {
                loseme(globme);
                crapup("bye bye.....\n");
                }
             }
          else
{
if(!strcmp(str,"#NOBR")) brmode=0;
else
             if((!ail_blind)&&(!xxx))bprintf("%s\n",str);
          xxx=brmode;
}
          }
       }
    else
       bprintf("\nYou are on channel %d\n",room);
    fclose(un1);
    openworld();
    if(!ail_blind)
    {
        lisobs();
        if(curmode==1) lispeople();
    }
    bprintf("\n");
    onlook();
    }
        """

    def loseme(self):
        # extern long iamon;
        # extern long mynum;
        # extern long zapped;
        # char bk[128];
        # extern char globme[];
        # FILE *unit;
        # sig_aloff()  # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.i_setup = False
        self.world.openworld()
        # dumpitems()
        if self.player.vis < 10000:
            bk = "%s has departed from AberMUDII\n" % (self.name)
            self.sendsys(self, -10113, 0, bk)
        self.world.players[self.mynum] = None
        self.world.close()
        # if not zapped:
        #     saveme()
        # chksnp()
