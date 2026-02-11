# from db_orm import DhcpTableOrm, TrafficTableOrm, DhcpHistoryTableOrm
from .models_mikrotik import DhcpTableOrm, DhcpHistoryTableOrm, TrafficTableOrm


def fill_dhcp_tables(session, mikrotik_dhcp_data):
    # очистка таблица dhcp_table
    session.query(DhcpTableOrm).delete()

    dhcp_history_list = session.query(DhcpHistoryTableOrm).all() #список объектов из таблицы DhcpHistoryTableOrm
    dhcp_history_set = set()
    for h in dhcp_history_list:
        dhcp_history_set.add((h.ip, h.mac_address))


    mikrotik_dhcp_set = set()
    mikrotik_dhcp_dict = {}
    for m in mikrotik_dhcp_data:
        ip = m.get("ip")
        mac = m.get("mac_address")
        host = m.get("host_name")
        age = m.get("age")
        dynamic = m.get("dynamic")
        last_seen = m.get("last_seen")

        mikrotik_dhcp_set.add((ip, mac)) #множество из tuples (ip, mac) по данным с роутера
        mikrotik_dhcp_dict[ip, mac] = m # словарик со словариками данным с роутера, ключ [ip, mac], значение - словарь  из дхцп таблицы
        # добавление в таблицу dhcp_table данных от роутера
        session.add(DhcpTableOrm(ip=ip, mac_address=mac, host_name=host, age=age, dynamic=dynamic, last_seen=last_seen))
        
        if (ip, mac) not in dhcp_history_set:
            session.add(DhcpHistoryTableOrm(ip=ip, mac_address=mac, host_name=host, dynamic=dynamic, removed=False))

    for h in dhcp_history_list:
        if (h.ip, h.mac_address) in mikrotik_dhcp_dict:
            m = mikrotik_dhcp_dict[h.ip, h.mac_address]
            h.host_name = m.get("host_name")
            h.dynamic = m.get("dynamic")
            h.removed = False
        else:
            h.removed = True
    

        
def fill_traffic_table(session, mikrotik_traffic_data):
    for t in mikrotik_traffic_data:
        traffic = TrafficTableOrm(
            ip = t["ip"],
            name = t.get("name"),
            rx_Mbytes = t.get("rx_Mbytes"),
            tx_Mbytes = t.get("tx_Mbytes")
        )
        session.add(traffic)



def get_data_from_db(session):
    dhcp_query = (session.query(DhcpTableOrm).order_by(DhcpTableOrm.updated_at.desc()).all())
    dhcp_history_query = (session.query(DhcpHistoryTableOrm).order_by(DhcpHistoryTableOrm.updated_at.desc()).all())
    traf_query = (session.query(TrafficTableOrm).order_by(TrafficTableOrm.updated_at.desc()).limit(15).all())

    dhcp_list = []
    for d in dhcp_query:
        dhcp_list.append({
            "id": d.id,
            "ip": d.ip,
            "mac_address": d.mac_address,
            "host_name": d.host_name,
            "age": d.age,
            "dynamic": d.dynamic,
            "last_seen": d.last_seen,
            "updated_at": d.updated_at.isoformat() if d.updated_at else None
        })

    dhcp_history_list = []
    for dh in dhcp_history_query :
        dhcp_history_list.append({
            "id": dh.id,
            "ip": dh.ip,
            "mac_address": dh.mac_address,
            "host_name": dh.host_name,
            "dynamic": dh.dynamic,
            "removed": dh.removed,
            "updated_at": dh.updated_at.isoformat() if dh.updated_at else None
        })

    traf_list = []
    for t in traf_query:
        traf_list.append({
            "id": t.id,
            "ip": t.ip,
            "name": t.name,
            "rx_Mbytes": t.rx_Mbytes,
            "tx_Mbytes": t.tx_Mbytes,
            "updated_at": t.updated_at.isoformat() if t.updated_at else None
        })


    session.close()
    return {"dhcp_from_db": dhcp_list,  "dhcp_history_from_db": dhcp_history_list, "traf_from_db": traf_list}



if __name__ == "__main__":
    fill_dhcp_tables()
    fill_traffic_table()
    get_data_from_db()

