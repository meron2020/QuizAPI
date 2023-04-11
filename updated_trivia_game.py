from client_side.request_classes import Requests
from client_side.quiz_builder import QuizBuilder
from client_side.quiz_manager import QuizManager
from client_side.add_or_remove_question import AddOrRemoveQuestion
import PySimpleGUI as sg


class TriviaGame:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/"
        self.requests = Requests(self.url)
        sg.theme("Dark Amber")

    def login(self, username, password):
        jwt_token = self.requests.login(username, password)

        return username, jwt_token

    def sign_up(self, l_or_s):
        choice, value = sg.Window(l_or_s, [[sg.T('Username'), sg.In(key='Username')],
                                                    [sg.T('Password'), sg.In(key='Password')],
                                                    [sg.B('Ok'), sg.B('Cancel')]], size=(500, 600)).read(close=True)

        if choice == "Ok":
            username = value["Username"]
            password = value["Password"]
            sign_up = self.requests.sign_up(username, password)
            choice, value = sg.Window("Sign Up", [[sg.Text(sign_up)],
                                                  [sg.B('Ok'), sg.B('Cancel')]]).read(close=True)
            #            print(sign_up)
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
        choice, value = sg.Window("Stats", [[sg.T("Username >> {}".format(username))],
                                           [sg.T("Average Score >> {}".format(stats['average']))]
                                            ], size=(500, 600)).read(close=True)
        print()
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
            li_or_su, value = sg.Window("Sign Up/Login", [
                                        [sg.T('Would you like to sign up or login?', pad=(140, 70), justification='center')],
                                        [sg.B('Sign Up', size=(10, 1), pad=(200, 10))],
                                                          [sg.B('Login', pad=(200, 10), size=(10, 1))]],
                                        size=(500, 600)).read(close=True)
            # li_or_su = input("\nWould you like to log in or sign up?"
            #                  "\n 1.Sign up"
            #                  "\n2.Log in"
            #                  "\nPlease enter the number that represents what you would like to do."
            #                  "\n>>")
            if li_or_su == "Sign Up":
                username_password = self.sign_up(li_or_su)
                if not username_password:
                    continue
                username = username_password[0]
                password = username_password[1]
                token = self.login(username, password)
                jwt_token = token
                break
            elif li_or_su == "Login":
                username_password = self.sign_up(li_or_su)
                try:
                    token = self.login(username_password[0], username_password[1])
                    jwt_token = token
                except Exception:
                    choice, value = sg.Window("Error",
                                              [[sg.Text("Username or password incorrect! Please try again.")],[sg.B('Ok'), sg.B('Cancel')]]).read(close=True)

                    continue
                break
            else:
                print("Answer not recognized. Please try again\n\n")
                continue
        while True:
            sg.theme('DarkAmber')  # Add a touch of color
            # All the stuff inside your window.

            do_input, values = sg.Window('Game Options',
                [[sg.B('Make quiz')], [sg.B('Do a quiz')], [sg.Button('Check your current statistics')],
                 [sg.Button('Look at available quizzes')], [sg.Button('Add question to quiz')],
                 [sg.Button('Remove question from quiz')], [sg.Button('Log out')]]).read(close=True)
            # = input("\nWhat would you like to do?"
            #                 "\n1.Make quiz"
            #                 "\n2.Do a quiz"
            #                 "\n3.Check your current statistics"
            #                 "\n4.Look at available quizzes"
            #                 "\n5.Add question to quiz"
            #                 "\n6.Remove question from quiz"
            #                 "\n7.Log out"
            #                 "\nPlease enter the number that represents what you would like to do."
            #                 "\n>>")
            if do_input == "Make quiz":
                self.make_quiz(username)
                print("\n")
                print("\n")
                continue

            elif do_input == "Do a quiz":
                quiz = input("\n Quiz >>")
                self.do_quiz(quiz, jwt_token, username)
                continue

            elif do_input == "Check your current statistics":
                self.get_stats(username)
                continue

            elif do_input == "Look at available quizzes":
                print("\n")
                self.see_all_quizzes()
                continue

            elif do_input == "Add question to quiz":
                print("\n")
                quiz = input("Quiz >>")
                try:
                    response = self.add_question(jwt_token, quiz, username)
                    print(response)
                except KeyError:
                    print("No quiz named {}".format(quiz))
                continue

            elif do_input == "Remove question from quiz":
                print("\n")
                quiz = input("Quiz >>")
                try:
                    response = self.remove_question(jwt_token, quiz, username)
                    print(response)
                except KeyError:
                    print("No quiz named {}".format(quiz))
                continue

            elif do_input == "Log out":
                print("\nThank you for playing! See you next time!")
                exit()
            else:
                print("Answer not recognized. Please try again.\n")
                continue


trivia_game = TriviaGame()
trivia_game.trivia_game()
