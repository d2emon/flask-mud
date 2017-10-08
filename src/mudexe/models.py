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
            name = ""
        else:
            name = user.name.lower()

        return self.filter_by(name=name)


class Person(db.Model):
    """
    Create a Person table
    """
    query_class = PersonQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), info={'label': "Name"})
    score = db.Column(db.Integer, default=0, info={'label': "Score"})
    strength = db.Column(db.Integer, default=40, info={'label': "Strength"})
    sex = db.Column(db.Integer, default=0, info={'label': "Sex"})
    level = db.Column(db.Integer, default=1, info={'label': "Level"})

    def __repr__(self):
        return self.name

    def decpers(self, user):
        # user.name = self.name
        user.my_str = self.strength
        user.my_sco = self.score
        user.my_lev = self.level
        user.my_sex = self.sex

    def save(self):
        db.session.add(self)
        db.session.commit()
