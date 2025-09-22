import multiprocessing
import os

# bind = "0.0.0.0:8181"
# workers = 3

BASE_DIR = "/home/zhguzya/my_app"

bind = f"unix:{BASE_DIR}/my_app.sock"
workers = multiprocessing.cpu_count() * 2 + 1
umask = 0o007
wsgi_app = "api:app"
accesslog = f"{BASE_DIR}/logs/gunicorn_access.log"
errorlog  = f"{BASE_DIR}/logs/gunicorn_error.log"
loglevel = "info"