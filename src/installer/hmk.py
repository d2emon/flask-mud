from .compiler import gcc


scripts = [
    "make.h.c"
]
libs = [
]
output = "hmk"


def compile():
    gcc(scripts, output, libs=libs)
    return hmk


def hmk(dst):
    print(">>> ./hmk >%s" % (dst, ))
