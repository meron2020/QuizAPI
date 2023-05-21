from flask_restful import Resource, reqparse

from api.database_handlers.user_database_handler import UserDatabaseHandler


class Scoring(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('quiz',
                        type=str)

    def get(self):
        handler = UserDatabaseHandler()
        return handler.get_all_averages(), 200
