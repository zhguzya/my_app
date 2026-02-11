from flask import session, redirect, url_for

def require_login(user_type):
    if "user" not in session:
        if user_type == "api":
            return {"error": "Unauthorized"}, 401
        if user_type == "ui":
            return redirect(url_for("auth.login"))