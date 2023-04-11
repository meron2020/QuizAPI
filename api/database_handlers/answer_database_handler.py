from db import db
from api.models.answer import Answer


class AnswerDatabaseHandler:
    def save_to_db(self, answer, question_id, correct):
        try:
            save_answer = Answer(answer, question_id, correct)
            save_answer.save_to_db()
        except Exception as e:
            print(e)

    def delete_answer_from_db(self, answer):
        db.session.delete(answer)
        db.session.commit()

    def get_question_answers(self, question_id):
        return Answer.get_from_db(question_id)

    def delete_answers_from_db(self, question_id):
        question_answers = Answer.get_from_db(question_id)
        for answer in question_answers:
            answer.delete_from_db()

