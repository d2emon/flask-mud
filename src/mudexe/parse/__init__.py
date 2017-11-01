"""
 globme holds global me data
"""

"""
#define  OBMUL 8
#include <stdio.h>

extern char * oname();
extern char * pname();
extern FILE *openlock();
"""

"""
 Objects held in format

 [Short Text]
 [4 Long texts]
 [Max State]
"""

"""
 Objects in text file in form

 Stam:state:loc:flag
"""

wd = {
    "it": "",
    "him": "",
    "her": "",
    "them": "",
    "there": "",
}


class Parser():
    strbuff = ""
    wordbuff = ""
    stp = 0

    def gamecom(self, s, user, buff):
        # extern long in_fight;

        if s == "!":
            self.strbuf == s
        if s == ".q":
            s = ""  # Otherwise drops out after command

        self.stp = 0

        if not len(s):
            return 0

        if s == "!":
            s = self.strbuf

        if self.brkword(user) is None:
            buff.bprintf("Pardon ?\n")
            return None
        a = self.chkverb()
        if a is None:
            buff.bprintf("I don't know that verb\n")
            return None
        # doaction(a)
        return 0

    def brkword(self, user):
        s = self.strbuf[self.stp:].strip(" ")
        parts = s.split(" ")
        self.wordbuf = parts[0].lower()

        wd.update({
            "me": user.name,
            "myself": user.name,
        })
        r = wd.get(self.wordbuf, None)
        if r is not None:
            self.wordbuf = r
        return self.wordbuf

    def chkverb(self):
        cmds = [GameCmd()] * 255
        return chklist(self.wordbuf, cmds)


def chklist(word, cmdlist):
    best = 0
    cmd = None
    word = word.lower()
    for c in cmdlist:
        s = c.match(word)
        if s > best:
            best = s
            cmd = c
    if best < 5:
        return None
        # No good matches
    return cmd


class GameCmd():
    text = ""
    cmd_id = 0

    def match(self, cmd):
        if cmd == self.text:
            return 10000
        if self.text == "reset":
            return -1
        if not cmd:
            return 0
        s = 0
        for i in range(len(cmd)):
            if i >= len(self.text):
                break
            if cmd[i] == self.text[i]:
                if i == 0:
                    s += 3
                elif i == 1:
                    s += 2
                else:
                    s += 1
        return s


"""
char here_ms[81]="is here";
"""


def gamrcv(user, message):
    # extern long zapped;
    # extern long vdes,tdes,rdes,ades;
    # auto long  zb[32];
    # extern long curch;
    # extern long my_lev;
    # extern long my_sco;
    # extern long my_str;
    # extern long snoopd;
    # extern long fl_com;
    # char ms[128];
    # extern long fighting,in_fight;
    nameme = user.name.lower()
    nam1 = message.from_user
    nam2 = message.to_user
    text = message.text
    isme = split(blok, nam1, nam2, text, nameme)
    # i = (int)text
    if message.message_code == -20000 and Player.query.fpbns(nam1) == user.fighting:
        user.in_fight = 0
        user.fighting= -1
    if message.message_code < -10099:
        return new1rcv(isme, message)
    """
    switch(blok[1])
       {
       case -9900:
          setpvis(i[0],i[1]);break;
       case -666:
          bprintf("Something Very Evil Has Just Happened...\n");
          loseme();
          crapup("Bye Bye Cruel World....");
       case -599:
          if(isme)
             {
             sscanf(text,"%d.%d.%d.",&my_lev,&my_sco,&my_str);
             calibme();
             }
          break;
       case -750:
          if(isme)
             {
             if(fpbns(nam2)!= -1) loseme();
             closeworld();
             printf("***HALT\n");
             exit(0);
             }
       case -400:
          if(isme) snoopd= -1;
          break;
       case -401:
          if(isme)
             {
             snoopd=fpbns(nam2);
             }
          break;
    """
    if message.message_code == -10000:
        if isme:
            return
        if message.location != user.location:
            return
        user.buff.bprintf(text)
        return
    """
       case -10030:
          wthrrcv(blok[0]);break;
       case -10021:
          if(curch==blok[0])
             {
             if(isme==1)
                {
                rdes=1;
                vdes=i[0];
                bloodrcv((long *)text,isme);
                }
             }
          break;
       case -10020:
          if(isme==1)
             {
             ades=blok[0];
             if(my_lev<10)
                {
                bprintf("You drop everything you have as you are summoned by \001p%s\001\n",nam2);
                }
             else
                {
                bprintf("\001p%s\001 tried to summon you\n",nam2);
                return;
                }
             tdes=1;
             }
          break;
       case -10001:
          if(isme==1)
             {
             if (my_lev>10)
                bprintf("\001p%s\001 cast a lightning bolt at you\n", nam2);
             else
                /* You are in the .... */
                {
                bprintf("A massive lightning bolt arcs down out of the sky to strike");
                sprintf(zb,"[ \001p%s\001 has just been zapped by \001p%s\001 and terminated ]\n",
                    globme, nam2);
                sendsys(globme,globme,-10113,curch,zb);
                bprintf(" you between\nthe eyes\n");
                zapped=1;
                delpers(globme);
                sprintf(zb,"\001s%s\001%s has just died.\n\001",globme,globme);
                sendsys(globme,globme,-10000,curch,zb);
                loseme();
                bprintf("You have been utterly destroyed by %s\n",nam2);

                crapup("Bye Bye.... Slain By Lightning");
                }
             }
          else if (blok[0]==curch)
             bprintf("\001cA massive lightning bolt strikes \001\001D%s\001\001c\n\001", nam1);
          break;
       case -10002:
          if(isme!=1)
             {
             if (blok[0]==curch||my_lev>9)
                 bprintf("\001P%s\001\001d shouts '%s'\n\001", nam2, text);
             else
                bprintf("\001dA voice shouts '%s'\n\001",text);
             }
          break;
       case -10003:
          if(isme!=1)
             {
             if (blok[0]==curch)
                bprintf("\001P%s\001\001d says '%s'\n\001", nam2, text);
             }
          break;
       case -10004:
          if(isme)
             bprintf("\001P%s\001\001d tells you '%s'\n\001",nam2,text);
          break;
       case -10010:
          if(isme==1)
             {
             loseme();
             crapup("You have been kicked off");
             }
          else
             bprintf("%s has been kicked off\n",nam1);
          break;
       case -10011:
          if(isme==1)
             {
             bprintf("%s",text);
             }
          break;
          }
    """


"""
 getreinput(blob)
    {
    extern long stp;
    extern char strbuf[];
    strcpy(blob,"");
    while(strbuf[stp]==' ') stp++;
    while(strbuf[stp]) addchar(blob,strbuf[stp++]);
    }


 systat()
    {
    extern long my_lev;
    if(my_lev<10000000)
       {
       bprintf("What do you think this is a DEC 10 ?\n");
       return;
       }
    }


look_cmd()
{
	int a;
	long brhold;
	extern long brmode;
	extern char wordbuf[];
        extern long curch;
	if(brkword()==-1)
	{
          brhold=brmode;
          brmode=0;
          lookin(curch);
          brmode=brhold;
          return;
        }
        if(strcmp(wordbuf,"at")==0)
        {
        	examcom();
        	return;
        }
        if((strcmp(wordbuf,"in"))&&(strcmp(wordbuf,"into")))
        {
        	return;
        }
        if(brkword()==-1)
        {
        	bprintf("In what ?\n");
        	return;
        }
        a=fobna(wordbuf);
	if(a==-1)
	{
		bprintf("What ?\n");
		return;
	}
	if(!otstbit(a,14))
	{
		bprintf("That isn't a container\n");
		return;
	}
	if((otstbit(a,2))&&(state(a)!=0))
	{
		bprintf("It's closed!\n");
		return;
	}
	bprintf("The %s contains:\n",oname(a));
	aobjsat(a,3);
}

set_ms(x)
char *x;
{
	extern long my_lev;
	extern char globme[];
	if((my_lev<10)&&(strcmp(globme,"Lorry")))
	{
		bprintf("No way !\n");
	}
	else
	{
		getreinput(x);
	}
	return;
}
"""
