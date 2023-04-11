from client_side.request_classes import Requests
from client_side.quiz_builder import QuizBuilder
from client_side.quiz_manager import QuizManager
from client_side.add_or_remove_question import AddOrRemoveQuestion


class TriviaGame:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/"
        self.requests = Requests(self.url)

    def login(self, username, password):
        jwt_token = self.requests.login(username, password)

        return username, jwt_token

    def sign_up(self):
        username = input("Username >>")
        password = input("Password >>")
        sign_up = self.requests.sign_up(username, password)
        print(sign_up)
        if "A user with that username already exists." in sign_up:
            return False
        return [username, password]

    def make_quiz(self, username):
        quiz_dict = QuizBuilder.build_quiz(username)
        data = quiz_dict['data']
        post = self.requests.post_quiz(quiz=quiz_dict['quiz_name'], user=data['user'],
                                       question_dict=data['question_dict'])
        print(post)

    def do_quiz(self, quiz_name, jwt_token, username):
        quiz = self.requests.get_quiz(jwt_token, quiz_name)
        if "message" in quiz.keys():
            print("\nNo quiz named {}".format(quiz_name))
            return False

        quiz_manager = QuizManager(quiz_name, quiz[quiz_name])
        percentage = quiz_manager.run_whole_quiz()
        update = self.requests.update_percentage(quiz_name=quiz_name, user=username, percentage=percentage)
        print(update)
        return update

    def get_stats(self, username):
        stats = self.requests.get_stats(username)
        if "" in stats['quizzes']:
            stats['quizzes'].remove("")

        if "" in stats["quiz_scores"]:
            stats['quiz_scores'].remove("")
        print("Username >> {}".format(username))
        print("*****************")
        print("Average Score >> {}".format(stats['average']))
        print("*****************")
        try:
            col_width = max(len(quiz) for quiz in stats['quizzes'])
        except ValueError:
            print("You do not have any quizzes in your stats.")
            return
        q_s_list = ["quiz", "score"]
        print("   ".join(quiz_score.ljust(col_width) for quiz_score in q_s_list))
        print("------------------")
        for i in range(len(stats['quizzes'])):
            quiz_score_list = [stats['quizzes'][i], stats['quiz_scores'][i]]
            print("   ".join(quiz_score.ljust(col_width) for quiz_score in quiz_score_list))

    def see_all_quizzes(self):
        quizzes = self.requests.get_quizzes()
        if not quizzes:
            print("No quizzes")
        for quiz in quizzes:
            print(quiz)

    def remove_question(self, jwt_token, quiz, user):
        remove = AddOrRemoveQuestion(self.requests, jwt_token, quiz)
        response = remove.remove_question(user)
        return response

    def add_question(self, jwt_token, quiz, user):
        add = AddOrRemoveQuestion(self.requests, jwt_token, quiz)
        response = add.add_question(user)
        return response

    def trivia_game(self):
        jwt_token = ""
        username = ""
        while True:
            li_or_su = input("\nWould you like to log in or sign up?"
                             "\n 1.Sign up"
                             "\n2.Log in"
                             "\nPlease enter the number that represents what you would like to do."
                             "\n>>")
            if li_or_su == "1":
                username_password = self.sign_up()
                if not username_password:
                    continue
                username = username_password[0]
                password = username_password[1]
                token = self.login(username, password)
                jwt_token = token
                break
            elif li_or_su == "2":
                username = input("Username >>")
                password = input("Password >>")
                try:
                    token = self.login(username, password)
                    jwt_token = token
                except Exception:
                    print("Username or password incorrect! Please try again.")
                    continue
                break
            else:
                print("Answer not recognized. Please try again\n\n")
                continue
        while True:
            do_input = input("\nWhat would you like to do?"
                             "\n1.Make quiz"
                             "\n2.Do a quiz"
                             "\n3.Check your current statistics"
                             "\n4.Look at available quizzes"
                             "\n5.Add question to quiz"
                             "\n6.Remove question from quiz"
                             "\n7.Log out"
                             "\nPlease enter the number that represents what you would like to do."
                             "\n>>")
            if do_input == "1":
                self.make_quiz(username)
                print("\n")
                print("\n")
                continue

            elif do_input == "2":
                quiz = input("\n Quiz >>")
                self.do_quiz(quiz, jwt_token, username)
                continue

            elif do_input == "3":
                self.get_stats(username)
                continue

            elif do_input == "4":
                print("\n")
                self.see_all_quizzes()
                continue

            elif do_input == "5":
                print("\n")
                quiz = input("Quiz >>")
                try:
                    response = self.add_question(jwt_token, quiz, username)
                    print(response)
                except KeyError:
                    print("No quiz named {}".format(quiz))
                continue

            elif do_input == "6":
                print("\n")
                quiz = input("Quiz >>")
                try:
                    response = self.remove_question(jwt_token, quiz, username)
                    print(response)
                except KeyError:
                    print("No quiz named {}".format(quiz))
                continue

            elif do_input == "7":
                print("\nThank you for playing! See you next time!")
                exit()
            else:
                print("Answer not recognized. Please try again.\n")
                continue


trivia_game = TriviaGame()
trivia_game.trivia_game()
