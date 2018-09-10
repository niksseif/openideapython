from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.ideas import IdeaModel



parser = reqparse.RequestParser()
parser.add_argument('title',
type=str,
required=True,
help="This field cannot be left blank!"
)
parser.add_argument('label',
type=str,
required=True,
help="Every idea needs a label."
)

parser.add_argument('description',
type=str,
required=False
)

parser.add_argument('users_id',
type=int,
required=True,
help="ideas need users_id"
)


# this is class of one idea
class Idea(Resource):

    # @jwt_required
    def get(self, users_id: int):
        idea = IdeaModel.find_by_users_id(users_id)
        print(idea,'<<<<idea')
        if idea:
            return idea.json(), 200

        return {'message': 'Ideas of the user not found'}, 404

    @jwt_required
    def delete(self, idea_title):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        idea = IdeaModel.find_by_title(_title)
        if idea:
            idea.delete_from_db()
            return {'message': 'Idea deleted.'}
        return {'message': 'Idea not found.'}, 404

    def put(self, title):
        data = parser.parse_args()

        idea = IdeaModel.find_by_title(title)

        if idea:
            idea.title = data['title']
        else:
            idea = ideaModel(title, **data)

        idea.save_to_db()
        return idea.json()


class IdeaList(Resource):

    def get(self,users_id: int):
        user_id_Ideas = [idea.json() for idea in IdeaModel.find_by_users_id(users_id)]
        return user_id_Ideas, 200

        # label = IdeaModel.find_by_label(label)
        # if label:
        #     return label.json(), 200

        return {'message': 'Ideas of the user not found'}, 404


    @jwt_required
    def post(self):
        data = parser.parse_args()
        print(self)
        if IdeaModel.find_by_title(data.title):
            return {'message': "An beer with beer_name '{}' already exists.".format(title)}, 400
        print(data)

        idea = IdeaModel(**data)

        try:
            idea.save_to_db()
        except:
            return {"message": "An error occurred while inserting the idea."}, 500

        return idea.json(), 201