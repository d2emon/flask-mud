"""

 Object structure

 Name,
 Long Text 1
 Long Text 2
 Long Text 3
 Long Text 4
 statusmax
 Value
 flags (0=Normal 1+flannel)

"""
# from global_vars import logger


class Item():
    def __init__(self):
        # Objects
        self.item_id = 0
        self.name = ""
        self.desc = []  # longt
        self.flannel = 0
        self.max_state = 0
        self.value = 0

        # Bits
        self.is_dest = False  # 0

        # Objinfo
        self.loc = None  # 0
        self.state = 0  # 1
        self.carrf = 0  # 3

    @classmethod
    def all(cls):
        return [cls() for i in range(10)]

    @classmethod
    def at_location(cls, location_id, **kwargs):
        """
        lojal2
        """
        # self.state <= 3:
        # len(o.desc) > o.state:
        include_destroyed = kwargs.get('include_destroyed', False)
        flannel = kwargs.get('flannel')
        state = kwargs.get('state')

        objects = cls.all()
        for id, o in enumerate(objects):
            o.set_here(location_id, id=id, carrf=0, **kwargs)
        return objects

    @classmethod
    def at_player(cls, player_id, **kwargs):
        """
        lojal2
        """
        # self.state <= 3:
        # len(o.desc) > o.state:
        include_destroyed = kwargs.get('include_destroyed', False)
        flannel = kwargs.get('flannel')
        state = kwargs.get('state')

        objects = cls.all()
        for id, o in enumerate(objects):
            o.set_here(player_id, id=id, carrf=1, **kwargs)
            # carrf in (1, 2)

            # o_txt = c.short_name(user, debug_mode=debug_mode)
        return objects

    def iswornby(self, user):
        return self.iscarrby(user) and self.carrf == 2

    def ishere(self, location, include_destroyed=False):
        if self.is_dest and not include_destroyed:
            return False
        if self.carrf == 1:
            return False
        if self.loc != location:
            return False
        return True

    def set_here(self, location, **kwargs):
        id = kwargs.get('id', 0)
        include_destroyed = kwargs.get('include_destroyed', False)
        state = kwargs.get('state')
        flannel = kwargs.get('flannel')
        carrf = kwargs.get('carrf')

        if include_destroyed:
            destroyed = (id % 3) == 1
        else:
            destroyed = False

        self.item_id = id
        self.name = "Item %d" % (id)
        self.desc.append("Item %d description" % (id))
        self.carrf = carrf  # self.carrf != 1
        self.loc = location
        if destroyed:
            self.is_dest = True
        else:
            self.is_dest = False

        if flannel is not None:
            self.flannel = flannel
        if state is not None:
            self.state = state

    def oplong(self, debug_mode=False):
        if len(self.desc) <= self.state:
            return "ERROR"
        desc = self.desc[self.state]
        if debug_mode:
            desc = "{%s} %s" % (self.item_id, desc)
        return desc

    def iscarrby(self, user, include_destroyed=False):
        if self.is_dest and not include_destroyed:
            return False
        if self.carrf != 1 and self.carrf != 2:
            return False
        if self.loc != user:
            return False
        return True

    def iscontin(self, o2, user):
        if self.carrf != 3:
            return False
        if self.loc != o2:
            return False
        if user.person.level < 10 and self.is_dest:
            return False
        return True

    def short_name(self, owner=None, debug_mode=False):
        res = self.name
        if debug_mode:
            res += "{%-3s}" % (str(self.item_id))
        if self.iswornby(owner):
            res += " <worn>"
        if self.is_dest:
            res = "(%s)" % (res)
        return res


"""
#define OBMUL 8
#include <stdio.h>

extern FILE *openlock();
extern FILE *openworld();
extern char * oname();
extern char * pname();
"""


def inventory():
    """"
    {
    extern long mynum;
   bprintf("You are carrying\n");
    lobjsat(mynum);
    }
    """


"""
 Objinfo

 Loc
 Status
 Stamina
 Flag 1=carr 0=here
"""


"""
fobnsys(nam,ctrl,ct_inf)
char *nam;
long ctrl,ct_inf;
{
    extern char wd_it[];
    extern long mynum;
    long a;
    long l1[32],l2[32];
    extern char wordbuf[];
    strcpy(l1,nam);lowercase(l1);
    a=0;
if(!strcmp(l1,"red")) {brkword();return(4);}
if(!strcmp(l1,"blue")) {brkword();return(5);}
if(!strcmp(l1,"green")) {brkword();return(6);}
    while(a<NOBS)
       {
       strcpy(l2,oname(a));lowercase(l2);
       if(!strcmp(l1,l2))
          {
          strcpy(wd_it,nam);
          switch(ctrl)
             {
             case 0:
                return(a);
             case 1:/* Patch for shields */
                if((a==112)&&(iscarrby(113,mynum))) return(113);
                if((a==112)&&(iscarrby(114,mynum))) return(114);
                if(isavl(a)) return(a);
                break;
             case 2:
                if(iscarrby(a,mynum)) return(a);
                break;
             case 3:
                if(iscarrby(a,ct_inf)) return(a);
                break
                ;
             case 4:
                if(ishere(a)) return(a);
                break;
             case 5:
                if(iscontin(a,ct_inf)) return(a);
                break;
             default:
                return(a);
                }
          }
       a++;
       }
    return(-1);
    }

 fobn(word)
 char *word;
    {
long x;
x=fobna(word);
if(x!=-1) return(x);
    return(fobnsys(word,0,0));
    }

 fobna(word)
 char *word;
    {
    return(fobnsys(word,1,0));
    }

 fobnin(word,ct)
 char *word;
 long ct;
 {
return(fobnsys(word,5,ct));
 }

 fobnc(word)
 char *word;
    {
    return(fobnsys(word,2,0));
    }

 fobncb(word,by)
 char *word;
    {
    return(fobnsys(word,3,by));
    }

 fobnh(word)
 char *word;
    {
    return(fobnsys(word,4,0));
    }

 getobj()
    {
    extern long mynum;
    extern char globme[];
    extern long curch;
    extern char wordbuf[];
    long a,b;
    long i;
    long des_inf= -1;
    extern long stp;
    char bf[256];
    if(brkword()==-1)
       {
      bprintf("Get what ?\n");
       return;
       }
    a=fobnh(wordbuf);
    /* Hold */
    i=stp;
    strcpy(bf,wordbuf);
    if((brkword()!=-1)&&((strcmp(wordbuf,"from")==0)||(strcmp(wordbuf,"out")==0)))
    {
        if(brkword()==-1)
        {
            bprintf("From what ?\n");
            return;
        }
        des_inf=fobna(wordbuf);
        if(des_inf==-1)
        {
            bprintf("You can't take things from that - it's not here\n");
            return;
        }
        a=fobnin(bf,des_inf);
    }
    stp=i;
    if(a==-1)
       {
      bprintf("That is not here.\n");
       return;
       }
if((a==112)&&(des_inf==-1))
{
if(isdest(113)) a=113;
else if(isdest(114)) a=114;
if((a==113)||(a==114)) oclrbit(a,0);
else bprintf("The shields are all to firmly secured to the walls\n");
}
    if(obflannel(a)==1)
       {
      bprintf("You can't take that!\n");
       return;
       }
if(dragget()) return;
    if(!cancarry(mynum))
       {
      bprintf("You can't carry any more\n");
       return;
}
if((a==32)&&(state(a)==1)&&(ptothlp(mynum)==-1))
{
bprintf("Its too well embedded to shift alone.\n");
return;
}
setoloc(a,mynum,1);
    sprintf(bf,"\001D%s\001\001c takes the %s\n\001",globme,oname(a));
   bprintf("Ok...\n");
    sendsys(globme,globme,-10000,curch,bf);
if(otstbit(a,12)) setstate(a,0);
if(curch==-1081)
{
setstate(20,1);
bprintf("The door clicks shut....\n");
}
}

 dropitem()
    {
    extern long mynum,curch;
    extern char wordbuf[],globme[];
    extern long my_sco;
    long a,b,bf[32];
    extern long my_lev;
    if(brkword()==-1)
       {
      bprintf("Drop what ?\n");
       return;
       }
    a=fobnc(wordbuf);
    if(a==-1)
       {
      bprintf("You are not carrying that.\n");
       return;
       }

if((my_lev<10)&&(a==32))
{
bprintf("You can't let go of it!\n");
return;
}
    setoloc(a,curch,0);
   bprintf("OK..\n");
    sprintf(bf,"\001D%s\001\001c drops the %s.\n\n\001",globme,wordbuf);
    sendsys(globme,globme,-10000,curch,bf);
    if((curch!=-183)&&(curch!=-5))return;
   sprintf(bf,"The %s disappears into the bottomless pit.\n",wordbuf);
   bprintf("It disappears down into the bottomless pit.....\n");
    sendsys(globme,globme,-10000,curch,bf);
    my_sco+=(tscale()*obaseval(a))/5;
    calibme();
setoloc(a,-6,0);
    }
"""


"""
 whocom()
    {
    long a;
    extern long my_lev;
    long bas;
    a=0;
    bas=16;
    if(my_lev>9)
       {
      bprintf("Players\n");
       bas=48;
       }
    while(a<bas)
       {
       if(a==16)bprintf("----------\nMobiles\n");
       if(!strlen(pname(a))) goto npas;
       dispuser(a);
       npas:a++;
       }
   bprintf("\n");
    }

 dispuser(ubase)
    {
extern long my_lev;
    if(pstr(ubase)<0) return; /* On  Non game mode */
    if(pvis(ubase)>my_lev) return;
if(pvis(ubase)) bprintf("(");
   bprintf("%s ",pname(ubase));
    disl4(plev(ubase),psex(ubase));
if(pvis(ubase)) bprintf(")");
if(ppos(ubase)==-2) bprintf(" [Absent From Reality]");
bprintf("\n");
    }

 disle3(n,s)
    {
    disl4(n,s);
   bprintf("\n");
    }
    """


def usercom():
    """
    {
    extern long my_lev;
    long a;
    a=my_lev;
    my_lev=0;
    whocom();
    my_lev=a;
    }
    """

    """
 isavl(ob)
    {
    extern long mynum;
    if(ishere(ob)) return(1);
    return(iscarrby(ob,mynum));
    }

 ospare(ob)
    {
    return(otstbit(ob,0)?-1:0);
    }

ocreate(ob)
{
oclrbit(ob,0);
}

osetbit(ob,x)
{
extern long objinfo[];
bit_set(&(objinfo[4*ob+2]),x);
}
oclearbit(ob,x)
{
extern long objinfo[];
bit_clear(&(objinfo[4*ob+2]),x);
}
otstbit(ob,x)
{
extern long objinfo[];
return(bit_fetch(objinfo[4*ob+2],x));
}
osetbyte(o,x,y)
{
extern long objinfo[];
byte_put(&(objinfo[4*o+2]),x,y);
}
obyte(o,x)
{
extern long objinfo[];
return(byte_fetch(objinfo[4*o+2],x));
}
ohany(mask)
long mask;
{
extern long numobs;
auto a;
extern long mynum;
extern long objinfo[];
a=0;
mask=mask<<16;
while(a<numobs)
{
if(((iscarrby(a,mynum))||(ishere(a,mynum)))&&(objinfo[4*a+2]&mask))return(1);
a++;
}
return(0);
}
    """


class Weather(Item):
    CLIMATES = [
        range(5),
        [n % 2 for n in range(5)],
        [0, 3, 4, 3, 4],
    ]

    def __init__(self, climate_id=0):
        Item.__init__(self)
        self.state = 1
        self.climate_id = climate_id
        self.climate = self.CLIMATES[climate_id]

    @property
    def climate_state(self):
        return self.climate[self.state]

    def oplong(self, debug=False):
        """
        showwthr
        """
        if self.climate_state == 1:
            if self.climate_id == 1:
                res = ""
                res += "It is raining, a gentle mist of rain, which sticks to everything around\n"
                res += "you making it glisten and shine. High in the skies above you is a rainbow\n"
                return res
            else:
                return "<c>It is raining\n</c>"
        if self.climate_state == 2:
            return "<c>The skies are dark and stormy\n</c>"
        if self.climate_state == 3:
            return "<c>It is snowing</c>\n"
        if self.climate_state == 4:
            return "<c>A blizzard is howling around you</c>\n"
        return "None"
