from .redis_conf import schedule_daily_refresh
from db_orm import refresh_all_data


schedule_daily_refresh(refresh_all_data, repeat_seconds=86400)

