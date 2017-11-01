"""
char *verbtxt[]={
    "go","climb","n","e","s","w","u","d", "north","east","south","west","up","down", "quit", "get","take","drop",
    "look","i","inv","inventory","who","reset","zap","eat","drink","play","shout","say","tell",
    "save","score","exorcise","give","steal","pinch","levels","help","value","stats","examine","read",
    "delete","pass","password","summon","weapon","shoot","kill","hit","fire","launch","smash","break",
    "laugh",
    "cry","burp","fart","hiccup","grin","smile","wink","snigger","pose","set",
    "pray","storm","rain","sun","snow","goto",
    "wear",
    "remove","put","wave","blizzard","open","close","shut","lock","unlock","force","light",
    "extinguish","where","turn","invisible","visible","pull","press","push","cripple","cure","dumb",
    "change","missile","shock","fireball","translocate","blow","sigh","kiss","hug","slap",
    "tickle","scream","bounce","wiz","stare","exits","crash","sing","grope","spray",
    "groan","moan","directory","yawn","wizlist","in","smoke","deafen","resurrect","log",
    "tss","rmedit","loc","squeeze","users","honeyboard","inumber","update","become","systat",
    "converse","snoop","shell","raw","purr","cuddle","sulk","roll","credits","brief",
    "debug","jump","wield","map","flee","bug","typo","pn","blind","patch","debugmode",
    "pflags","frobnicate",
    "strike",
    "setin","setout","setmin","setmout","emote","dig","empty"
    ,0 };
int verbnum[]={
    1,1,2,3,4,5,6,7,2,3,4,5,6,7,8,9,9,10,
    11,12,12,12,13,14,15,16,16,17,18,19,20,
    21,22,23,24,25,25,26,27,28,29,30,30,
    31,32,32,33,34,35,35,35,35,35,35,35,
    50,
    51,52,53,54,55,56,57,58,59,60,
    61,62,63,64,65,66,
    100,
    101,102,103,104,105,106,106,107,108,109,110,
    111,112,117,114,115,117,117,117,118,119,120,
    121,122,123,124,125,126,127,128,129,130,
    131,132,133,134,135,136,137,138,139,140,
    141,142,143,144,145,146,147,148,149,150,
    151,152,153,154,155,156,157,158,159,160,
    161,162,163,164,165,166,167,168,169,170,
    171,172,34,173,174,175,176,177,178,179,180,
    181,182,
    35,
    183,184,185,186,187,188,189
};
"""


EXITS = {
    "north": 0,
    "east": 1,
    "south": 2,
    "west": 3,
    "up": 4,
    "down": 5,
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3,
    "u": 4,
    "d": 5,
}


def doaction(n):
    """
    {
    char xx[128];
    extern long my_sco;
    extern long curmode;
    extern long curch;
    extern long debug_mode;
    extern char globme[];
    extern long isforce;
    extern long in_fight;
    extern long brmode;
    long  brhold;
    extern long mynum;
    extern long my_lev;
    openworld();
    switch(n)
       {
    1: dogocom
    2: dodirn
    3: dodirn
    4: dodirn
    5: dodirn
    6: dodirn
    7: dodirn
    8: QUIT;
    9: getobj();
    10: dropitem();
    11: look_cmd();
    12: inventory();
    13: whocom();
    14: rescom();
    15: lightning();
    16: eatcom();
    17: playcom();
    18: shoutcom();
    19: saycom();
    20: tellcom();
    21: saveme();
    22: scorecom();
    23: exorcom();
    24: givecom();
    25: stealcom();
    26: levcom();
    27: helpcom();
    28: valuecom();
    29: stacom();
    30: examcom();
    31: delcom();
    32: passcom();
    33: sumcom();
    34: weapcom();
    35: killcom();
    ...
    50: laughcom();
    51: crycom();
    52: burpcom();
    53: fartcom();
    54: hiccupcom();
    55: grincom();
    56: smilecom();
    57: winkcom();
    58: sniggercom();
    59: posecom();
    60: setcom();
    61: praycom();
    62: stormcom();
    63: raincom();
    64: suncom();
    65: snowcom();
    66: goloccom();



       case 139:
          if(in_fight)
             {
             bprintf("Not in a fight!\n");break;
             }
          gropecom();
          break;
       case 137:
          crashcom();
          break;
       case 100:
          wearcom();
          break;
       case 101:
          removecom();
          break;
       case 102:
          putcom();
          break;
       case 103:
          wavecom();
          break;
       case 104:
          blizzardcom();
          break;
       case 105:
          opencom();
          break;
       case 106:
          closecom();
          break;
       case 107:
          lockcom();
          break;
       case 108:
          unlockcom();
          break;
       case 109:
          forcecom();
          break;
       case 110:
          lightcom();
          break;
       case 111:
          extinguishcom();
          break;
       case 118:
          cripplecom();
          break;
       case 119:
          curecom();
          break;
       case 120:
          dumbcom();
          break;
       case 121:
          changecom();
          break;
       case 122:
          missilecom();
          break;
       case 123:
          shockcom();
          break;
       case 124:
          fireballcom();
          break;
       case 126:
          blowcom();
          break;
       case 127:
          sighcom();
          break;
       case 128:
          kisscom();
          break;
       case 129:
          hugcom();
          break;
       case 130:
          slapcom();
          break;
       case 131:
          ticklecom();
          break;
       case 132:
          screamcom();
          break;
       case 133:
          bouncecom();
          break;
       case 134:
          wizcom();
          break;
       case 135:
          starecom();
          break;
       case 136:
          exits();
          break;
       case 138:
          singcom();
          break;
       case 140:
          spraycom();
          break;
       case 141:
          groancom();
          break;
       case 142:
          moancom();
          break;
       case 143:
          dircom();
          break;
       case 144:
          yawncom();
          break;
       case 117:;
       case 113:
          pushcom();
          break;
       case 145:
          wizlist();
          break;
       case 146:
          incom();
          break;
       case 147:
          lightcom();
          break;
       case 114:
          inviscom();
          break;
       case 115:
          viscom();
          break;
       case 148:
          deafcom();
          break;
       case 149:
          ressurcom();
          break;
       case 150:
          logcom();
          break;
       case 151:
          tsscom();
          break;
       case 152:
          rmeditcom();
          break;
       case 154:
          squeezecom();
          break;
       case 153:
          loccom();
          break;
       case 155:
          usercom();
          break;
       case 156:
          u_system();
          break;
       case 157:
          inumcom();
          break;
       case 158:
          updcom();
          break;
       case 159:
          becom();
          break;
       case 160:
          systat();
          break;
       case 161:
          convcom();
          break;
       case 162:
          snoopcom();
          break;
       case 163:
          shellcom();
          break;
       case 164:
          rawcom();
          break;
       case 165:
          purrcom();
          break;
       case 166:
          cuddlecom();
          break;
       case 167:
          sulkcom();
          break;
       case 168:
          rollcom();
          break;
       case 169:
          bprintf("\001f%s\001",CREDITS);
          break;
       case 170:
          brmode=!brmode;
          break;
       case 171:
          debugcom();
          break;
       case 172:
          jumpcom();
          break;
       case 112:
          wherecom();
          break;
       case 173:
          bprintf("Your adventurers automatic monster detecting radar, and long range\n");
          bprintf("mapping kit, is, sadly, out of order.\n");break;
       case 174:
          if(!in_fight)
             {
             dogocom();
             break;
             }
          else
             {
             char ar[120];
             if(iscarrby(32,mynum))
                {
                bprintf("The sword won't let you!!!!\n");
                break;
                }
             sprintf(ar,"\001c%s\001 drops everything in a frantic attempt to escape\n",globme);
             sendsys(globme,globme,-10000,curch,ar);
             sendsys(globme,globme,-20000,curch,"");
             my_sco-=my_sco/33; /* loose 3% */
             calibme();
             in_fight=0;
             on_flee_event();
             dogocom();
             break;
             }
       case 175:
          bugcom();
          break;
       case 176:
          typocom();
          break;
       case 177:
          pncom();
          break;
       case 178:
          blindcom();
          break;
       case 179:
          edit_world();
          break;
       case 180:
          if(ptstflg(mynum,4)) debug_mode=1-debug_mode;
          break;
       case 181:
          setpflags();
          break;
       case 182:
          frobnicate();
          break;
       case 183:
          setincom();
          break;
       case 184:
          setoutcom();
          break;
       case 185:
          setmincom();
          break;
       case 186:
          setmoutcom();
          break;
       case 187:
          emotecom();
          break;
       case 188:
          digcom();
          break;
       case 189:
          emptycom();
          break;
       default:
          if(my_lev>9999)bprintf("Sorry not written yet[COMREF %d]\n",n);
          else bprintf("I don't know that verb.\n");
          break;
       }
    }
    """


def dogocom(user, wordbuff=None):
    """
    Action 1
    """
    # if brkword is None:
    if wordbuff is None:
        raise GoError("GO where ?")
    if wordbuff == "rope":
        wordbuff = "up"
    exit_id = EXITS.get(wordbuff)
    if exit_id is None:
        raise GoError("Thats not a valid direction")
    return dodirn(exit_id)


def dodirn(user, direction=None):
    """
    Action 2-7
    """
    user.go(direction)


def do_action_8(user):
    """
    Action 8
    """
    user.quit()
