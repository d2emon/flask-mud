from app import db
from app.models import PagedQuery
# from global_vars import logger


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

    @classmethod
    def initme(cls, user, sex=0):
        person = cls.query.by_user(user)
        if person:
            return person

        # self.buff.bprintf("Creating character....")
        person = cls(user=user)
        person.sex = sex  # self.terminal.asksex()
        person.save()
        return person

    def saveme(self, user=None, zapped=False):
        if zapped:
            return
        if user is not None:
            # self.strength = user.my_str
            # self.level = user.my_lev
            self.sex = user.player.sex
            # self.person.sco = user.my_sco
            if user.zapped:
                return
            user.buff.bprintf("\nSaving %s\n" % (self.name))
        self.save()

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
