from .auth.auth_routes import auth_bp
from .routes.main_routes import ui_bp

__all__ = [
   "auth_bp",
   "ui_bp",
]