from .compiler import gcc


scripts = [
    "ogen.c",
    "blib.o",
]
libs = [
    "crypt",
]
output = "ogenerate"


def compile():
    gcc(scripts, output, libs=libs)
    return ogenerate


def ogenerate():
    print(">>> ./ogenerate")
