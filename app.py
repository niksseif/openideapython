import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from models.users import UserModel
from models.ideas import IdeaModel
from models.reviews import ReviewModel


from blacklist import BLACKLIST
from resources.users import UserRegister, User, UserLogin
from resources.ideas import Idea, IdeaList
from resources.reviews import Reviews

from seeds.users import users
from seeds.ideas import ideas
from seeds.tags import tags
from seeds.reviews import reviews




app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://animals:postgres@localhost/openidea_py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

app.config['JWT_SECRET_KEY']= 'nikki' # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)

# `claims` are data we choose to attach to each jwt payload
# and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
# one possible use case for claims are access level control, which is shown below
# """
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends


# # @app.before_first_request
# def create_tables():
#         db.drop_all()
#         db.create_all()
#         db.engine.execute(UserModel.__table__.insert(), users)
#         db.engine.execute(IdeaModel.__table__.insert(), ideas)
#         db.engine.execute(ReviewModel.__table__.insert(), reviews)



api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin,'/login')
api.add_resource(User,'/user/<int:user_id>/ideas')  #route is for getting/posting to the idea
api.add_resource(IdeaList, '/ideas')
api.add_resource(Idea, '/idea') #route is for editting one idea of a user,put
api.add_resource(Reviews, '/reviews') #route is for getting all the reviews for one idea, post to it and delete

# @app.before_first_request
# def create_tables():
#     print("Dropping, migrating, seeding")
#     db.drop_all()
#     db.create_all()
#     db.engine.execute(UserModel.__table__.insert(), users)
#     db.engine.execute(IdeaModel.__table__.insert(), ideas)
#     db.engine.execute(ReviewModel.__table__.insert(), reviews)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
