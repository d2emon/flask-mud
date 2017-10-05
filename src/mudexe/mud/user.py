from global_vars import logger
from .textbuff import TextBuffer


class User():
    def __init__(self, name):
        self.name = name  # globme
        self.i_setup = False
        self.cms = -1
        self.mynum = 0
        # Other
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

    def putmeon(self):
        """
 char *name;
    {
    extern long mynum,curch;
    extern long maxu;
    long ct,f;
    FILE *unit;
    extern long iamon;
    iamon=0;
    unit=openworld();
    ct=0;
    f=0;
    if(fpbn(name)!= -1)
       {
       crapup("You are already on the system - you may only be on once at a time");
       }
    while((f==0)&&(ct<maxu))
       {
       if (!strlen(pname(ct))) f=1;
       else
          ct++;
       }
    if(ct==maxu)
       {
       mynum=maxu;
       return;
       }
    strcpy(pname(ct),name);
    setploc(ct,curch);
    setppos(ct,-1);
    setplev(ct,1);
    setpvis(ct,0);
    setpstr(ct,-1);
    setpwpn(ct,-1);
    setpsex(ct,0);
    mynum=ct;
iamon=1;
    }
        """


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
