from global_vars import logger


class MudUnaviable(Exception):
    """
    crapup("Sorry AberMUD is currently unavailable")
    """


class MudFull(Exception):
    """
    print("\nSorry AberMUD is full at the moment")
    """


class World():
    # ???
    maxu = 255

    def __init__(self):
        self.players = [None] * self.maxu

    # ???
    def openworld(self):
        logger().debug("<<< openworld()")
        # raise MudUnaviable()
        return True

    # ???
    def closeworld(self):
        logger().debug("<<< closeworld()")

    def find_empty(self, player):
        for p in range(len(self.players)):
            if self.players[p] is None:
                self.players[p] = player
                return p
        raise MudFull()
