from flask import jsonify
from redis import Redis
from rq import Queue
from db_orm import refresh_all_data

redis_conn = Redis(host='localhost', port=6379)
queue = Queue(connection=redis_conn)

def refresh():
    job = queue.enqueue(refresh_all_data)
    print(job.get_status())
    return job.id


if __name__ == "__main__":
    refresh()