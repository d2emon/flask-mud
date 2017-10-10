import logging


__logger = logging.getLogger("installer")


def set_logger(new_logger):
    global __logger
    __logger = new_logger


def logger():
    return __logger
