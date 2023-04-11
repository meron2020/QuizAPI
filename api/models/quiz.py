from db import db


class QuizModel(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String)
    user = db.Column(db.String)
    questions = db.relationship('Question', lazy='dynamic')

    def __init__(self, quiz_name, user):
        self.quiz_name = quiz_name
        self.user = user

    def json(self, question_list):
        return {self.quiz_name: question_list}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_quiz_from_db(cls, quiz_name):
        return cls.query.filter_by(quiz_name=quiz_name).first()

    @classmethod
    def get_all_quizzes(cls):
        return cls.query.all()

    def get_id(self):
        return self.id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


