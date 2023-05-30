from api.database_handlers.answer_database_handler import AnswerDatabaseHandler
from api.models.question_class import Question


class QuestionDatabaseHandler:

    def __init__(self):
        self.answer_handler = AnswerDatabaseHandler()

    def save_to_db(self, quiz_id, question, correct_answer, wrong_answers):
        try:
            question.save_to_db()
        except Exception as e:
            print(e)
        question_id = self.get_question_id(question.question, quiz_id)
        self.answer_handler.save_to_db(correct_answer, question_id, True)
        for wrong_answer in wrong_answers:
            self.answer_handler.save_to_db(wrong_answer, question_id, False)

    def get_question_id(self, question, quiz_id):
        question = Question.find_by_question_name(question=question, quiz_id=quiz_id)
        return question.id

    def retrieve_from_db(self, quiz_name):
        return Question.find_by_quiz(quiz_name)

    def retrieve_question_answers(self, question_id):
        answers = self.answer_handler.get_question_answers(question_id)
        return answers
