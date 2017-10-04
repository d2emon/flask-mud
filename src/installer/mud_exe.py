from .compiler import gcc


obj = [
    "tk.o",
    "parse.o",
    "objsys.o",
    "extra.o",
    "magic.o",
    "blood.o",
    "weather.o",
    ">obdat.o",
    "new1.o",
    "support.o",
    "zones.o",
    "mobile.o",
    "bprintf.o",
    "bbc.o",
    ">blib.o",
    "opensys.o",
    "gamego.o",
    "ndebug.o",
    "key.o",
    "packer.o",
    "newuaf.o",
    "frob.o",
    ">flock.o",
]
incl = [
    "object.h",
    "files.h",
    "System.h",
]


def mud_1():
    for o in obj:
        c_o(o)
    print(obj)
    gcc(obj, "mud.exe", ["crypt", ])
    print(">>> chmod 700 mud.exe")


def c_o(c):
    gcc(c, "")


def compile():
    mud_1()
    print("%s: %s" % (obj, incl))
