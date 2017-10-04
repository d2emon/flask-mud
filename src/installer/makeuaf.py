from global_vars import logger


class UafBeing():
    def __init__(self, name=""):
        self.name = name
        self.score = 0
        self.strength = 0
        self.sex = 0
        self.level = 0


def makeuaf(dst):
    logger().debug(">>> ./makeuaf >%s" % (dst, ))
    x = UafBeing()
    x.sex = 0
    x.level = 10033
    x.score = 0
    x.strength = 100
    x.name = "Debugger"
    logger().debug(">>> fwrite(&%s, 1, sizeof(%s), stdout);" % (x, x))
