import base64
import json

from flask_restful import Resource, reqparse

from api.database_handlers.picture_database_handler import PictureDatabaseHandler


class Picture(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('imageString',
                        type=str)

    def get(self, name):
        return PictureDatabaseHandler.get_picture_by_quiz_name(name), 200

    def post(self, name):
        try:
            image_data = Picture.parser.parse_args()
            PictureDatabaseHandler.save_to_db(image_data['imageString'], name)
            return {"message": "Success"}, 201
        except Exception:
            return {"message": "Server Error"}, 500
