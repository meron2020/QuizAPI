from api.database_handlers.answer_database_handler import AnswerDatabaseHandler
from api.models.question_class import Question


class QuestionDatabaseHandler:

    def __init__(self):
        self.answer_handler = AnswerDatabaseHandler()

    def save_to_db(self, quiz_id, question, answer_dict):
        try:
            question.save_to_db()
        except Exception as e:
            print(e)
        question_id = self.get_question_id(question.question, quiz_id)
        for key, value in answer_dict.items():
            if key == "correct answer":
                self.answer_handler.save_to_db(value, question_id, True)
            else:
                self.answer_handler.save_to_db(value, question_id, False)

    def get_question_id(self, question, quiz_id):
        question = Question.find_by_question_name(question=question, quiz_id=quiz_id)
        return question.id

    def delete_from_db(self, question_id):
        question = Question.find_by_question_id(question_id)
        self.answer_handler.delete_answers_from_db(question_id)
        question.delete_from_db()

    def retrieve_one_question(self, quiz_id, question_name):
        return Question.find_by_question_name(question_name, quiz_id)

    def retrieve_from_db(self, quiz_name):
        return Question.find_by_quiz(quiz_name)

    def retrieve_question_answers(self, question_id):
        answers = self.answer_handler.get_question_answers(question_id)
        return answers