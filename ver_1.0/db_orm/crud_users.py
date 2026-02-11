from .models_users import UsersTableORM
     
def add_user(session, user_data):
    user = UsersTableORM(
        username = user_data.get("username"),
        email = user_data.get("email"),
        password_hash = user_data.get("password_hash")
    )
    session.add(user)


if __name__ == "__main__":
    add_user()