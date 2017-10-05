from global_vars import logger


class World():
    # ???
    maxu = 255

    def __init__(self):
        self.players = [None] * self.maxu

    # ???
    def openworld(self):
        logger().debug("<<< openworld()")
        return True

    # ???
    def closeworld(self):
        logger().debug("<<< closeworld()")

    def find_empty(self):
        for p in len(self.players):
            if self.players[p] is None:
                return p
        return self.maxu
