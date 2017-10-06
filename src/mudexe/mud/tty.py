"""
Key drivers
"""
from global_vars import logger
from ..gamego.signals import alarm


# ???
def gamecom(work):
    logger().debug("<<< gamecom(%s)", work)


def special(cmd, user):
    if not cmd:
        return
    bk = cmd.lower()
    if bk[0] != '.':
        return 0
    ch = bk[1:]
    if ch == 'g':
        user.start_game()
    else:
        print("\nUnknown . option")
    return 1


class Terminal():
    def __init__(self, *args):
        self.args = [a for a in args]
        self.tty = 4  # 0
        self.pr_bf = ""
        self.key_buff = ""
        self.key_mode = -1

        # Buffer
        self.buff = None
        self.user = None

        # self.tty = 0
        # if self.tty == 4:
        #     self.initbbc()
        #     self.initscr()
        #     self.topscr()

    def set_user(self, user):
        self.user = user
        self.buff = user.buff

    @property
    def title(self):
        return self.args[0]

    def initscr(self):
        pass

    def btmscr(self):
        print("\\", "=" * 100, "/")
        pass

    def topscr(self):
        print("/", "=" * 100, "\\")
        pass

    def show_top(self):
        self.pbfr()
        if self.tty == 4:
            self.topscr()
        self.pbfr()

    def show_bottom(self):
        self.pbfr()
        if self.tty == 4:
            self.btmscr()
        self.pbfr()

    # ???
    def set_progname(self, p_id=0, title=""):
        """
        int x=0;
        int y=strlen(argv_p[n])+strlen(argv_p[1]);
        y++;
        if(strcmp(argv_p[n],text)==0) return;

        while(x<y)
            argv_p[n][x++]=0;
        strcpy(argv_p[n],text);
        """
        self.args[p_id] = title
        print(self.title)

    # ???
    def key_input(self, prmpt, max_len):
        self.key_mode = 0
        self.pr_bf = prmpt
        self.bprintf(prmpt)
        self.pbfr()
        self.buff.pr_due = False
        self.key_buff = input(prmpt)[:max_len]
        self.key_mode = -1
        return self.key_buff

    def key_reprint(self):
        self.buff.pr_qcr = True
        self.pbfr()
        if self.key_mode == 0 and self.pr_due:
            print("\n%s%s" % (self.pr_bf, self.key_buff))
        self.buff.pr_due = 0
        # fflush(stdout)

    def pbfr(self):
        self.buff.pbfr(self.user)

    def bprintf(self, text):
        self.buff.sysbuf += text

    def crapup(self, s):
        dashes = "\n-" + "=-" * 38
        self.pbfr()
        self.buff.pr_due = 0  # So we dont get a prompt after the exit
        print("%s\n\n%s\n%s" % (dashes, s, dashes))
        exit(0)

    def sendmsg(self, user=None):
        if user is None:
            user = self.user

        # Bottom screen
        self.show_bottom()

        # Set program title
        if user.player.vis > 9999:
            self.set_progname(
                title="-csh"
            )
        elif user.player.vis == 0:
            self.set_progname(
                title="   --}----- ABERMUD -----{--     Playing as %s" % user.name
            )

        # Input from keyboard
        alarm.sig_alon()
        work = self.key_input(user.prmpt, 80)
        alarm.sig_aloff()

        # Top screen
        self.show_top()
        self.bprintf("<l>%s\n</l>" % (work))

        # Read messages
        user.world.openworld()
        user.rte()
        user.world.closeworld()

        if user.convflg and work == "**":
            user.convflg = 0
            return self.sendmsg(user)
        if work:
            if work[0] == '*':
                work[0] = 32
            else:
                work = user.apply_convflg(work)
        if user.curmode == 1:
            gamecom(work)
        else:
            if work.lower() != ".q":
                a = special(work, user)
        user.fight_next_round()
        return work.lower() == ".q"


save_flag = dict()


# ???
STDIN = 0
# ???
ECHO = "ECHO"
# ???
ICANON = "ICANON"
# ???
TCSANOW = "TCSANOW"


# ???
class Termios():
    c_lflag = {
        ECHO: False,
        ICANON: False,
    }
    attrs = {
        TCSANOW: -1,
    }

    def tcsetattr(self, f, attr):
        self.attrs[attr] = f


# ???
def tcgetattr(f):
    logger().debug("<<< tcgetattr(%s, &ios)", f)
    return Termios


def keysetup():
    """
    struct sgttyb x;
    gtty(fileno(stdin),&x);
    save_flag=x.sg_flags;
    x.sg_flags&=~ECHO;
    x.sg_flags|=CBREAK;
    stty(fileno(stdin),&x);
    """
    global save_flag
    ios = tcgetattr(STDIN)
    save_flag = ios.c_lflag
    ios.c_lflag[ECHO] = True
    ios.c_lflag[ICANON] = True
    ios.tcsetattr(STDIN, TCSANOW)


def keysetback():
    """
    struct sgttyb x;
    if(save_flag== -1) return;
    gtty(fileno(stdin),&x);
    x.sg_flags=save_flag;
    stty(fileno(stdin),&x);
    """
    ios = tcgetattr(STDIN)
    ios.c_lflag = save_flag
    ios.tcsetattr(STDIN, TCSANOW)
