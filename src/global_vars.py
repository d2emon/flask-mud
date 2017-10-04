import logging


__logger = logging.getLogger("installer")


def set_logger(new_logger):
    global __logger
    print("LOGGER")
    print(__logger)
    __logger = new_logger
    print(__logger)
    __logger.debug("TEST")
    print("LOGGED")


def logger():
    return __logger
