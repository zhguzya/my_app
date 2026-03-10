from flask import Blueprint, redirect, url_for, render_template, request, session, Response
from db_orm import SessionMikrotik, get_data_from_db, DhcpTableOrm
from collector import refresh_all_data
from security import require_login
import json
from config import REDIS_ENABLED
from for_redis import enqueue_job, fetch_job, get_workers



ui_bp = Blueprint("ui", __name__)



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
            
            return render_template("main.html", username=session["user"]["username"], output=output)

        elif "from_mikrotik" in request.form:

            if not REDIS_ENABLED:
                # На Mac: вызываем функцию и сразу показываем результат
                data = refresh_all_data()
                output = f"Обновлены данные с Mikrotik: {data}"
            
            else:
                # на VPS создаем задачу
                job_id = session.get("job_id")
                if not job_id:
                    try:
                        job = enqueue_job(refresh_all_data)
                        session["job_id"] = job.id
                        return redirect(url_for("ui.main"))
                    except Exception as e:
                        output = f"Redis недоступен: {e}"

    job_id = session.get("job_id")

    if job_id and REDIS_ENABLED:
        try:
            job = fetch_job(job_id)
            job_status = job.get_status()

            workers = get_workers()
            if not workers:
                output = f"Worker не запущен \nJob ID: {job_id}"
                # session.pop("job_id")

            elif job_status == "finished":
                data = job.result
                output = (
                    f"DHCP: {data['dhcp_data_mikrotik']}\n"
                    f"Traffic: {data['traffic_data_mikrotik']}\n"
                    f"Job ID: {job_id}"
                )
                session.pop("job_id")
            else:
                output = f"Задача выполняется, подождите... \nJob ID: {job_id}"
                refresh_page = True

        except Exception as e:
            output = f"Worker или Redis недоступен: {e} \nJob ID: {job_id}"
            session.pop("job_id")

    return render_template("main.html", username=session["user"]["username"], output=output, job_status=job_status, refresh_page=refresh_page)