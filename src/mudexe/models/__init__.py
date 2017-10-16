from app import db
from app.models import PagedQuery
# from auth.models import User
from sqlalchemy import desc
# from global_vars import logger


from .player import *
from .location import *


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

    @property
    def is_god(self):
        # return self.level > 9999
        return True


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
