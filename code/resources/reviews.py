from flask_restful import Resource, reqparse
from models.reviews import ReviewModel




parser = reqparse.RequestParser()
parser.add_argument('users_id',
                    type=int,
                    required=True,
                    help="Every review needs a users_id"
                    )

parser.add_argument('ideas_id',
                    type=int,
                    required=True,
                    help="Every review needs a idea_id"
                    )

parser.add_argument('review_title',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )

parser.add_argument('review_body',
                    type=str,
                    required=False
                    )

parser.add_argument('rating',
                    type=int,
                    required=False,
                    help="Every review needs rating"
                    )

parser.add_argument('image_url',
                    type=str,
                    required=False
                    )

parser.add_argument('vote',
                    type=int,
                    required=False
                    )


class Reviews(Resource):
    def get(self):
        reviews = [review.json() for review in ReviewModel.find_all()]
        # print(ideas,"<<<<<ideas from resource file")
        return reviews, 200

    def post(self):
        data = self.parser.parse_args()
        review = ReviewModel(**data)

        if ReviewModel.find_by_user_id_and_ideas_id(data['users_id'], data['ideas_id']):
            print('You are kidding me pls work')
            return {"message": "You Have already reviewed this idea!"}, 400

        try:
            review.save_to_db()
        except:
            return {"message": "An error occurred reviewing this idea."}, 500

        return review.json(), 201

    def delete(self, users_id):
        review = ReviewModel.find_by_users_id(users_id)
        if review:
            review.delete_from_db()
            return {'message': 'review deleted.'}
        return {'message': 'review not found.'}, 404

        
