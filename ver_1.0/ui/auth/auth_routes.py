from flask import redirect, url_for, render_template, request, session, Blueprint
from db_orm import SessionUsers, add_user, UsersTableORM
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    user_data = {}

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")
        password2 = request.form.get("password2")

        user_data = {
            'username': username,
            'email': email
        }

        #Проверка на совпадение паролей
        if password != password2:
            error = "Пароли не совпадают"
            return render_template("register.html", error=error, user_data=user_data)

        session_db_users = SessionUsers()

        existing_user = session_db_users.query(UsersTableORM).filter((UsersTableORM.username == username) | (UsersTableORM.email == email)).first()

        if existing_user:
            session_db_users.close()
            error = "Пользователь c таким именем или email уже существует"
            return render_template("register.html", error=error,user_data=user_data)

        user_data['password_hash'] = generate_password_hash(password)
        add_user(session_db_users, user_data)
        session_db_users.commit()
        session_db_users.close()

        return redirect(url_for("auth.login"))
    
    if "user" in session:
        return redirect(url_for("ui.main"))
    return render_template("register.html", user_data=user_data)



def check_credentials(email, password):
    session_db_users = SessionUsers()

    user = session_db_users.query(UsersTableORM).filter_by(email=email).first()
    if not user:
        session_db_users.close()
        return None

    if not check_password_hash(user.password_hash, password):
        session_db_users.close()
        return None

    credentials = {
        "user_id": user.id,
        "username": user.username
    }

    session_db_users.close()
    return credentials

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")
        current_user = check_credentials(email, password)
        if current_user:
            session["user"] = current_user
            return redirect(url_for("ui.main"))

        return render_template("login.html", error=True)

    if "user" in session:
        return redirect(url_for("ui.main"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
