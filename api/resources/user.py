from flask_restful import Resource, reqparse
from api.database_handlers.user_database_handler import UserDatabaseHandler
from api.models.usermodel import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)

    parser.add_argument('password',
                        type=str)

    parser.add_argument("percentage",
                        type=int)

    parser.add_argument("quiz_name",
                        type=str)

    def get(self, name):
        handler = UserDatabaseHandler()
        stats = handler.get_stats(name)

        return stats

    def post(self, name):
        handler = UserDatabaseHandler()
        data = User.parser.parse_args()
        if handler.get_by_username(name):
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(name, data['password'])

        handler.save_user_to_db(user)

        return {'message': 'User created successfully.'}, 201

    def put(self, name):
        handler = UserDatabaseHandler()
        data = User.parser.parse_args()

        handler.add_quiz_to_user(name, data['quiz_name'], data['percentage'])
        handler.update_user(data['percentage'], name)

        return {"message": "Stats updated."}, 201
