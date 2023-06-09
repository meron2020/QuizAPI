from flask import Flask, send_from_directory
from flask_restful import Api
from api.resources.quiz import Quiz
from api.resources.quiz import QuizList
from datetime import timedelta
from db import db
from api.resources.user import User
from flask_cors import CORS
from api.resources.scores import Scoring
from api.resources.auth import Auth
from api.resources.picture import Picture

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

app.secret_key = 'jose'
CORS(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')


api.add_resource(Quiz, '/quiz/<string:name>')
api.add_resource(QuizList, '/quizzes')
api.add_resource(User, '/user/<string:name>')
api.add_resource(Auth, '/auth')
api.add_resource(Scoring, '/scoring')
api.add_resource(Picture, '/pictures/<string:name>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
