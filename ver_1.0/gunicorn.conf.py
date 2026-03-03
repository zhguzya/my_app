import multiprocessing

# workers = 3

BASE_DIR = "/home/zhguzya/my_app/ver_1.0"

# bind = "0.0.0.0:8000"
bind = f"unix:{BASE_DIR}/app.sock"
# workers = multiprocessing.cpu_count() * 2 + 1
umask = 0o007
wsgi_app = "app:app"
# accesslog = f"{BASE_DIR}/logs/gunicorn_access.log"
# errorlog  = f"{BASE_DIR}/logs/gunicorn_error.log"
# loglevel = "info"