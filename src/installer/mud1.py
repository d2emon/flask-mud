from .compiler import gcc


obj = [
    ">blib.o",
    "gmain2.o",
    "gmainstubs.o",
    "gmlnk.o",
    ">obdat.o",
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
    gcc(obj, "mud.1", ["crypt", ])
    print(">>> strip mud.1")
    print(">>> chmod 4711 mud.1")


def c_o(c):
    gcc(c, "")


def compile():
    mud_1()
    print("%s: %s" % (obj, incl))
