"""
World Creator
"""
from global_vars import logger
from blib import sec_write


def makeworld(filename="_usr_tmp_-iy7AM"):
    logger().debug("./makeworld.util")

    x = [[1, 1], ] + [0, ] * 600
    with open(filename, "w") as a:
        sec_write(a, x, 0, 64)
