from api.database_handlers.user_database_handler import UserDatabaseHandler


def authenticate(username, password):
    user = UserDatabaseHandler.get_by_username(username)
    if user and user.password == password:
        return user
