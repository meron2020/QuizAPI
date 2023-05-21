from flask_restful import Resource, request

from api.database_handlers.picture_database_handler import PictureDatabaseHandler


class Picture(Resource):
    def get(self, name):
        return PictureDatabaseHandler.get_picture_by_quiz_name(name), 202

    def post(self, name):
        try:
            image_data = request.get_data()
            PictureDatabaseHandler.save_to_db(image_data, name)
            return {"message": "Success"}, 201
        except Exception:
            return {"message": "Server Error"}, 500
