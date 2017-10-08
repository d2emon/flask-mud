"""
Key drivers
"""
from global_vars import logger
from ..gamego.signals import alarm
from .exceptions import Crapup


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
        c_start = chr(int("2517", 16))
        c_fill = chr(int("2501", 16))
        c_finish = chr(int("251B", 16))
        print(c_start + c_fill * 100 + c_finish)

    def topscr(self):
        c_start = chr(int("250F", 16))
        c_fill = chr(int("2501", 16))
        c_finish = chr(int("2513", 16))
        print(c_start + c_fill * 100 + c_finish)

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
        border = chr(int("2503", 16))
        print(border + "\t" + self.title + "\t" + border)

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
        raise Crapup(s, terminal=self)

    def sendmsg(self, user=None):
        if user is None:
            user = self.user

        # Bottom screen
        self.show_bottom()

        # Set program title
        if user.player.visibility > 9999:
            self.set_progname(
                title="-csh"
            )
        elif user.player.visibility == 0:
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

    def getkbd(self, l):
        """
        Getstr() with length limit and filter ctrl
        """
        return input()[:l]
