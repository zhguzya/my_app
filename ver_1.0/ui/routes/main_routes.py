from flask import Blueprint, redirect, url_for, render_template, request, session, Response
from db_orm import SessionMikrotik, get_data_from_db, DhcpTableOrm
from collector import refresh_all_data
from security import require_login
import csv, io
from for_redis import refresh_data_worker
from redis import Redis
from rq import Queue, Worker
from rq.job import Job
import json
from config import REDIS_ENABLED



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
    job_status = None 
    refresh_page = False

    if request.method == "POST":
        if "from_db" in request.form:
            session_db = SessionMikrotik()
            data = get_data_from_db(session_db)
            session_db.close()
            output = (f"Получены данные из БД:\n"
                     f"DHCP: {data['dhcp_from_db']}\n"
                     f"DHCP_HISTORY: {data['dhcp_history_from_db']}\n"
                     f"Traffic: {data['traf_from_db']}\n")

        elif "from_mikrotik" in request.form:

            if REDIS_ENABLED == "false":
                # На Mac: вызываем функцию
                print("REDIS DISABLED")
                data = refresh_all_data()
                output = f"Обновлены данные с Mikrotik (тест Mac): {data}"
            else:
                # На VPS: работа с очередью и Redis
                try:
                    job_id = session.get("job_id")
                    if not job_id:
                        job = q.enqueue(refresh_all_data)
                        session["job_id"] = job.id
                        return redirect(url_for("ui.main"))

                    # если job_id есть, проверяем статус
                    job = Job.fetch(job_id, connection=redis_conn)
                    job_status = job.get_status()

                    if job_status == "finished":
                        data = job.result
                        output = (
                            f"DHCP: {data['dhcp_data_mikrotik']}\n"
                            f"Traffic: {data['traffic_data_mikrotik']}\n"
                            f"Job ID: {job_id}"
                        )
                        session.pop("job_id")
                    elif Worker.count(connection=redis_conn) > 0:
                        output = f"Задача выполняется, подождите... \nJob ID: {job_id}"
                        refresh_page = True
                    else:
                        output = f"Worker не запущен \nJob ID: {job_id}"
                        session.pop("job_id")

                except Exception:
                    output = f"Worker или Redis недоступен \nJob ID: {job_id}"
                    session.pop("job_id")

    return render_template("main.html", username=session["user"]["username"], output=output, job_status=job_status, refresh_page=refresh_page)