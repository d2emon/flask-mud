from global_vars import logger


class TextBuffer():
    # ???
    rd_qd = False
    # ???
    pr_due = False

    def __init__(self):
        self.log_fl = None  # 0 = not logging
        self.pr_qcr = False
        self.iskb = True
        self.snoopd = -1
        self.snoopt = -1

        self.makebfr()

    def makebfr(self):
        self.sysbuf = ""

    def pbfr(self):
        # block_alarm();
        # closeworld();
        if len(self.sysbuf):
            self.pr_due = True

        if len(self.sysbuf) and self.pr_qcr:
            # putchar('\n')
            print("\n")

        self.pr_qcr = False
        if self.log_fl is not None:
            self.iskb = False
            dcprnt(self.sysbuf, self.log_fl)
        if self.snoopd != -1:
            # fln = opensnoop(pname(snoopd), "a")
            fln = opensnoop(self.snoopd, "a")
            if fln > 0:
                self.iskb = False
                # dcprnt(sysbuf, fln)
                # fcloselock(fln)
        self.iskb = True
        # dcprnt(sysbuf, stdout)
        self.sysbuf = ""  # clear buffer
        if self.snoopt != -1:
            self.viewsnoop()
        # unblock_alarm();

    def bprintf(self, msg):
        if len(msg) > 235:
            logger().error("Bprintf Short Buffer overflow")
            # crapup("Internal Error in BPRINTF")
        # Now we have a string of chars expanded
        self.quprnt(msg)

    def quprnt(self, msg):
        if len(msg) + len(self.sysbuf) > 4095:
            self.sysbuf = ""
            # loseme()
            logger().error("Buffer overflow on user %s", "globme")
            # crapup("PANIC - Buffer overflow")
        self.sysbuf += msg

    def viewsnoop(self):
        fx = opensnoop("globme", "r+")
        if self.snoopt == -1:
            return
        if fx == 0:
            return
        # while not feof(fx) and fgets(z, 127, fx):
        #     print("|%s" % (z))
        # ftruncate(fileno(fx), 0)
        # fcloselock(fx)

        # x = self.snoopt
        # self.snoopt = -1
        # # self.pbfr()
        # self.snoopt = x


"""
#include "files.h"
#include <stdio.h>
#include "System.h"
"""

# long pr_due=0;


# The main loop
def dcprnt(stri, f):
    """
 char *str;
 FILE *file;
    {
    long ct;
    ct=0;
    while(str[ct])
       {
       if(str[ct]!='\001'){fputc(str[ct++],file);continue;}
       ct++;
       switch(str[ct++])
          {
          case 'f':
             ct=pfile(str,ct,file);continue;
          case 'd':
             ct=pndeaf(str,ct,file);continue;
          case 's':
             ct=pcansee(str,ct,file);continue;
          case 'p':
             ct=prname(str,ct,file);continue;
          case 'c':
             ct=pndark(str,ct,file);continue;
          case 'P':
             ct=ppndeaf(str,ct,file);continue;
          case 'D':
             ct=ppnblind(str,ct,file);continue;
          case 'l':
             ct=pnotkb(str,ct,file);continue;
          default:
             strcpy(str,"");
             loseme();crapup("Internal $ control sequence error\n");
             }
       }
    }
    """


def pfile(stri, ct, f):
    """
 char *str;
 FILE *file;
    {
    extern long debug_mode;
    char x[128];
    ct=tocontinue(str,ct,x,128);
    if(debug_mode) fprintf(file,"[FILE %s ]\n",str);
    f_listfl(x,file);
    return(ct);
    }
    """


def pndeaf(stri, ct, f):
    """
 char *str;
 FILE *file;
    {
    char x[256];
    extern long ail_deaf;
    ct=tocontinue(str,ct,x,256);
    if(!ail_deaf)fprintf(file,"%s",x);
    return(ct);
    }
    """


def pcansee(stri, ct, f):
    """
 char *str;
 FILE *file;
    {
    char x[25];
    char z[257];
    long a;
    ct=tocontinue(str,ct,x,23);
    a=fpbns(x);
    if(!seeplayer(a))
       {
       ct=tocontinue(str,ct,z,256);
       return(ct);
       }
    ct=tocontinue(str,ct,z,256);
    fprintf(file,"%s",z);
    return(ct);
    }
    """


def prname(stri, ct, f):
    """
 char *str;
 FILE *file;
    {
    char x[24];
    ct=tocontinue(str,ct,x,24);
    if(!seeplayer(fpbns(x)))
    fprintf(file,"Someone");
    else
      fprintf(file,"%s",x);
    return(ct);
    }
    """


"""
int pndark(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[257];
    extern long ail_blind;
    ct=tocontinue(str,ct,x,256);
    if((!isdark())&&(ail_blind==0))
    fprintf(file,"%s",x);
    return(ct);
    }

int tocontinue(str,ct,x,mx)
 char *str;
 long ct;
 char *x;
 long mx;
    {
    long s;
    s=0;
    while(str[ct]!='\001')
       {
       x[s++]=str[ct++];
       }
    x[s]=0;
if(s>=mx)
{
syslog("IO_TOcontinue overrun");
strcpy(str,"");
crapup("Buffer OverRun in IO_TOcontinue");
}
    return(ct+1);
    }

int seeplayer(x)
    {
    extern long mynum;
    extern long ail_blind;
    extern long curch;
    if(x==-1) return(1);
    if(mynum==x) {return(1);} /* me */
    if(plev(mynum)<pvis(x)) return(0);
    if(ail_blind) return(0); /* Cant see */
    if((curch==ploc(x))&&(isdark(curch)))return(0);
    setname(x);
    return(1);
    }
int ppndeaf(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[24];
    extern long ail_deaf;
    long a;
    ct=tocontinue(str,ct,x,24);
    if(ail_deaf) return(ct);
    a=fpbns(x);
    if(seeplayer(a)) fprintf(file,"%s",x);
    else
      fprintf(file,"Someone");
    return(ct);
    }

int  ppnblind(str,ct,file)
char *str;
FILE *file;
    {
    extern long ail_blind;
    char x[24];
    long a;
    ct=tocontinue(str,ct,x,24);
    if(ail_blind) return(ct);
    a=fpbns(x);
    if(seeplayer(a)) fprintf(file,"%s",x);
    else
       fprintf(file,"Someone");
    return(ct);
    }



void logcom()
    {
    extern FILE * log_fl;
    extern char globme[];
    if(getuid()!=geteuid()) {bprintf("\nNot allowed from this ID\n");return;}
    if(log_fl!=0)
       {
       fprintf(log_fl,"\nEnd of log....\n\n");
       fclose(log_fl);
       log_fl=0;
       bprintf("End of log\n");
       return;
       }
    bprintf("Commencing Logging Of Session\n");
    log_fl=fopen("mud_log","a");
    if(log_fl==0) log_fl=fopen("mud_log","w");
    if(log_fl==0)
       {
       bprintf("Cannot open log file mud_log\n");
       return;
       }
    bprintf("The log will be written to the file 'mud_log'\n");
    }

int pnotkb(str,ct,file)
 char *str;
 FILE *file;
    {
    extern long iskb;
    char x[128];
    ct=tocontinue(str,ct,x,127);
    if(iskb) return(ct);
    fprintf(file,"%s",x);
    return(ct);
    }
"""


def opensnoop(user, per):
    # z = "%s%s" % (SNOOP, user)
    # x = openlock(z, per)
    # return x
    return 0


# char sntn[32];


def snoopcom():
    """
    {
    FILE *fx;
    long x;
    if(my_lev<10)
       {
       bprintf("Ho hum, the weather is nice isn't it\n");
       return;
       }
    if(snoopt!=-1)
       {
       bprintf("Stopped snooping on %s\n",sntn);
       snoopt= -1;
       sendsys(sntn,globme,-400,0,"");
       }
    if(brkword()== -1)
       {
       return;
       }
    x=fpbn(wordbuf);
    if(x==-1)
       {
       bprintf("Who is that ?\n");
       return;
       }
    if(((my_lev<10000)&&(plev(x)>=10))||(ptstbit(x,6)))
       {
       bprintf("Your magical vision is obscured\n");
       snoopt= -1;
       return;
       }
    strcpy(sntn,pname(x));
    snoopt=x;
    bprintf("Started to snoop on %s\n",pname(x));
    sendsys(sntn,globme,-401,0,"");
    fx=opensnoop(globme,"w");
    fprintf(fx," ");
    fcloselock(fx);
    }
    """


def chksnp():
    """
{
if(snoopt==-1) return;
sendsys(sntn,globme,-400,0,"");
}
    """


def setname(x):
    """
    /* Assign Him her etc according to who it is */
long x;
{
	if((x>15)&&(x!=fpbns("riatha"))&&(x!=fpbns("shazareth")))
	{
		strcpy(wd_it,pname(x));
		return;
	}
	if(psex(x)) strcpy(wd_her,pname(x));
	else strcpy(wd_him,pname(x));
	strcpy(wd_them,pname(x));
}
"""
