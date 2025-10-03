import sqlite3
from config import DATABASE_NAME, SCHEMA_FILE

#create DB, tables
def create_db_tables(db_name, schema_f):
    con = sqlite3.connect(db_name)

    with open(schema_f, 'r') as f:
        schema_sql = f.read()
    con.executescript(schema_sql)

    con.close()


#add dhcp_table
def fill_dhcp_table(dhcp_table):
    con = sqlite3.connect(DATABASE_NAME)
    # insert_dhcp = 'INSERT INTO dhcp_table (ip, mac_address, host_name) VALUES (:ip, :mac_address, :host_name)'
    insert_dhcp = '''
                    INSERT INTO dhcp_table (ip, mac_address, host_name, updated_at)
                    VALUES (:ip, :mac_address, :host_name, CURRENT_TIMESTAMP)
                    ON CONFLICT(ip) DO UPDATE SET
                        mac_address=excluded.mac_address,
                        host_name=excluded.host_name,
                        updated_at=CURRENT_TIMESTAMP
                    WHERE excluded.mac_address != dhcp_table.mac_address
                    OR excluded.host_name != dhcp_table.host_name;
                    '''   
    with con:
        con.executemany(insert_dhcp, dhcp_table)
    con.close()

#add traffic_table
def fill_traffic_table(traffic_table):
    con = sqlite3.connect(DATABASE_NAME)
    insert_traffic = '''
                    INSERT INTO traffic_table (dhcp_table_id, ip, name, rx_Mbytes, tx_Mbytes, updated_at)
                    SELECT id, :ip, :name, :rx_Mbytes, :tx_Mbytes, CURRENT_TIMESTAMP
                    FROM dhcp_table
                    WHERE ip = :ip;
                    ''' 
    with con:
        con.executemany(insert_traffic, traffic_table)
    con.close()


def get_data_from_db():
    con = sqlite3.connect(DATABASE_NAME)
    con.row_factory = sqlite3.Row

    select_traffic = 'SELECT * FROM traffic_table ORDER BY updated_at DESC;'
    select_dhcp = 'SELECT * FROM dhcp_table ORDER BY updated_at DESC;'

    traf = con.execute(select_traffic).fetchall()
    traf_dict = [dict(row) for row in traf]

    dhcp = con.execute(select_dhcp).fetchall()
    dhcp_dict = [dict(row) for row in dhcp]

    con.close()
    # print(traf_dict)
    # print("\n")
    # print("\n")
    # print(dhcp_dict)
    return {"dhcp_from_db": dhcp_dict, "traf_from_db": traf_dict}


if __name__ == '__main__':
    create_db_tables(DATABASE_NAME, SCHEMA_FILE)
    get_data_from_db()

