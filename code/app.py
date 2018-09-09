from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask import Flask, jsonify

# this is importing models into the app
from models.users import UsersModel
# from models.ideas import IdeasModel
# from models.reviews import ReviewsModel
# from models.tags import TagsModel


# this section is importing resources into the app

# from resources.users import UserRegister, UserLogin, User, TokenRefresh, UserLogout
# from resources.ideas import Ideas, IdeasList
# from resources.reviews import Reviews, ReviewList
# from resources.tags import Tags

# this section is importing seeds into app
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







if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
