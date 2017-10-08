from app import db
from app.models import PagedQuery
from sqlalchemy import desc

SEX_MALE = 0
SEX_FEMALE = 1


class PersonQuery(PagedQuery):
    def by_user(self, user=None):
        '''
        Return block data for user or -1 if not exist
        '''
        if user is None:
            user_id = 0
        else:
            user_id = user.id

        return self.filter_by(user_id=user_id)


class User(db.Model):
    """
    Create a User table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), info={'label': "Name"})

    def save(self):
        db.session.add(self)
        db.session.commit()


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
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Player(db.Model):
    """
    Create a Player model
    """
    id = db.Column(db.Integer, primary_key=True)  # ct
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(32), info={'label': "Name"})
    location = db.Column(db.Integer, default=0, info={'label': "Location"})  # loc
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))  # pos
    level = db.Column(db.Integer, default=1, info={'label': "Level"})  # lev
    visibility = db.Column(db.Integer, default=0, info={'label': "Visibility"})  # vis
    strength = db.Column(db.Integer, default=-1, info={'label': "Strength"})  # str
    weapon = db.Column(db.Integer, default=-1, info={'label': "Weapon"})  # wpn
    helping = db.Column(db.Integer, default=-1, info={'label': "Helping"})  # helping
    sex = db.Column(db.Integer, default=0, info={'label': "Sex"})

    user = db.relationship('User', backref='players')
    last_message = db.relationship('Message')


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
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_code = db.Column(db.Integer, default=0, info={'label': "Code"})
    text = db.Column(db.String(255), info={'label': "Text"})

    from_user = db.relationship('User', backref='sent', foreign_keys=[from_user_id])
    to_user = db.relationship('User', backref='recieved', foreign_keys=[to_user_id])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return "<%d>" % (self.message_code)

    def is_text(self):
        return self.message_code >= -3
