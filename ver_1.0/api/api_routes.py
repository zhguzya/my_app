from flask import session, Blueprint
from flask_restx import Api, Resource
from db_orm import get_data_from_db, SessionMikrotik
from collector import refresh_all_data
from security import require_login

# Blueprint для API
api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
api = Api(api_bp, title="Mikrotik API", version="1.0", description="Mikrotik API", doc="/")

@api_bp.before_request
def protect_api():
    return require_login("api")    

# ---------------- API Эндпоинты ----------------
@api.route("/get_data_from_db")
class MikrotikDataFromDB(Resource):
    def get(self):
        session_db = SessionMikrotik()
        data_from_db = get_data_from_db(session_db)
        session_db.close()
        return data_from_db

@api.route("/refresh_data_from_mikrotik")
class RefreshDataFromMikrotik(Resource):
    def get(self):
        return refresh_all_data()
