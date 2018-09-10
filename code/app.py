import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from db import db


from models.users import UserModel
from models.ideas import IdeaModel



from resources.users import UserRegister, User, UserLogin
from resources.ideas import Idea, IdeaList


from seeds.users import users
from seeds.ideas import ideas
from seeds.tags import tags
from seeds.reviews import reviews







app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)



app.config['JWT_SECRET_KEY']= 'nikki' # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)



@app.before_first_request
def create_tables():
        # db.drop_all()
        db.create_all()
        db.engine.execute(UserModel.__table__.insert(), users)
        db.engine.execute(IdeaModel.__table__.insert(), ideas)
        # db.engine.execute(ReviewModel.__table__.insert(), reviews)
        # db.engine.execute(TagsModel.__table__.insert(), tags)



@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin,'/login')
api.add_resource(User,'/user/<int:user_id>/ideas')
# api.add_resource(IdeaModel, '/ideas/<int:ideas_id>')
# api.add_resource(Idea,'/ideas/<int:users_id>')
# api.add_resource(IdeaList, '/ideas')
# api.add_resource(IdeaList, '/user/<int:user_id>/ideas')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
