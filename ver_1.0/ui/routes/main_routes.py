from flask import Blueprint, redirect, url_for, render_template, request, session, Response
from db_orm import SessionMikrotik, get_data_from_db, DhcpTableOrm
from collector import refresh_all_data
from security import require_login
import csv, io
from for_redis import refresh_data_worker
from redis import Redis
from rq import Queue
import json


ui_bp = Blueprint("ui", __name__)

redis_conn = Redis()
q = Queue(connection=redis_conn)


@ui_bp.before_request
def protect_ui():
    return require_login("ui") 

@ui_bp.route("/")
def root_redirect():
    return redirect(url_for("ui.main"))

@ui_bp.route("/main", methods=["GET", "POST"])
def main():
    output = None
    if request.method == "POST":
        if "from_db" in request.form:
            session_db = SessionMikrotik()
            data = get_data_from_db(session_db)
            session_db.close()
            output = f"Получены данные из БД: {data}"

        elif "from_mikrotik" in request.form:
            data = refresh_all_data()
            output = f"Обновлены данные с Mikrotik: {data}"
    
    return render_template("main.html", username=session["user"]["username"], output=output)