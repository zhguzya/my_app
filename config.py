import os
from dotenv import load_dotenv

load_dotenv()

# MikroTik API
MIKROTIK_HOST = os.getenv("MIKROTIK_HOST")
MIKROTIK_USER = os.getenv("MIKROTIK_USER")
MIKROTIK_PASSWORD = os.getenv("MIKROTIK_PASSWORD")

# Endpoints
URL_DHCP_TABLE = f"{MIKROTIK_HOST}/ip/dhcp-server/lease"
URL_TRAFFIC_TABLE = f"{MIKROTIK_HOST}/queue/simple"

# База данных
DATABASE_NAME = os.getenv("DATABASE_NAME")
SCHEMA_FILE = os.getenv("SCHEMA_FILE")

# Интервал сбора (в секундах)
COLLECT_INTERVAL = int(os.getenv("COLLECT_INTERVAL", 3600))