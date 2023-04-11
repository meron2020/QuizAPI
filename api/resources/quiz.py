from flask_restful import Resource, reqparse
from api.database_handlers.quiz_database_handler import QuizDatabaseHandler
from api.models.quiz import QuizModel
from api.models.question_class import Question


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

    parser.add_argument("question_added",
                        type=dict,
                        required=False)

    parser.add_argument("question_removed",
                        type=str)

    parser.add_argument("add_question",
                        required=False,
                        type=str)

    parser.add_argument("remove_question",
                        required=False,
                        type=str)

    def __init__(self):
        self.handler = QuizDatabaseHandler()

    def get(self, name):
        try:
            quiz, question_list = self.handler.turn_to_quiz(name)
            if quiz:
                return quiz.json(question_list)
        except Exception as e:
            print(e)

        return {"message": "Quiz not found."}, 200

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

    def delete(self, name):
        quiz = self.handler.find_by_quiz_name(name)
        if quiz:
            self.handler.delete_quiz_from_db(name)
            return {"message": "Quiz deleted."}

        return {"message": "Quiz not found."}

    def put(self, name):
        data = Quiz.parser.parse_args()
        quiz = self.handler.find_by_quiz_name(name)
        if quiz:
            if quiz.user == data['user']:
                if data["add_question"] == "True":
                    question = data["question_added"]
                    save_question = Question(question['question'], quiz.id)

                    self.handler.add_question(save_question, question['answers'], quiz.id)
                    return {"message": "Question added to {}".format(name)}
                elif data["remove_question"] == "True":
                    question = data['question_removed']
                    self.handler.delete_question(question, quiz.id)
                    return {"message": "Question deleted."}
            else:
                return {"message": "You do not have permission to change this quiz."}


class QuizList(Resource):
    def get(self):
        return {'quizzes': list(map(lambda x: x.quiz_name, QuizDatabaseHandler.get_all_quizzes()))}


class checker(Resource):
    def get(self):
        return {"message": "I'm alive"}
