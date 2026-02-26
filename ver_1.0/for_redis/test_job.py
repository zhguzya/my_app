from flask import jsonify
from redis import Redis
from rq import Queue
from .worker_update_db import refresh_data_worker
from collector import refresh_all_data

redis_conn = Redis(host='localhost', port=6379, db=0)
queue = Queue(connection=redis_conn)

def refresh():
    # job = queue.enqueue(refresh_data_worker)
    job = queue.enqueue(refresh_all_data)
    print(job.get_status())
    return job.id


if __name__ == "__main__":
    refresh()