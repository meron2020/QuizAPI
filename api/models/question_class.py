from db import db


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"))
    answers = db.relationship('Answer', lazy='dynamic')

    def __init__(self, question, quiz_id):
        self.question = question
        self.quiz_id = quiz_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_question_id(cls, question_id):
        return cls.query.filter_by(id=question_id).first()

    @classmethod
    def find_by_question_name(cls, question, quiz_id):
        return cls.query.filter_by(question=question, quiz_id=quiz_id).first()

    @classmethod
    def find_by_quiz(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()





