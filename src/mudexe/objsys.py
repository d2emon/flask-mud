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
from global_vars import logger


class Item():
    # ???
    loc = None
    # ???
    name = ""

    # ???
    def isdest(self):
        logger().debug("<<< isdest(%s)", self)
        return True

    # ???
    def ocarrf(self):
        logger().debug("<<< ocarrf(%s)", self)
        return True

    # ???
    def state(self):
        logger().debug("<<< state(%s)", self)
        return True

    # ???
    def oflannel(self):
        logger().debug("<<< oflannel(%s)", self)
        return True

    # ???
    def olongt(self, state):
        logger().debug("<<< olongt(%s, %s)", self, state)
        return True

    def ishere(self, user):
        if user.person.level < 10 and self.isdest():
            return False
        if self.ocarrf() == 1:
            return False
        if self.loc != user.curch:
            return 0
        return True

    def oplong(self, user):
        if user.debug_mode:
            return "{%d} %s\n" % (self, self.olongt(self.state()))
        if len(self.olongt(self.state())):
            return "%s\n" % (self.olongt(self.state()))
        return ""

    def lojal2(self, n, user):
        res = ""
        if self.ishere(user) and self.oflannel() == n:
            if self.state() > 3:
                continue
            if not self.olongt(self, self.state()):
                # OLONGT NOTE TO BE ADDED
                if self.isdest():
                    res += "--"
                res += self.oplong(user)
                user.wd_it = self.name
        return res

    def iscarrby(self, user):
        if user.person.level < 10 and self.isdest():
            return False
        if self.ocarrf() != 1 and self.ocarrf() != 2:
            return False
        if self.loc != user:
            return 0
        return 1


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


def lobjsat(loc):
    """
    {
    aobjsat(loc,1);
    }
    """


def aobjsat(loc, mode):
    """
    /* Carried Loc ! */
    {
    long a,b,c,d,e,f;
    char x[6],y[6];
    extern long debug_mode;
    b=0;
    c=0;
    d=0;
    e=0;
    f=0;
    while(c<NOBS)
       {
       if(((iscarrby(c,loc))&&(mode==1))||
((iscontin(c,loc))&&(mode==3)))
          {
          e=1;
              f+=1+strlen(oname(c));
if(debug_mode){ f+=5;sprintf(x,"%d",c);sprintf(y,"{%-3s}",x);}
if(isdest(c)) f+=2;
if(iswornby(c,loc)) f+=strlen("<worn> ");
          if(f>79)
             {
             f=0;
            bprintf("\n");
             }
if(isdest(c)) bprintf("(");
         bprintf("%s",oname(c));
         if(debug_mode) bprintf(y);
if(iswornby(c,loc)) bprintf(" <worn>");
if(isdest(c)) bprintf(")");
bprintf(" ");
          f++;
          }
       d+=4;
       c++;
       }
    if(!e)bprintf("Nothing");
   bprintf("\n");
    }
    """


def iscontin(o1, o2):
    """
    {
    extern long my_lev;
    if(ocarrf(o1)!=3) return(0)
    ;
    if(oloc(o1)!=o2) return(0);
    if((my_lev<10)&&(isdest(o1)))return(0);
    return(1);
    }
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
