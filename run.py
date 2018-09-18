from app import app
from db import db
from models.users import UserModel
from models.ideas import IdeaModel
from models.reviews import ReviewModel
from seeds.users import users
from seeds.ideas import ideas
from seeds.tags import tags
from seeds.reviews import reviews

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    db.engine.execute(UserModel.__table__.insert(), users)
    db.engine.execute(IdeaModel.__table__.insert(), ideas)
    
   
