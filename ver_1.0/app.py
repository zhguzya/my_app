from flask import Flask
from api import api_bp
from ui import auth_bp, ui_bp
from config import SECRET_KEY_SESSION
from db_orm import init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY_SESSION

# Регистрируем Blueprint
app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(ui_bp)


init_db()            
            
if __name__ == "__main__":
    app.run(debug=True)