from api.models.picture import Picture


class PictureDatabaseHandler:
    @classmethod
    def save_to_db(cls, img, quiz_name):
        try:
            save_picture = Picture(img, quiz_name)
            save_picture.save_to_db()
        except Exception as e:
            print(e)

    @classmethod
    def get_picture_by_quiz_name(cls, quiz_name):
        return Picture.get_img_by_quiz_name(quiz_name)
