class Person():
    def __init__(self):
        self.name = ""
        self.score = 0
        self.strength = 0
        self.sex = 0
        self.level = 0

    def decpers(self):
        return self.name, self.strength, self.score, self.level, self.sex


"""
#include <errno.h>
#include <stdio.h>
#include "files.h"

extern FILE *openuaf();
extern FILE *openlock();
extern char *oname();
extern char *pname();

extern char globme[];
"""


PCTL_GET = 0
PCTL_FIND = 1


def personactl(name, d, act):
    a = openuaf("r+")
    e = name.lower()
    while getperson(a, d):
        c = d.name.lower()
        if c == e:
            if act == PCTL_GET:
                # fcloselock(a)
                return True
            elif act == PCTL_FIND:
                # fseek(a, ftell(a) - sizeof(PERSONA), 0)
                return a
    # fcloselock(a)
    return None


def findpers(name, x):
    return personactl(name, x, PCTL_GET)


def delpers(name):
    """
    {
    FILE *i;
    PERSONA x;
    l1:
    i=(FILE *)personactl(name,&x,PCTL_FIND);
    if(i==(FILE *)-1) return;
    lowercase(name);
    lowercase(x.p_name);
    if(strcmp(x.p_name,name))
        crapup("Panic: Invalid Persona Delete");
    strcpy(x.p_name,"");
    x.p_level= -1;
    fwrite(&x,sizeof(PERSONA),1,i);
    fcloselock(i);
    goto l1;
    }
    """


def putpers(name, pers):
    """
    char *name;
    PERSONA *pers;
    {
    FILE *i;
    unsigned long flen;
    PERSONA s;
    i=(FILE *)personactl(name,&s,PCTL_FIND);
    if(i==(FILE *)-1)
    {
        flen= -1;
        i=(FILE *)personactl("",&s,PCTL_FIND);
        if(i!=(FILE *)-1) goto fiok;
        i=openuaf("a");
        flen=ftell(i);
        fiok:
        if(fwrite(pers,sizeof(PERSONA),1,i)!=1)
        {
            bprintf("Save Failed - Device Full ?\n");
            if(flen!=-1)ftruncate(fileno(i),flen);
            fcloselock(i);
            return;
        }
        fcloselock(i);
        return;
    }
    fwrite(pers,sizeof(PERSONA),1,i);
    fcloselock(i);
    }
    """


def openuaf(perm):
    """
    char *perm;
    {
    FILE *i;
    i=openlock(UAF_RAND,perm);
    if(i==NULL)
    {
        crapup("Cannot access UAF\n");
    }
    return(i);
    }
    """


# long my_sco;
# long my_lev;
# long my_str;
# long my_sex;


def initme(user):
    def fill_user(person, user):
        person.name = user.name
        person.strength = user.my_str
        person.level = user.my_lev
        person.sex = user.my_sex
        person.score = user.my_sco

    def moan1(user, x):
        user.buff.bprintf("\nSex (M/F) : ")
        user.buff.pbfr()
        user.terminal.keysetback()
        # s = getkbd(2)
        s = "M"
        user.terminal.keysetup()
        s = s.lower()
        sexes = {
            'm': 0,
            'f': 1,
        }
        sex = sexes.get(s[0])
        user.my_sex = sex
        if sex is None:
            user.buff.bprintf("M or F")
            return moan1(user, x)
        fill_user(x, user)
        putpers(user, x)
        return x

    errno = 0
    x = findpers(user)
    if x is not None:
        s, user.my_str, user.my_sco, user.my_lev, user.my_sex = x.decpers()
        return
    if errno != 0:
        # crapup("Panic: Timeout event on user file\n")
        pass
    x.score = 0
    # ???
    x.strerngth = 40
    # ???
    x.level = 1
    user.buff.bprintf("Creating character....")
    # s, user.my_str, user.my_sco, user.my_lev, user.my_sex = x.decpers()
    s, user.my_str, user.my_sco, user.my_lev, user.my_sex = x.decpers()
    moan1(user, x)


def saveme():
    """
    extern char globme[];
    extern long zapped;
    PERSONA x;
    extern int mynum;
    strcpy(x.p_name,globme);
    x.p_strength=my_str;
    x.p_level=my_lev;
    x.p_sex=psexall(mynum);
    x.p_score=my_sco;
    if(zapped) return;
    bprintf("\nSaving %s\n",globme);
    putpers(globme,&x);
    """


def validname(name):
    """
 char *name;
    {
    long a;
    if(resword(name)){bprintf("Sorry I cant call you that\n");return(0);  }
    if(strlen(name)>10)
       {
       return(0);
       }
    a=0;
    while(name[a])
       {
       if(name[a]==' ')
          {
          return(0);
          }
       a++;
       }
    if(fobn(name)!=-1)
       {
      bprintf("I can't call you that , It would be confused with an object\n");
       return(0);
       }
    return(1);
    }
    """


def resword(name):
    """
{
if(!strcmp(name,"The")) return(1);
if(!strcmp(name,"Me")) return(1);
if(!strcmp(name,"Myself")) return(1);
if(!strcmp(name,"It")) return(1);
if(!strcmp(name,"Them")) return(1);
if(!strcmp(name,"Him")) return(1);
if(!strcmp(name,"Her")) return(1);
if(!strcmp(name,"Someone")) return(1);
return(0);
}
    """


def getperson(f, pers):
    # pers = fread(pers, sizeof(PERSONA), 1, f) is None:
    pers = None
    if pers is None:
        return False
    return True
