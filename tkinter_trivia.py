from tkinter import *
from client_side.request_classes import Requests
from client_side.quiz_builder import QuizBuilder
from client_side.quiz_manager import QuizManager
from client_side.add_or_remove_question import AddOrRemoveQuestion


class TriviaApp:
    def __init__(self):
        self.window = Tk()
        self.url = "http://127.0.0.1:5000/"
        self.requests = Requests(self.url)

        self.state = False
        self.window.bind("<F11>", self.toggle_fullscreen())
        self.window.bind("<Escape>", self.end_fullscreen)

        # Add image file
        photo = PhotoImage(file="background2.png")
        self.canvas1 = Canvas(self.window, width=1920,
                         height=1080)

        self.canvas1.pack(fill="both", expand=True)

        # Display image
        self.canvas1.create_image(0, 0, image=photo,
                             anchor="nw")


        self.window.mainloop()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.window.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.window.attributes("-fullscreen", False)
        return "break"

    def sign_up(self):
        sign_up = Button(self.window, text="Sign Up",
                         command=self.user_and_pass(),
                         width=40, height=1)

        self.button1_canvas = self.canvas1.create_window(900, 400,
                                               anchor="nw",
                                               window=sign_up)

    def user_and_pass(self):
        username = Entry(self.window, text="Username:   ")
        password = Entry(self.window, text="Password:   ")

        self.canvas1.delete(self.canvas1.button1_canvas)
        entry_canvas = self.canvas1.create_window(900, 400,
                                                    anchor="nw",
                                                    window=username)
        password_canvas = self.canvas1.create_window(900, 400,
                                                      anchor="nw", window=password)

        sign_up = self.requests.sign_up(username.get(), password.get())

        print(sign_up)
        if "A user with that username already exists." in sign_up:
            return False
        return [username, password]


if __name__ == '__main__':
    app = TriviaApp()


