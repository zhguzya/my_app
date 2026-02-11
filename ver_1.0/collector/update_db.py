from db_orm import SessionMikrotik, fill_dhcp_tables, fill_traffic_table, init_db
from .data_from_router import get_dhcp_table_from_mikrotik, get_traffic_from_mikrotik
import time


def refresh_all_data():
    init_db()

    """Создание сессии, обновление DHCP и трафика за раз"""
    session = SessionMikrotik()

    #данные с MikroTik
    dhcp_data_mikrotik = get_dhcp_table_from_mikrotik()
    traffic_data_mikrotik = get_traffic_from_mikrotik()

    # Обновление БД
    fill_dhcp_tables(session, dhcp_data_mikrotik)
    fill_traffic_table(session, traffic_data_mikrotik)

    session.commit()
    session.close()

    return {"dhcp_data_mikrotik": dhcp_data_mikrotik,  "traffic_data_mikrotik": traffic_data_mikrotik}

if __name__ == "__main__":
    refresh_all_data()