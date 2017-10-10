"""
Key drivers
"""
from global_vars import logger
from ..gamego.signals import alarm
from ..models import SEX_MALE, SEX_FEMALE
from .exceptions import Crapup


sexes = {
    'm': SEX_MALE,
    'f': SEX_FEMALE,
}


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
        # user.terminal = self
        self.user = user
        self.buff = user.buff

    @property
    def input_text(self):
        res = self.__input_text
        self.__input_text = ""
        return res

    @property
    def title(self):
        return self.args[0]

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

    def initscr(self):
        pass

    def btmscr(self):
        pass

    def topscr(self):
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

    def get_prmpt(self, prmpt):
        self.key_mode = 0
        self.pr_bf = prmpt
        self.bprintf(prmpt)
        self.pbfr()
        self.buff.pr_due = False
        self.prmpt = prmpt
        return prmpt

    def key_input(self, prmpt, max_len):
        self.get_prmpt(prmpt)
        self.key_buff = self.input_text[:max_len]
        self.key_mode = -1
        return self.key_buff

    def key_reprint(self):
        self.buff.pr_qcr = True
        res = self.pbfr()
        if self.key_mode == 0 and self.pr_due:
            res += "\n%s%s" % (self.pr_bf, self.key_buff)
        self.buff.pr_due = 0
        # fflush(stdout)
        return res

    def bprintf(self, text):
        self.buff.sysbuf += text

    def pbfr(self):
        return self.buff.pbfr(self.user)

    def crapup(self, s):
        raise Crapup(s, terminal=self)

    def sendmsg_before(self, user=None):
        if user is None:
            user = self.user

        program_title = None
        if user.player.visibility > 9999:
            program_title = "-csh"
        elif user.player.visibility == 0:
            program_title = "   --}----- ABERMUD -----{--     Playing as %s" % user.name

        # Bottom screen
        self.show_bottom()

        # Set program title
        if program_title is not None:
            self.set_progname(
                title=program_title
            )

        # Input from keyboard
        alarm.sig_alon()
        return self.get_prmpt(user.prmpt)

    def sendmsg_after(self, input_text="", user=None):
        work = input_text
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
        return self.input_text[:l]

    def asksex(self):
        sex = None
        while sex is None:
            self.bprintf("\nSex (M/F) : ")
            self.pbfr()
            # self.terminal.keysetback()
            sex_id = self.getkbd(1).lower()
            # self.terminal.keysetup()
            sex = sexes.get(sex_id)
            if sex is None:
                self.bprintf("M or F")
        return sex


class CliTerminal(Terminal):
    @property
    def input_text(self):
        res = self.__input_text
        self.__input_text = input(self.prmpt)
        return res

    def set_progname(self, p_id=0, title=""):
        Terminal.set_progname(self, p_id, title)
        border = chr(int("2503", 16))
        print(border + "\t" + self.title + "\t" + border)

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

    def key_reprint(self):
        res = Terminal.key_reprint(self)
        print(res)
        return res

    def send_msg(self, user):
        self.sendmsg_before(user)
        work = self.key_input(user.prmpt, 80)
        self.sendmsg_after(work, user)


class PageTerminal(Terminal):
    def __init__(self, *args):
        Terminal.__init__(self, *args)
        self.prmpt = "?"
        self.__input_text = ""
        self.text = ""

    @property
    def input_text(self):
        res = self.__input_text
        self.__input_text = "???\n"
        return res

    def key_reprint(self):
        res = Terminal.key_reprint(self)
        self.text += res
        return res

    def pbfr(self):
        res = self.buff.pbfr(self.user)
        self.text += res
        return res

    def asksex(self):
        sex = None
        while sex is None:
            self.bprintf("\nSex (M/F) : ")
            self.pbfr()
            # self.terminal.keysetback()
            sex_id = self.getkbd(1).lower()
            # self.terminal.keysetup()
            sex = sexes.get(sex_id)
            if sex is None:
                self.bprintf("M or F")
        return sex

    def do_loop(self):
        self.pbfr()
        self.sendmsg_before(self.user)

    def on_text(self, text):
        self.sendmsg_after(text, self.user)

        if self.buff.rd_qd:
            self.user.rte()
        self.buff.rd_qd = False

        self.user.world.closeworld()
        self.pbfr()

    def next_turn(self):
        self.user.next_turn()
        self.key_reprint()
