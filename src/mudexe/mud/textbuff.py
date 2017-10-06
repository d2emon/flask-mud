from global_vars import logger


class TextBuffer():
    rd_qd = False
    # ???
    sysbuf = ""

    def __init__(self):
        self.makebfr()

    # ???
    def makebfr(self):
        logger().debug("<<< makebfr()")

    # ???
    def pbfr(self):
        logger().debug("<<< pbfr()")

    # ???
    def bprintf(self, msg):
        logger().debug("<<< bprintf(%s)", msg)
