from api.database_handlers.user_database_handler import UserDatabaseHandler
from api.models.usermodel import UserModel


def authenticate(username, password):
    user = UserDatabaseHandler.get_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
