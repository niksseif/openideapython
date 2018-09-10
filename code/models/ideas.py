from db import db
from seeds.ideas import ideas
# from models.reviews import ReviewsModel
from models.users import UserModel





class IdeaModel(db.Model):
    __tablename__ = 'Ideas'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(1000))
    label = db.Column(db.String(250))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    users = db.relationship('UserModel')
    averageRating = db.Column(db.Integer)
   

    def __init__(self, title, label, users_id,description ='none'):
        self.title = title
        self.description = description
        self.label = label
        self.users_id = users_id




    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    @classmethod
    def find_by_label(cls,):
        return cls.query.filter_by(lable=label)
    
    @classmethod
    def find_by_users_id(cls,users_id):
        return cls.query.filter_by(users_id=users_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()