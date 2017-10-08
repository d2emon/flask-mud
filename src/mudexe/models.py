from app import db
from app.models import PagedQuery


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
