from .global_vars import logger


def gcc(src, dst, libs=[]):
    logger().debug("gcc -w %s -o %s -l%s" % (src, dst, libs))
