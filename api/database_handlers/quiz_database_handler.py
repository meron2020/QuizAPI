from api.database_handlers.question_database_handler import QuestionDatabaseHandler
from api.models.question_class import Question
from api.models.quiz import QuizModel


class QuizDatabaseHandler:
    def __init__(self):
        self.question_handler = QuestionDatabaseHandler()

    def save_to_db(self, quiz_id, question_dict):
        counter = 1
        for i in range(len(question_dict)):
            question_number = "question_" + str(counter)
            question = question_dict[question_number]
            save_question = Question(question['question'], quiz_id)
            self.question_handler.save_to_db(quiz_id, save_question, question['correctAnswer'],
                                             question['wrongAnswers'])

            counter += 1
        return True

    def get_quiz_id(self, quiz_name):
        quiz = QuizModel.get_quiz_from_db(quiz_name)
        return quiz.id

    def get_questions(self, quiz_name):
        quiz_id = self.get_quiz_id(quiz_name)
        questions = self.question_handler.retrieve_from_db(quiz_id)
        question_list = []
        for question in questions:
            answers = self.question_handler.retrieve_question_answers(question.id)
            correct_answer = ""
            wrong_answers = []
            for answer in answers:
                if answer.correct:
                    correct_answer = answer.answer
                else:
                    wrong_answers.append(answer.answer)
            question = {"question": question.question,
                        "answer_dict": {"correct_answer": correct_answer, "wrong_answers": wrong_answers}}
            question_list.append(question)

        return question_list

    def turn_to_quiz(self, quiz_name):
        quiz = self.find_by_quiz_name(quiz_name)
        questions = self.get_questions(quiz_name)
        return quiz, questions

    def find_by_quiz_name(self, quiz_name):
        return QuizModel.get_quiz_from_db(quiz_name)

    @classmethod
    def get_all_quizzes(cls):
        return QuizModel.get_all_quizzes()
