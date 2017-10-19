from global_vars import logger
from ..gamego.signals import alarm


class BaseOutput():
    def __init__(self):
        self.text = ""

    def output(self, text_buffer, text=None):
        if text is None:
            text = text_buffer.sysbuf
        self.text += self.dcprnt(text)

    def dcprnt(self, text="", output=None):
        """
        The main loop
        ct = 0
        while s[ct]:
            if s[ct] != '\001':
                output.putc(s[ct])
                ct += 1
                continue
            ct += 1
            c = s[ct]
            ct += 1
            if c == 'f':
                ct = pfile(s, ct, f)
                continue
            elif c == 'd':
                ct = pndeaf(s, ct, f)
                continue
            elif c == 's':
                ct = pcansee(s, ct, f)
                continue
            elif c == 'p':
                ct = prname(s, ct, f)
                continue
            elif c == 'c':
                ct = pndark(s, ct, f)
                continue
            elif c == 'P':
                ct = ppndeaf(s, ct, f)
                continue
            elif c == 'D':
                ct = ppnblind(s, ct, f)
                continue
            elif c == 'l':
                ct = pnotkb(s, ct, f)
                continue
            else:
                s = ""
                loseme()
                crapup("Internal $ control sequence error\n")
        """
        return text


class TextOutput(BaseOutput):
    def output(self, text_buffer, text=None):
        text_buffer.iskb = True
        BaseOutput.output(self, text_buffer, text)


class LogOutput(TextOutput):
    def output(self, text_buffer, text=None):
        text_buffer.iskb = False
        BaseOutput.output(self, text_buffer, text)
        # text_buffer.dcprnt(f="log_fl")


class SnoopOutput(TextOutput):
    def __init__(self, player=None, per="a"):
        if player is not None:
            self.fln = self.opensnoop(player, per)
        else:
            self.fln = None

    def output(self, text_buffer, text=None):
        if self.fln is None:
            return
        text_buffer.iskb = False
        BaseOutput.output(self, text_buffer, text)
        # text_buffer.dcprnt(f=sn.fln)
        self.closesnoop()

    def opensnoop(self, player, per="a"):
        # f = "%s%s" % (SNOOP, player.name)
        # return openlock(f, per)
        return 0

    def closesnoop(self):
        logger().debug("<<< fcloselock(%s)" % (self))

    def viewsnoop(self):
        if self.fln is None:
            return
        # while not feof(fx) and fgets(z, 127, fx):
        #     print("|%s" % (z))
        # ftruncate(fileno(fx), 0)
        # fcloselock(fx)

        # x = self.snoopt
        # self.snoopt = None
        # # self.pbfr()
        # self.snoopt = x


class TextBuffer():
    # ???
    rd_qd = False

    def __init__(self):
        self.log_fl = None  # 0 = not logging
        self.pr_qcr = False
        self.pr_due = False
        self.iskb = True
        self.snoopd = None
        self.snoopt = None
        self.sntn = None

        self.makebfr()
        self.output = TextOutput()

    def makebfr(self):
        self.sysbuf = ""
        self.chat = ""

    def pbfr(self, user):
        self.output.text = ""
        alarm.block_alarm()
        user.world.closeworld()
        if len(self.sysbuf):
            self.pr_due = True

        if len(self.sysbuf) and self.pr_qcr:
            self.output.text += "\n"

        self.pr_qcr = False
        if self.log_fl is not None:
            self.log_fl.output(self)
        if self.snoopd is not None:
            SnoopOutput(self.snoopd).output(self)
        self.output.output(self)

        self.sysbuf = ""  # clear buffer
        if self.snoopt is not None:
            self.viewsnoop()
        alarm.unblock_alarm()
        print(self.output.text)
        return self.output.text

    def get_message(self, message):
        self.chat += message

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

    def viewsnoop(self, user):
        sn = SnoopOutput(user.player, "r+")
        if self.snoopt is None:
            return
        sn.viewsnoop()

    def chksnp(self, sntn, user):
        self.sntn = sntn
        if self.snoopt is None:
            return
        self.sntn.sendsys(user, -400, 0)


def pfile(stri, ct, f):
    ct, x = tocontinue(stri, ct, 128)
    # extern long debug_mode;
    # if debug_mode:
    #     f.printf("[FILE %s ]\n", stri)
    # f.f_listfl(x)
    return ct


def pndeaf(stri, ct, f):
    ct, x = tocontinue(stri, ct, 256)
    # if not user.ail_deaf:
    #     f.printf(x)
    return ct


def pcansee(stri, ct, f):
    ct, x = tocontinue(stri, ct, 23)
    # a = Player.query.fpbns(x)
    # if not seeplayer(a):
    #     ct, z = tocontinue(stri, ct, 256)
    #     return ct
    # ct, z = tocontinue(stri, ct, 256)
    # f.printf(z)
    return ct


def prname(stri, ct, f):
    ct, x = tocontinue(stri, ct, 24)
    # if not seeplayer(Player.fpbns(x)):
    #     f.printf("Someone")
    # else:
    #     f.printf(x)
    return ct


def pndark(stri, ct, f):
    ct, x = tocontinue(stri, ct, 256)
    # if not user.isdark() and not user.ail_blind:
    #     f.printf(x)
    return ct


def tocontinue(stri, ct, mx):
    x = ""
    while stri[ct] != '\001':
        x += stri[ct]
        ct += 1
    if len(x) >= mx:
        # syslog("IO_TOcontinue overrun")
        # stri = ""
        # crapup("Buffer OverRun in IO_TOcontinue")
        pass
    return ct+1, "x"


def ppndeaf(stri, ct, f):
    ct, x = tocontinue(stri, ct, 24)
    # if user.ail_deaf:
    #     return ct
    # a = Player.fpbns(x)
    # if seeplayer(a):
    #     f.printf(x)
    # else:
    #     f.printf("Someone")
    return ct


def ppnblind(stri, ct, f):
    ct, x = tocontinue(stri, ct, 24)
    # if user.ail_blind:
    #     return ct
    # a = Player.query.fpbns(x)
    # if seeplayer(a):
    #     f.printf(x)
    # else:
    #     f.printf("Someone")
    return ct


"""
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
"""


def pnotkb(stri, ct, f):
    ct, x = tocontinue(stri, ct, 127)
    # if user.iskb:
    #     return ct
    # f.printf(x)
    return ct


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
