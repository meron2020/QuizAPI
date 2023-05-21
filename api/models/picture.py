from db import db


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    quiz_name = db.Column(db.Integer, db.ForeignKey("quizzes.quiz_name"))

    def __init__(self, img, quiz_name):
        self.img = img
        self.quiz_name = quiz_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_img_by_quiz_name(cls, quiz_name):
        return cls.query.filter_by(quiz_name=quiz_name).first()
