from .compiler import gcc


scripts = [
    "makeuaf.c"
]
libs = [
]
output = "makeuaf"


def compile():
    gcc(scripts, output, libs=libs)
    return makeuaf


def makeuaf(dst):
    print(">>> ./makeuaf >%s" % (dst, ))
