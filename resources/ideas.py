from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.ideas import IdeaModel



parser = reqparse.RequestParser()

parser.add_argument('users_id',
                    type=int,
                    required=True,
                    help="Every idea needs a users_id"
                    )

parser.add_argument('title',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )

parser.add_argument('description',
                    type=str,
                    required=False
                    )

parser.add_argument('image_url',
                    type=str,
                    required=False
                    )

parser.add_argument('label',
                    type=str,
                    required=True,
                    help="Every idea needs a label."
                    )

# parser.add_argument('vote',
#                     type=int,
#                     required=False
#                     )


# this is class of one idea
class Idea(Resource):

    # @jwt_required
    def get(self,idea_id:int):
        idea = IdeaModel.find_by_id(idea_id)
        print(idea,'<<<<idea')
        if idea:
            return idea.json(), 200

        return {'message': 'Ideas of the user not found'}, 404

    #  add post to this class to be able to create an idea
    def post(self,name):
        if IdeaModel.find_by_name:
            return {"message": "An idea with name '{}' already exist.".format(name)},400
        
        data =self.parser.parse_args()
        idea = IdeaModel(name,**data)

        try:
            idea.save_to_db
        except:
            return {"message": "An error occured while inserting the idea"}


    @jwt_required
    def delete(self, title):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        idea = IdeaModel.find_by_title(title)
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
            idea = IdeaModel(title, **data)

        idea.save_to_db()
        return idea.json()
    

    

class IdeaList(Resource):
    def get(self):
        ideas = [idea.json() for idea in IdeaModel.find_all()]
        # print(ideas,"<<<<<ideas from resource file")
        return ideas, 200

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        print(self,"<<<self from post")
        if IdeaModel.find_by_title(data.title):
            print(data.title,"<<<<<<")
            return {'message': "An idea with idea_name '{}' already exists.".format(data.title)}, 400
        print(data)
        idea = IdeaModel(**data) 

        try:
            idea.save_to_db()
        except:
            return {"message": "An error occurred while inserting the idea."}, 500

        return idea.json(), 201
