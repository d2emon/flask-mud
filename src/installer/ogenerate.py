from global_vars import logger
from blib import sec_write


class GameObject():
    def __init__(self, location=0, v1=0, flags=[], v3=0):
        self.location = location
        self.v1 = v1
        self.flags = flags
        self.bin_flags = []
        self.v3 = v3

    def __str__(self):
        return "<GameObject at %s, %s, %s, %s>" % (
            [self.location, ],
            [self.v1, ],
            [
                self.flags,
                self.bin_flags
            ],
            [self.v3, ],
        )

    def set_flagstr(self, flagstr):
        print("Input line is %s" % (flagstr))
        flags = flagstr.split(":")
        for i in range(len(flags), 3):
            flags.append(0)
        self.binproc(flags[2])
        print("Result=%s" % (flags))
        self.flags = flags

    def binproc(self, flags):
        if not flags:
            self.bin_flags = []
            return []
        # b = [False, ] * 32
        b = []
        for i, a in enumerate(flags):
            # b[i] = (int(a) > 0)
            b.append(int(a) > 0)
        print("Binproc of %s is %s\n" % (flags, b))
        self.bin_flags = b
        return b


def load():
    blob = []
    ctt = 0
    with open("ob.in", "r") as a:
        c = True
        obj = []
        o = None
        while c:
            c = a.readline().strip()
            if ctt % 4 == 0:
                o = GameObject(location=c)
            elif ctt % 4 == 1:
                o.v1 = c
            elif ctt % 4 == 2:
                o.set_flagstr(c)
            else:
                o.v3 = c
                blob.append(o)
            ctt += 1
    for b in blob:
        print(b)
    return blob


def save(blob):
    with open("ob.out", "w") as a:
        sec_write(a, blob, 0, len(blob))


def ogenerate():
    logger().debug(">>> ./ogenerate")
    save(load())
