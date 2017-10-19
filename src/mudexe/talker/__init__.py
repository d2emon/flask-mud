"""
AberMUD II   C


This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott

This file holds the basic communications routines
"""
# from global_vars import logger


# include "files.h"

# long oddcat=0;
# long  talkfl=0;

# extern FILE * openroom();
# extern long ppos();

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


# long gurum=0;


def talker(user):
    user.prepare_game()
    # while True:
    for i in range(5):
        user.do_loop()


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


# long dsdb=0;
# long moni=0;


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
