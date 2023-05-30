from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    quiz_average = db.Column(db.Integer)
    quizzes = db.Column(db.String)
    quiz_score = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.quiz_average = 0
        self.quizzes = ""
        self.quiz_score = ""

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update_average(cls, new_average, username):
        user = UserModel.find_by_username(username)
        quizzes = user.quizzes.split(",")
        average = (new_average + (user.quiz_average * (len(quizzes) - 2))) / (len(quizzes) - 1)

        user.quiz_average = average
        db.session.commit()

    @classmethod
    def add_quiz_to_user(cls, user, quiz_name, quiz_score):
        user = UserModel.find_by_username(user)
        user.quizzes = user.quizzes + quiz_name + ","
        user.quiz_score = user.quiz_score + str(quiz_score) + ","
        db.session.commit()

    @classmethod
    def get_stats(cls, username):
        user = cls.find_by_username(username)
        quizzes = user.quizzes.split(",")
        quizzes.remove('')
        quiz_scores = user.quiz_score.split(",")
        quiz_scores.remove('')
        quiz_scores = [int(i) for i in quiz_scores]
        if len(quiz_scores) == 0:
            return {"user": username, "quizzes": quizzes, "quiz_scores": quiz_scores, "average": user.quiz_average}

        combined_list = list(zip(quizzes, quiz_scores))

        # Sort the combined list based on the integers
        sorted_list = sorted(combined_list, key=lambda x: x[1], reverse=True)

        # Split the sorted list back into separate string and integer lists
        sorted_quiz_list, sorted_scores = zip(*sorted_list)

        quizzes, quiz_scores = list(sorted_quiz_list), list(sorted_scores)
        if len(quizzes) >= 10:
            quiz_scores = quiz_scores[:10]
            quizzes = quizzes[:10]
        average = user.quiz_average
        return {"user": username, "quizzes": quizzes, "quiz_scores": quiz_scores, "average": average}

    @classmethod
    def get_all_averages(cls):
        averages = cls.query.with_entities(UserModel.username, UserModel.quiz_average).all()
        averages.sort(key=lambda x: x[1], reverse=True)
        averages_list = []
        for average in averages:
            average_list = [average[0], str(int(average[1]))]
            averages_list.append(average_list)

        return {"scores": averages_list}
