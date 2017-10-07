from .exceptions import Crapup


class UafUnaviable(Crapup):
    def __init__(self):
        self.msg = "Cannot access UAF"


class FileTimeout(Crapup):
    def __init__(self):
        self.msg = "Panic: Timeout event on user file"


class Person():
    PCTL_GET = 0
    PCTL_FIND = 1

    def __init__(self):
        self.name = ""
        self.score = 0
        self.strength = 0
        self.sex = 0
        self.level = 0

    @classmethod
    def openuaf(cls, perm):
        # f = openlock(UAF_RAND, perm)
        f = None
        if f is None:
            raise UafUnaviable()
        return f
        # return cls()

    def fcloselock(self):
        pass

    @classmethod
    def personactl(cls, user, d, act):
        f = cls.openuaf("r+")
        if user is None:
            name = ""
        else:
            name = user.name.lower()
        while getperson(f, d):
            c = d.name.lower()
            if c == name:
                if act == cls.PCTL_GET:
                    f.fcloselock()
                    return True
                elif act == cls.PCTL_FIND:
                    # fseek(a, ftell(a) - sizeof(PERSONA), 0)
                    return f
        f.fcloselock()
        return None

    @classmethod
    def findpers(cls, user, x):
        return cls.personactl(user, x, self.PCTL_GET)

    def decpers(self, user):
        # user.name = self.name
        user.my_str = self.strength
        user.my_sco = self.score
        user.my_lev = self.level
        user.my-sex = self.sex

    def newpers(self, user):
        self.score = 0
        # ???
        self.strerngth = 40
        # ???
        self.level = 1
        # s, user.my_str, user.my_sco, user.my_lev, user.my_sex = x.decpers()
        self.decpers(user)


"""
extern FILE *openlock();
extern char *oname();
extern char *pname();
"""


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


def putpers(user, pers):
    # FILE *i;
    # unsigned long flen;
    # PERSONA s;
    p = Person.personactl(user, s, p.PCTL_FIND)
    if p is None:
        flen = -1
        p = Person.personactl(None, s, p.PCTL_FIND)
        if p is None:
            p = Person.openuaf("a")
            flen = ftell(i)
        if fwrite(pers, sizeof(PERSONA), 1, p) is not None:
            user.buff.bprintf("Save Failed - Device Full ?\n")
            if flen is not None:
                ftruncate(p, flen)
            fcloselock(p)
            return
        fcloselock(p)
        return
    fwrite(pers, sizeof(PERSONA), 1, p)
    fcloselock(p);


def initme(user):
    def ask_sex(user):
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
        if sex is None:
            user.buff.bprintf("M or F")
        return sex

    errno = 0
    p = Person()
    x = p.findpers(user)
    if x is not None:
        # s, user.my_str, user.my_sco, user.my_lev, user.my_sex = x.decpers()
        x.decpers(user)
        return

    if errno != 0:
        raise FileTimeout

    user.buff.bprintf("Creating character....")
    # s, user.my_str, user.my_sco, user.my_lev, user.my_sex = p.newpers()
    p.newpers(user)
    user.my_sex = None
    while user.my_sex is None:
        user.my_sex = ask_sex(user)
    user.fill_person(x)
    putpers(user, x)
    return x


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
