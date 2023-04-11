from flask_restful import Resource, reqparse
from security import authenticate


class Auth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)

    parser.add_argument('password',
                        type=str)

    def post(self):
        data = Auth.parser.parse_args()
        authenticated = authenticate(data['username'], data['password'])

        if authenticated:
            return {'message': 'User authenticated successfully.'}, 201
        else:
            return {'message': "Not authenticated"}
