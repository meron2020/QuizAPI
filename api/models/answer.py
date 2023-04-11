from db import db


class Answer(db.Model):
    __tablename__ = "answers"


    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    correct = db.Column(db.Boolean)

    def __init__(self, answer, question_id, correct):
        self.answer = answer
        self.question_id = question_id
        self.correct = correct

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_from_db(cls, question_id):
        return cls.query.filter_by(question_id=question_id).all()

    @classmethod
    def get_correct_answer(cls, question_id):
        return cls.query.filter_by(question_id=question_id, correct=True).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
