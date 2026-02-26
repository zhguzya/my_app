import json
from datetime import datetime
from redis import Redis
from collector import refresh_all_data

redis_conn = Redis()

def refresh_data_worker():
    # ставим статус updating
    redis_conn.set("mt_state", json.dumps({"status": "updating"}))

    result = refresh_all_data()  # возвращает dhcp_data_mikrotik и traffic_data_mikrotik
    # сохраняем результат в Redis + статус finished
    redis_conn.set("mt_state", json.dumps({
        "status": "finished",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": result
    }))


if __name__ == "__main__":
    refresh_data_worker()
    raw = redis_conn.get("mt_state")
    print("RES:", raw)