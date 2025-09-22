# bind = "0.0.0.0:8181"
# workers = 3



import multiprocessing

bind = "unix:/home/zhguzya/my_app/my_app.sock"
workers = multiprocessing.cpu_count() * 2 + 1
umask = 0o007
wsgi_app = "api:app"
accesslog = "-"
errorlog = "-"
loglevel = "info"