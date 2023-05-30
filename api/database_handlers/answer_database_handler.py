from db import db
from api.models.answer import Answer


class AnswerDatabaseHandler:
    def save_to_db(self, answer, question_id, correct):
        try:
            save_answer = Answer(answer, question_id, correct)
            save_answer.save_to_db()
        except Exception as e:
            print(e)

    def get_question_answers(self, question_id):
        return Answer.get_from_db(question_id)


