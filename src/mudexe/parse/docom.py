"""
void pncom()
{
	extern long my_lev;
	extern char globme[];
	bprintf("Current pronouns are:\n");
	bprintf("Me              : %s\n",globme);
	bprintf("Myself          : %s\n",globme);
	bprintf("It              : %s\n",wd_it);
	bprintf("Him             : %s\n",wd_him);
	bprintf("Her             : %s\n",wd_her);
	bprintf("Them            : %s\n",wd_them);
	if(my_lev>9)
	{
		bprintf("There           : %s\n",wd_there);
	}
}
"""


def lightning(self, player=None):
    if self.person.level < 10:
        raise Exception("Your spell fails.....")
    # if brkword is None:
    if player is None:
        raise Exception("But who do you wish to blast into pieces....")
    vic = Player.fpbn(player)
    if vic is None:
        raise Exception("There is no one on with that name")
    vic.sendsys(self, -10001, text="")
    logger().info("%s zapped %s" % (self.name, vic.name))
    if vic.id > 15:
        vic.woundmn(10000)
        # DIE
    broad("<d>You hear an ominous clap of thunder in the distance\n</d>");


def eatcom(self, food=None):
    # if brkword is None:
    if food is None:
        Exception("What")

    if self.location == 609 and food == "water":
        food = "spring"
    # if wordbuff == "from":
    #     brkword
    b = Item.fobna(food)
    if b is None:
        Exception("There isn't one of those here")
    if b.id == 11:
        self.buff.bprintf("You feel funny, and then pass out\n")
        self.buff.bprintf("You wake up elsewhere....\n")
        self.teletrap(-1076)
    elif b.id == 75:
        self.buff.bprintf("very refreshing\n")
    elif b.id == 175:
        if self.person.level < 3:
            self.person.score += 40
            calibme()
            self.buff.bprintf("You feel a wave of energy sweeping through you.\n")
        else:
            self.buff.bprintf("Faintly magical by the taste.\n")
            if self.person.strength < 40:
                self.person.strength += 2
                calibme()
    else:
        if b.bit[6]:
            b.destroy()
            self.buff.bprintf("Ok....\n")
            self.person.strength += 12
            calibme()
        else:
            self.buff.bprintf("Thats sure not the latest in health food....\n")


def calibme(self):
    """
    Routine to correct me in user file
    """
    # long  a;
    # extern long mynum,my_sco,my_lev,my_str,my_sex,wpnheld;
    # extern char globme[];
    # long  b;
    # char *sp[128];
    # extern long i_setup;
    if not self.i_setup:
        return
    b = levelof(self.person.score)
    if b != self.person.level:
        self.person.level = b
        self.buff.bprintf("You are now %s " % (self.name))
        logger().info("%s to level %d", self.name, b)
        disle3(b, self.person.sex)
        sp = "<p>%s</p> is now level %d\n" % (self.name, self.person.level)
        self.sendsys(self, -10113, self.player.location, sp )
        if b == 10:
            self.buff.bprintf("<f>%s</f>" % ("GWIZ"))
        self.player.level = self.person.level
        if self.person.strength > (30 + 10 * self.person.level):
            self.person.strength = 30 + 10 * self.person.level
        self.player.strength = self.person.strength
        self.player.sex = self.person.sex
        self.player.weapon = self.wpnheld

def levelof(score):
    # extern long my_lev;
    score = score / 2  # Scaling factor
    if self.person.level > 10:
        return self.person.level
    if score < 500:
        return 1
    if score < 1000:
        return 2
    if score < 3000:
        return 3
    if score < 6000:
        return 4
    if score < 10000:
        return 5
    if score < 20000:
        return 6
    if score < 32000:
        return 7
    if score < 44000:
        return 8
    if score < 70000:
        return 9
    return 10


"""
 playcom()
    {
    extern char wordbuf[];
    extern long curch;
    extern long mynum;
    long  a,b;
    if(brkword()== -1)
       {
       bprintf("Play what ?\n");
       return;
       }
    a=fobna(wordbuf);
    if(a== -1)
       {
       bprintf("That isn't here\n");
       return;
       }
    if(!isavl(a))
       {
       bprintf("That isn't here\n");
       return;
       }
    }
"""


def shoutcom(self, blob=""):
    if chkdumb():
        return
    # blob = getreinput()
    if self.person.level > 9:
        self.sendsys(self, -10104, self.location, blob)
    else:
        self.sendsys(self, -10002, self.location, blob)
    self.buff.bprintf("Ok\n")


def saycom(self, blob=""):
    if chkdumb():
        return
    # blob = getreinput()
    self.sendsys(self, -10003, self.location, blob)
    self.buff.bprintf("You say '%s'\n" % (blob))


def tellcom(self, player=None, blob=""):
    if chkdumb():
        return
    # if(brkword()== -1)
    if player is None:
        raise Exception("Tell who ?")
    b = Player.query.fpbn(player)
    if b is None:
        raise Exception("No one with that name is playing")
    # getreinput(blob);
    b.sendsys(self, -10004, self.location, blob)


"""
 scorecom()
    {
    extern long my_str,my_lev,my_sco;
    extern long my_sex;
    extern char globme[];
    if(my_lev==1)
       {
       bprintf("Your strength is %d\n",my_str);
       return;
       }
    else
       bprintf("Your strength is %d(from %d),Your score is %d\nThis ranks you as %s ",
          my_str,50+8*my_lev,my_sco,globme);
    disle3(my_lev,my_sex);
    }

 exorcom()
    {
    long  x,a;
    extern long curch;
    extern long my_lev;
    extern char globme[];
    extern char wordbuf[];
    if(my_lev<10)
       {
       bprintf("No chance....\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Exorcise who ?\n");
       return;
       }
    x=fpbn(wordbuf);
    if(x== -1)
       {
       bprintf("They aren't playing\n");
       return;
       }
       if(ptstflg(x,1))
       {
       	bprintf("You can't exorcise them, they dont want to be exorcised\n");
       	return;
       	}
    syslog("%s exorcised %s",globme,pname(x));
    dumpstuff(x,ploc(x));
    sendsys(pname(x),globme,-10010,curch,"");
    pname(x)[0]=0;
    }

 givecom()
    {
    auto long  a,b;
    auto long  c,d;
    extern char wordbuf[];
    if(brkword()== -1)
       {
       bprintf("Give what to who ?\n");
       return;
       }
    if(fpbn(wordbuf)!= -1) goto obfrst;
    a=fobna(wordbuf);
    if(a== -1)
       {
       bprintf("You aren't carrying that\n");
       return(0);
       }
    /* a = item giving */
    if(brkword()== -1)
       {
       bprintf("But to who ?\n");
       return;
       }
    if(!strcmp(wordbuf,"to"))
       {
       if(brkword()== -1)
          {
          bprintf("But to who ?\n");
          return;
          }
       }
    c=fpbn(wordbuf);
    if(c== -1)
       {
       bprintf("I don't know who %s is\n",wordbuf);
       return;
       }
    dogive(a,c);
    return;
    obfrst:/* a=player */
    a=fpbn(wordbuf);
    if(a== -1)
       {
       bprintf("Who is %s\n",wordbuf);
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Give them what ?\n");
       return;
       }
    c=fobna(wordbuf);
    if(c== -1)
       {
       bprintf("You are not carrying that\n");
       return;
       }
    dogive(c,a);
    }

 dogive(ob,pl)
    {
    long  x;
    auto z[32];
    extern char globme[];
    extern long my_lev,curch;
    extern long mynum;
    if((my_lev<10)&&(ploc(pl)!=curch))
       {
       bprintf("They are not here\n");
       return;
       }
    if(!iscarrby(ob,mynum))
       {
       bprintf("You are not carrying that\n");
       }
    if(!cancarry(pl))
       {
       bprintf("They can't carry that\n");
       return;
       }
    if((my_lev<10)&&(ob==32))
       {
       bprintf("It doesn't wish to be given away.....\n");
       return;
       }
    setoloc(ob,pl,1);
    sprintf(z,"\001p%s\001 gives you the %s\n",globme,oname(ob));
    sendsys(pname(pl),globme,-10011,curch,z);
    return;
    }

 stealcom()
    {
    extern long mynum;
    extern long curch,my_lev;
    extern char wordbuf[];
    long  a,b;
    long  c,d;
    char x[128];
    long e,f;
    extern char globme[];
    char tb[128];
    if(brkword()== -1)
       {
       bprintf("Steal what from who ?\n");
       return;
       }
    strcpy(x,wordbuf);
    if(brkword()== -1)
       {
       bprintf("From who ?\n");
       return;
       }
    if(!strcmp(wordbuf,"from"))
       {
       if(brkword()== -1)
          {
          bprintf("From who ?\n");
          return;
          }
       }
    c=fpbn(wordbuf);
    if(c== -1)
       {
       bprintf("Who is that ?\n");
       return;
       }
    a=fobncb(x,c);
    if(a== -1)
       {
       bprintf("They are not carrying that\n");
       return;
       }
    if((my_lev<10)&&(ploc(c)!=curch))
       {
       bprintf("But they aren't here\n");
       return;
       }
    if(ocarrf(a)==2)
       {
       bprintf("They are wearing that\n");
       return;
       }
    if(pwpn(c)==a)
       {
       bprintf("They have that firmly to hand .. for KILLING people with\n");
       	return;
       }
    if(!cancarry(mynum))
       {
       bprintf("You can't carry any more\n");
       return;
       }
    time(&f);
    srand(f);
    f=randperc();
    e=10+my_lev-plev(c);
    e*=5;
    if(f<e)
       {
       sprintf(tb,"\001p%s\001 steals the %s from you !\n",globme,oname(a));
       if(f&1){
       	 sendsys(pname(c),globme,-10011,curch,tb);
       	 if(c>15) woundmn(c,0);
       	}
       setoloc(a,mynum,1);
       return;
       }
    else
       {
       bprintf("Your attempt fails\n");
       return;
       }
    }

 dosumm(loc)
    {
    char ms[128];
    extern long curch;
    extern char globme[];
    sprintf(ms,"\001s%s\001%s vanishes in a puff of smoke\n\001",globme,globme);
    sendsys(globme,globme,-10000,curch,ms);
    sprintf(ms,"\001s%s\001%s appears in a puff of smoke\n\001",globme,globme);
    dumpitems();
    curch=loc;
    sendsys(globme,globme,-10000,curch,ms);
    trapch(curch);
    }

 tsscom()
    {
    char s[128];
    extern long my_lev;
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    getreinput(s);
    closeworld();
    keysetback();
    if(getuid()==geteuid()) system(s);
    else bprintf("Not permitted on this ID\n");
    keysetup();
    }

 rmeditcom()
    {
    extern long my_lev;
    extern long cms;
    extern long mynum;
    char ms[128];
    extern char globme[];
    if(!ptstflg(mynum,3))
       {
       bprintf("Dum de dum.....\n");
       return;
       }

    sprintf(ms,"\001s%s\001%s fades out of reality\n\001",globme,globme);
    sendsys(globme,globme,-10113,0,ms); /* Info */
    cms= -2;/* CODE NUMBER */
    update(globme);
    pbfr();
    closeworld();
    if(chdir(ROOMS)==-1) bprintf("Warning: Can't CHDIR\n");
    sprintf(ms,"/cs_d/aberstudent/yr2/hy8/.sunbin/emacs");
    system(ms);
    cms= -1;
    openworld();
    if(fpbns(globme)== -1)
       {
       loseme();
       crapup("You have been kicked off");
       }
    sprintf(ms,"\001s%s\001%s re-enters the normal universe\n\001",globme,globme);
    sendsys(globme,globme,-10113,0,ms);
    rte();
    }

 u_system()
    {
    extern long my_lev;
    extern char globme[];
    extern long cms;
    char x[128];
    if(my_lev<10)
       {
       bprintf("You'll have to leave the game first!\n");
       return;
       }
    cms= -2;
    update(globme);
    sprintf(x,"%s%s%s%s%s","\001s",globme,"\001",globme," has dropped into BB\n\001");
    sendsys(globme,globme,-10113,0,x);
    closeworld();
    system("/cs_d/aberstudent/yr2/iy7/bt");
    openworld();
    cms= -1;
    if(fpbns(globme)== -1)
       {
       loseme();
       crapup("You have been kicked off");
       }
    rte();
    openworld();
    sprintf(x,"%s%s%s%s%s","\001s",globme,"\001",globme," has returned to AberMud\n\001");
    sendsys(globme,globme,-10113,0,x);
    }

 inumcom()
    {
    extern long my_lev;
    extern char wordbuf[];
    if(my_lev<10000)
       {
       bprintf("Huh ?\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("What...\n");
       return;
       }
    bprintf("Item Number is %d\n",fobn(wordbuf));
    }

 updcom()
    {
    extern long my_lev;
    char x[128];
    extern char globme[];
    if(my_lev<10)
       {
       bprintf("Hmmm... you can't do that one\n");
       return;
       }
    loseme();
    sprintf(x,"[ %s has updated ]\n",globme);
    sendsys(globme,globme,-10113,0,x);
    closeworld();
    sprintf(x,"%s",globme);
    execl(EXE,
    "   --{----- ABERMUD -----}--   ",x,0);  /* GOTOSS eek! */
    bprintf("Eeek! someones pinched the executable!\n");
    }

 becom()
    {
    extern char globme[];
    extern long my_lev;
    char x[128];
    char x2[128];
    if(my_lev<10)
       {
       bprintf("Become what ?\n");
       return;
       }
    getreinput(x2);
    if(!strlen(x2))
       {
       bprintf("To become what ?, inebriated ?\n");
       return;
       }
    sprintf(x,"%s has quit, via BECOME\n",globme);
    sendsys("","",-10113,0,x);
    keysetback();
    loseme();
    closeworld();
    sprintf(x,"-n%s",x2);
    execl(EXE2,"   --}----- ABERMUD ------   ",x,0);	/* GOTOSS eek! */
    bprintf("Eek! someone's just run off with mud!!!!\n");
    }
 convcom()
    {
    extern long convflg;
    convflg=1;
    bprintf("Type '**' on a line of its own to exit converse mode\n");
    }

 shellcom()
    {
    extern long convflg,my_lev;
    if(my_lev<10000)
       {
       bprintf("There is nothing here you can shell\n");
       return;
       }
    convflg=2;
    bprintf("Type ** on its own on a new line to exit shell\n");
    }

 rawcom()
    {
    extern long my_lev;
    char x[100],y[100];
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    getreinput(x);
    if((my_lev==10033)&&(x[0]=='!'))
       {
       broad(x+1);
       return;
       }
    else
       {
       sprintf(y,"%s%s%s","** SYSTEM : ",x,"\n\007\007");
       broad(y);
       }
    }

 rollcom()
    {
    auto long  a,b;
    b=ohereandget(&a);
    if(b== -1) return;
    switch(a)
       {
       case 122:;
       case 123:
          gamecom("push pillar");
          break;
       default:
          bprintf("You can't roll that\n");
       }
    }

 debugcom()
    {
    extern long my_lev;
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    debug2();
    }

bugcom()
{
	char x[120];
	extern char globme[];
	getreinput(x);
	syslog("Bug by %s : %s",globme,x);
}

typocom()
{
	char x[120],y[32];
	extern char globme[];
	extern long curch;
	sprintf(y,"%s in %d",globme,curch);
	getreinput(x);
	syslog("Typo by %s : %s",y,x);
}

setmincom()
{
	extern char min_ms[];
	set_ms(min_ms);
}
setincom()
{
	extern char min_ms[];
	set_ms(in_ms);
}
setoutcom()
{
	extern char out_ms[];
	set_ms(out_ms);
}
setmoutcom()
{
	extern char mout_ms[];
	set_ms(mout_ms);
}

setherecom()
{
	extern char here_ms[];
	set_ms(here_ms);
}

digcom()
{
        extern long curch;
	if((oloc(186)==curch)&&(isdest(186)))
	{
		bprintf("You uncover a stone slab!\n");
		ocreate(186);
		return;
	}
	if((curch!=-172)&&(curch!=-192))
	{
		bprintf("You find nothing.\n");
		return;
	}
	if(state(176)==0)
	{
		bprintf("You widen the hole, but with little effect.\n");
		return;
	}
	setstate(176,0);
	bprintf("You rapidly dig through to another passage.\n");
}

emptycom()
{
	long a,b;
	extern long numobs;
        extern long mynum;
	char x[81];
	b=ohereandget(&a);
	if(b==-1) return;
	b=0;
	while(b<numobs)
	{
		if(iscontin(b,a))
		{
			setoloc(b,mynum,1);
			bprintf("You empty the %s from the %s\n",oname(b),oname(a));
			sprintf(x,"drop %s",oname(b));
			gamecom(x);
			pbfr();
			openworld();
		}
		b++;
	}
}
"""
