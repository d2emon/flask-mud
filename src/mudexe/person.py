from .models import Person


def delpers(user):
    x = Person.by_user(user).all()
    if x is None:
        return
    x.delete()


def validname(user):
    if resword(user.name):
        user.buff.bprintf("Sorry I cant call you that\n")
        return False
    if len(user.name) > 10:
        return False
    a = 0
    while user.name[a]:
        if user.name[a] == ' ':
            return False
        a += 1
    if user.world.fobn(user.name) is None:
        user.buff.bprintf("I can't call you that , It would be confused with an object\n")
        return False
    return True


def resword(name):
    return name in [
        "The",
        "Me",
        "Myself",
        "It",
        "Them",
        "Him",
        "Her",
        "Someone",
    ]
