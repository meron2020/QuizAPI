from flask_restful import Resource, reqparse

from api.database_handlers.quiz_database_handler import QuizDatabaseHandler
from api.models.quiz import QuizModel


class Quiz(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('quiz',
                        type=str)

    parser.add_argument("user",
                        required=False,
                        type=str,
                        help="This field cannot be left blank.")

    parser.add_argument("question_dict",
                        type=dict,
                        required=False)

    def __init__(self):
        self.handler = QuizDatabaseHandler()

    def get(self, name):
        try:
            quiz, question_list = self.handler.turn_to_quiz(name)
            if quiz:
                return quiz.json(question_list)
        except Exception as e:
            print(e)

        return {"message": "Quiz not found."}, 400

    def post(self, name):
        if self.handler.find_by_quiz_name(name):
            return {"message": "Quiz with the name {} already exists.".format(name)}, 400

        data = Quiz.parser.parse_args()
        quiz = QuizModel(name, data['user'])
        quiz.save_to_db()
        new_quiz = QuizModel.get_quiz_from_db(quiz.quiz_name)
        question_dict = data['question_dict']

        try:
            self.handler.save_to_db(new_quiz.id, question_dict)

        except Exception:
            return {"message": "An error occurred inserting the item."}, 500  # Internal Server Error

        return {"message": "Quiz created."}, 201


class QuizList(Resource):
    def get(self):
        return {'quizzes': list(map(lambda x: x.quiz_name, QuizDatabaseHandler.get_all_quizzes()))}

