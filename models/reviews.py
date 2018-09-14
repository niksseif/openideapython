from db import db
from seeds.reviews import reviews






class ReviewModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('UserModel')
    idea = db.relationship('IdeaModel')
    ideas_id = db.Column(db.Integer, db.ForeignKey('ideas.id', ondelete='SET NULL'))
    review_title = db.Column(db.String(250))
    review_body = db.Column(db.String(250))
    rating = db.Column(db.Integer, default=1)
    image_url = db.Column(db.String(250))


    def __init__(self, users_id, ideas_id, review_title, review_body, rating, image_url):
            self.users_id = users_id
            self.ideas_id = ideas_id
            self.review_title = review_title
            self.review_body = review_body
            self.rating = rating
            self.image_url = image_url

    
    def json(self):
        return {
            'id': self.id,
            'users_id': self.users_id,
            'ideas_id': self.ideas_id,
            'review_title': self.review_title,
            'review_body': self.review_body,
            'image_url': self.image_url,
            'rating': self.rating
            }

    
    @classmethod
    def find_by_ideas_id(cls, ideas_id):
        return cls.query.filter_by(ideas_id=ideas_id).all()

    @classmethod
    def find_by_users_id(cls, users_id):
        return cls.query.filter_by(users_id=users_id).all()

    @classmethod
    def find_by_users_id_and_ideas_id(cls, users_id, ideas_id):
        return cls.query.filter_by(users_id=users_id, ideas_id=ideas_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
