from flask import Blueprint, redirect, url_for, render_template, request, session, Response
from db_orm import SessionMikrotik, get_data_from_db, DhcpTableOrm
from collector import refresh_all_data
from security import require_login
import csv, io

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



@ui_bp.route("/dhcp_history")
def dhcp_history():
    session_db = SessionMikrotik()
    data = session_db.query(DhcpTableOrm).all()
    session_db.close()

    return render_template("tables.html", data=data)


@ui_bp.route("/export_csv'")
def export_csv():
    session_db = SessionMikrotik()
    rows = session_db.query(DhcpTableOrm).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "IP", "MAC", "Host", "Dynamic", "Removed"])

    for row in rows:
        writer.writerow([
            row.id,
            row.ip,
            row.mac_address,
            row.host_name,
            row.dynamic,
            row.last_seen
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=dhcp.csv"}
    )
   