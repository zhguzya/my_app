from redis import Redis
from rq import Queue, Worker
from rq.job import Job

#соединение и очередь (работают только на VPS)
redis_conn = Redis()
q = Queue(connection=redis_conn)

def enqueue_job(func):
    """Поставить задачу в очередь и вернуть объект Job"""
    return q.enqueue(func, result_ttl=300, failure_ttl=300, job_timeout=120)

def fetch_job(job_id):
    """Получить задачу по job_id"""
    return Job.fetch(job_id, connection=redis_conn)

def get_workers():
    """Список активных worker"""
    return Worker.all(connection=redis_conn)

def schedule_daily_refresh(func, repeat_seconds=86400):
    """Ставим задачу, повтор каждый день"""
    q.enqueue(func, repeat=repeat_seconds, job_id="daily_refresh")