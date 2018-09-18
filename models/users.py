from db import db
import uuid
from seeds.users import users



class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    hashedPassword = db.Column(db.String(150))
    image_url = db.Column(db.String(150))
    ideas = db.relationship('IdeaModel',lazy='dynamic')
    reviews = db.relationship('ReviewModel', lazy='dynamic')
    
   
    def __init__(self, name, email, hashedPassword, image_url= 'https://www.w3schools.com/howto/img_avatar2.png'):
        self.name = name
        self.email = email
        self.hashedPassword = hashedPassword
        self.image_url = image_url
        

# create json method to return in the url
    def json(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'hashedPassword':self.hashedPassword,
            'image_url':self.image_url,
            'ideas': [idea.json() for idea in self.ideas.all()]
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
