from .compiler import gcc


scripts = [
    "makeworld.c",
    "blib.c",
]
libs = [
    "crypt",
]
output = "makeworld.util"


def compile():
    gcc(scripts, output, libs=libs)
    return makeworld


def makeworld():
    print(">>> ./makeworld.util")
