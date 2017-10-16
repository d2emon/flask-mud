from app import db
from app.models import PagedQuery
# from auth.models import User
from sqlalchemy import desc
from global_vars import logger


from ..objsys import Item


from .location import *


SEX_MALE = 0
SEX_FEMALE = 1


LEVEL_NAMES = {
    1: ["The Novice", ],
    2: ["The Adventurer", "The Adventuress"],
    3: ["The Hero", "The Heroine"],
    4: ["The Champion", ],
    5: ["The Conjurer", "The Conjuress"],
    6: ["The Magician", ],
    7: ["The Enchanterress", "The Enchantress"],
    8: ["The Sorceror", "The Sorceress"],
    9: ["The Warlock", ],
    10: ["The Apprentice Wizard", "The Apprentice Witch"],
    11: ["The 370", ],
    12: ["The Hilbert-Space", ],
    14: ["The Completely Normal Naughty Spud", ],
    15: ["The Wimbledon Weirdo", ],
    16: ["The DangerMouse", ],
    17: ["The Charred Wizzard", "The Charred Witch"],
    18: ["The Cuddly Toy", ],
    19: ["Of The Opera", ],
    20: ["The 50Hz E.R.C.S", ],
    21: ["who couldn't decide what to call himself", ],
    22: ["The Summoner", ],
    10000: ["The 159 IQ Mega-Creator", ],
    10033: ["The Arch-Wizard", "The Arch-Witch"],
    10001: ["The Arch-Wizard", "The Arch-Witch"],
    10002: ["The Wet Kipper", ],
    10003: ["The Thingummy", ],
    68000: ["The Wanderer", ],
    -2:  ["\010", ],
    -11: ["The Broke Dwarf", ],
    -12: ["The Radioactive Dwarf", ],
    -10: ["The Heavy-Fan Dwarf", ],
    -13: ["The Upper Class Dwarven Smith", ],
    -14: ["The Singing Dwarf", ],
    -30: ["The Sorceror", ],
    -31: ["the Acolyte", ],
}


# ???
def seeplayer(p):
    logger().debug("<<< seeplayer(%s)", p)
    return True


class PersonQuery(PagedQuery):
    def by_user(self, user=None):
        '''
        Return block data for user or -1 if not exist
        '''
        if user is None:
            user_id = 0
        else:
            user_id = user.id

        return self.filter_by(user_id=user_id).first()


class Person(db.Model):
    """
    Create a Person table
    """
    query_class = PersonQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, default=0, info={'label': "Score"})
    strength = db.Column(db.Integer, default=40, info={'label': "Strength"})
    sex = db.Column(db.Integer, default=0, info={'label': "Sex"})
    level = db.Column(db.Integer, default=1, info={'label': "Level"})

    user = db.relationship('User', backref='persons')

    def __repr__(self):
        return self.user.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def is_wizzard(self):
        # return self.level > 9
        return True


class PlayerQuery(PagedQuery):
    def by_user(self, user=None):
        '''
        Return block data for user or -1 if not exist
        '''
        if user is None:
            user_id = 0
        else:
            user_id = user.id

        return self.filter_by(user_id=user_id).first()

    def fpbns(self, name):
        return self.filter_by(name=name).first()

    def fpbn(self, name):
        player = self.fpbns(name)
        if player is None:
            return None
        if not seeplayer(player):
            return None
        return player


class Player(db.Model):
    """
    Create a Player model
    """
    query_class = PlayerQuery

    id = db.Column(db.Integer, primary_key=True)  # ct
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(32), info={'label': "Name"})  # 0
    location = db.Column(db.Integer, default=0, info={'label': "Location"})  # loc 4
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))  # pos 5
    level = db.Column(db.Integer, default=1, info={'label': "Level"})  # lev 10
    visibility = db.Column(db.Integer, default=0, info={'label': "Visibility"})  # vis 8
    strength = db.Column(db.Integer, default=-1, info={'label': "Strength"})  # str 7
    weapon = db.Column(db.Integer, default=-1, info={'label': "Weapon"})  # wpn 11
    helping = db.Column(db.Integer, default=-1, info={'label': "Helping"})  # helping 13
    sex = db.Column(db.Integer, default=SEX_MALE, info={'label': "Sex"})  # sex 9

    user = db.relationship('User', backref='players')
    last_message = db.relationship('Message', foreign_keys=[message_id, ])

    has_farted = False

    def puton(self, game_user=None):
        if self.user:
            self.name = self.user.username
        if game_user is not None:
            self.name = game_user.name
            self.location = game_user.location
        self.last_message = None
        self.level = 1
        self.visibility = 0
        self.strength = -1
        self.weapon = -1
        self.sex = SEX_MALE
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def showto(self, user):
        if self == user.player:
            return False
        if not self.name:
            return False
        # if self.location != user.location:
        #     return False
        # if not user.seeplayer(self):
        #     return False
        return self

    def show_name(self, debug_mode=False):
        name = self.name
        if debug_mode:
            name = "%s{%d}" % (name, self.id)

        return "%s %s" % (
            name,
            self.level_name,
        )

    @property
    def level_name(self):
        """
        disl4
        """
        level_names = LEVEL_NAMES
        if self.has_farted:
            level_names[19] = ["Raspberry Blower Of Old London Town", ]
        l = level_names.get(self.level)
        if l is None:
            return "The Cardboard Box"
        if len(l) < 2:
            return l[0]
        else:
            return l[self.sex]

    def lobjsat(self, user):
        return self.aobjsat(user)

    def aobjsat(self, user):
        """
        Carried Loc !
        """
        res = []
        objects = [Item()] * 10
        for c in objects:
            c.carrf = 1
            c.loc = user
            c.name = "Item"

            if not c.iscarrby(user, user.person.is_wizzard):
                continue

            # o_txt = c.short_name(user, debug_mode=debug_mode)
            res.append(c)
        return res


class MessageQuery(PagedQuery):
    def findfirst(self):
        '''
        Return block data for user or -1 if not exist
        '''
        msg = self.order_by(Message.id).first()
        if msg:
            return msg.id
        return 0

    def findend(self):
        '''
        Return block data for user or -1 if not exist
        '''
        msg = self.order_by(desc(Message.id)).first()
        if msg:
            return msg.id
        return 0

    def readmsg(self, msg_id):
        return self.order_by(Message.id).filter(Message.id > msg_id)


class Message(db.Model):
    """
    Create a Message table
    """
    query_class = MessageQuery

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    message_code = db.Column(db.Integer, default=0, info={'label': "Code"})
    text = db.Column(db.String(255), info={'label': "Text"})

    from_player = db.relationship('Player', backref='sent', foreign_keys=[from_user_id])
    to_player = db.relationship('Player', backref='recieved', foreign_keys=[to_user_id])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return "<%d>" % (self.message_code)

    def is_text(self):
        return self.message_code >= -3


"""
#include "object.h"
#include <stdio.h>
#include "files.h"

extern FILE* openlock();
 /*

 Some more basic functions


 Note

 state(obj)
 setstate(obj,val)
 destroy(obj)

 are elsewhere

 */
extern OBJECT objects[];



ptothlp(pl)
{
int tot;
extern long maxu;
int ct=0;
while(ct<maxu)
{
if(ploc(ct)!=ploc(pl)){ct++;continue;}
if(phelping(ct)!=pl){ct++;continue;}
return(ct);
}
return(-1);
}


psetflg(ch,x)
long ch;
long x;
{
extern long ublock[];
ublock[16*ch+9]|=(1<<x);
}

pclrflg(ch,x)
long ch;
long x;
{
extern long ublock[];
ublock[16*ch+9]&=~(1<<x);
}

/*Pflags

0 sex
1 May not be exorcised ok
2 May change pflags ok
3 May use rmedit ok
4 May use debugmode ok
5 May use patch
6 May be snooped upon

*/

ptstbit(ch,x)
long ch;
long x;
{
return(ptstflg(ch,x));
}


ptstflg(ch,x)
long ch;
long x;
{
extern long ublock[];
extern char globme[];
if((x==2)&&(strcmp(globme,"Debugger")==0)) return(1<<x);
return(ublock[16*ch+9]&(1<<x));
}
"""