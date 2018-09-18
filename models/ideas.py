from db import db
from seeds.ideas import ideas
from models.users import UserModel
from models.reviews import ReviewModel





class IdeaModel(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')
    title = db.Column(db.String(80))

    description = db.Column(db.String(1000))
    image_url = db.Column(db.String(150))
    label = db.Column(db.String(250))
    vote = db.Column(db.Integer)
   
    
    def __init__(self, vote, users_id, title, image_url, label, description='none'):
        self.users_id = users_id
        self.title = title
        self.description = description
        self.image_url = image_url
        self.label = label
        self.vote = vote


    def json(self):
            return {
                'id':self.id,
                'users_id': self.users_id,
                'title': self.title,
                'description': self.description,
                'image_url': self.image_url,
                'label':self.label,
                'vote': self.vote
            }


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    @classmethod
    def find_by_label(cls,label):
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
