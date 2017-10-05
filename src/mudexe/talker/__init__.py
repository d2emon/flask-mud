"""
AberMUD II   C


This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott

This file holds the basic communications routines
"""
from global_vars import logger
# from ..gamego import crapup
from ..mud.world import World


# include "files.h"
# include "flock.h"

# long oddcat=0;
# long  talkfl=0;

# include <stdio.h>
# include <sys/errno.h>
# include <sys/file.h>

# extern FILE * openlock();
# extern long my_str;
# extern long my_sex;
# extern long my_lev;
# extern FILE * openroom();
# extern FILE * openworld();
# extern char * pname();
# extern char * oname();
# extern long ppos();
# extern char key_buff[];

# long  meall=0;

"""
Data format for mud packets

Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]

[channel][controlword][text data]

[controlword]
0 = Text
- 1 = general request

"""


def vcpy(dest, offd, source, offs, l):
    """
long *dest,*source;
long offd,offs,len;
    {
    long c;
    c=0;
    while(c<len)
       {
       dest[c+offd]=source[c+offs];
       c++;
       }
    }
    """

# long gurum=0;
# long convflg=0;


def sendmsg(name):
    """
 char *name;
    {
    extern long debug_mode;
    extern char *sysbuf;
    extern long curch,moni,mynum;
    char prmpt[32];
    long a;
extern long tty;
    char work[200];
    long w2[35];
    extern char key_buff[];
    extern long convflg;
    extern long my_lev;
extern long my_str;
extern long in_fight;
extern long fighting;
    extern long curmode;
    l:pbfr();
if(tty==4) btmscr();
strcpy(prmpt,"\r");
    if(pvis(mynum)) strcat(prmpt,"(");
    if(debug_mode) strcat(prmpt,"#");
    if(my_lev>9)strcat(prmpt,"----");
    switch(convflg)
       {
       case 0:
          strcat(prmpt,">");
          break;
       case 1:
          strcat(prmpt,"\"");
          break;
       case 2:
          strcat(prmpt,"*");
          break;
       default:
          strcat(prmpt,"?");
          }
    if(pvis(mynum)) strcat(prmpt,")");
    pbfr();
    if(pvis(mynum)>9999) set_progname(0,"-csh");
    else
    sprintf(work,"   --}----- ABERMUD -----{--     Playing as %s",name);
    if(pvis(mynum)==0) set_progname(0,work);
    sig_alon();
    key_input(prmpt,80);
    sig_aloff();
    strcpy(work,key_buff);
if(tty==4) topscr();
strcat(sysbuf,"\001l");
strcat(sysbuf,work);
strcat(sysbuf,"\n\001");
openworld();
rte(name);
closeworld();
    if((convflg)&&(!strcmp(work,"**")))
       {
       convflg=0;
       goto l;
       }
    if(!strlen(work)) goto nadj;
if((strcmp(work,"*"))&&(work[0]=='*')){(work[0]=32);goto nadj;}
    if(convflg)
       {
       strcpy(w2,work);
       if(convflg==1) sprintf(work,"say %s",w2);
       else
          sprintf(work,"tss %s",w2);
       }
    nadj:if(curmode==1) gamecom(work);
    else
       {
       if(((strcmp(work,".Q"))&&(strcmp(work,".q")))&& (!!strlen(work)))
          {
          a=special(work,name);
          }
       }
if(fighting>-1)
{
if(!strlen(pname(fighting)))
{
in_fight=0;
fighting= -1;
}
if(ploc(fighting)!=curch)
{
in_fight=0;
fighting= -1;
}
}
if(in_fight) in_fight-=1;
    return((!strcmp(work,".Q"))||(!strcmp(work,".q")));
    }
    """


def send2(block):
    """
 long *block;
    {
    FILE * unit;
    long number;
    long inpbk[128];
    extern char globme[];
    extern char *echoback;
    unit=openworld();
    if (unit<0) {loseme();crapup("\nAberMUD: FILE_ACCESS : Access failed\n");}
    sec_read(unit,inpbk,0,64);
    number=2*inpbk[1]-inpbk[0];inpbk[1]++;
    sec_write(unit,block,number,128);
    sec_write(unit,inpbk,0,64);
    if (number>=199) cleanup(inpbk);
    if(number>=199) longwthr();
    }
    """


# FILE *fl_com;


def openlock(f, perm):
    """
char *file;
char *perm;
    {
    FILE *unit;
    long ct;
    extern int errno;
    extern char globme[];
    ct=0;
   unit=fopen(file,perm);
   if(unit==NULL) return(unit);
   /* NOTE: Always open with R or r+ or w */
intr:if(flock(fileno(unit),LOCK_EX)== -1)
    if(errno==EINTR) goto intr; /* INTERRUPTED SYSTEM CALL CATCH */
    switch(errno)
    {
        case ENOSPC:crapup("PANIC exit device full\n");
/*    	case ESTALE:;*/
        case EHOSTDOWN:;
        case EHOSTUNREACH:crapup("PANIC exit access failure, NFS gone for a snooze");
    }
    return(unit);
    }
    """


def talker(user):
    # extern long curch,cms;
    # FILE *fl;
    # char string[128];
    world = World()
    user.cms = -1
    user.putmeon(world)
    user.rte()
    world.closeworld()
    user.cms = -1
    special(".g", user)
    user.i_setup = True
    while True:
        user.buff.pbfr()
        sendmsg(user)
        if user.buff.rd_qd:
            user.rte()
        user.buff.rd_qd = False
        world.closeworld()
        user.buff.pbfr()
        break
    logger().debug("<<< talker(%s)" % (user, ))


def cleanup(inpbk):
    """
 long *inpbk;
    {
    FILE * unit;
    long buff[128],ct,work,*bk;
    unit=openworld();
    bk=(long *)malloc(1280*sizeof(long));
    sec_read(unit,bk,101,1280);sec_write(unit,bk,1,1280);
    sec_read(unit,bk,121,1280);sec_write(unit,bk,21,1280);
    sec_read(unit,bk,141,1280);sec_write(unit,bk,41,1280);
    sec_read(unit,bk,161,1280);sec_write(unit,bk,61,1280);
    sec_read(unit,bk,181,1280);sec_write(unit,bk,81,1280);
    free(bk);
    inpbk[0]=inpbk[0]+100;
    sec_write(unit,inpbk,0,64);
    revise(inpbk[0]);
    }
    """


def special(cmd, user):
    # char ch,bk[128];
    # extern long curch,moni;
    # extern long mynum;
    # extern long my_str,my_lev,my_sco,my_sex;
    # FILE * ufl;
    bk = cmd.lower()
    if bk[0] != '.':
        return 0
    ch = bk[1:]
    if ch == 'g':
        user.start_game()
    else:
        print("\nUnknown . option")
    return 1


# long dsdb=0;
# long moni=0;


def broad(mesg):
    """
 char *mesg;
    {
extern long rd_qd;
char bk2[256];
long block[128];
rd_qd=1;
block[1]= -1;
strcpy(bk2,mesg);
vcpy(block,2,(long *)bk2,0,126);
send2(block);
}
    """


def tbroad(message):
    """
char *message;
    {
    broad(message);
    }
    """


# long  bound=0;
# long  tmpimu=0;
# char  *echoback="*e";
# char  *tmpwiz=".";/* Illegal name so natural immunes are ungettable! */


def split(block, nam1, nam2, work, luser):
    """
 long *block;
 char *nam1;
 char *nam2;
 char *work;
 char *luser;
    {
    long wkblock[128],a;
    vcpy(wkblock,0,block,2,126);
    vcpy((long *)work,0,block,64,64);
    a=scan(nam1,(char *)wkblock,0,"",".");
    scan(nam2,(char *)wkblock,a+1,"",".");
if((strncmp(nam1,"The ",4)==0)||(strncmp(nam1,"the ",4)==0))
{
if(!strcmp(lowercase(nam1+4),lowercase(luser))) return(1);
}
    return(!strcmp(lowercase(nam1),lowercase(luser)));
    }
    """


def revise(cutoff):
    """
 long cutoff;
    {
    char mess[128];
    long ct;
    FILE *unit;
    unit=openworld();
    ct=0;
    while(ct<16)
       {
       if((pname(ct)[0]!=0)&&(ppos(ct)<cutoff/2)&&(ppos(ct)!=-2))
          {
          sprintf(mess,"%s%s",pname(ct)," has been timed out\n");
          broad(mess);
          dumpstuff(ct,ploc(ct));
          pname(ct)[0]=0;
          }
       ct++;
       }
    }
    """


def loodrv():
    """
    {
    extern long curch;
    lookin(curch);
    }
    """


def userwrap():
    """
{
extern char globme[];
extern long iamon;
if(fpbns(globme)!= -1) {loseme();syslog("System Wrapup exorcised %s",globme);}
}
    """


def fcloselock(f):
    """
FILE *file;
{
fflush(file);
flock(fileno(file),LOCK_UN);
fclose(file);
}
    """
