from os import path


CONFIG = {
    "UAF_RAND": "uaf.rand",
    "ROOMS": path.join("TEXT", "ROOMS", ""),
    "LOG_FILE": "mud_syslog",
    "BAN_FILE": "banned_file",
    "NOLOGIN": "nologin",
    "RESET_T": "reset_t",
    "RESET_N": "reset_n",
    "RESET_DATA": "reset_data",
    "MOTD": path.join("TEXT", "gmotd2"),
    "GWIZ": path.join("TEXT", "gwiz"),
    "HELP1": path.join("TEXT", "help1"),
    "HELP2": path.join("TEXT", "help2"),
    "HELP3": path.join("TEXT", "help3"),
    "WIZLIST": path.join("TEXT", "wiz.list"),
    "CREDITS": path.join("TEXT", "credits"),
    "EXAMINES": path.join("EXAMINES", ""),
    "LEVELS": path.join("TEXT", "level.txt"),
    "PFL": "user_file",
    "PFT": "user_file.b",
    "EXE": "mud.exe",
    "EXE2": "mud.1",
    "SNOOP": path.join("SNOOP", ""),
}


def packitems(wd):
    settings = dict()
    for k, v in CONFIG.items():
        p = path.join(wd, v)
        settings[k] = p
    return settings


def hmk():
    wd = "/"  # getwd()
    settings = packitems(wd)
    host = "gethostname" * 50  # gethostmachine(31)
    settings["HOST_MACHINE"] = host[:31]
    for k, v in settings.items():
        print("#define %s \"%s\"" % (k, v))
    return settings
