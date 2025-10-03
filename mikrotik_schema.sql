-- schema

create table if not exists dhcp_table (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ip          text UNIQUE,
    mac_address text,
    host_name   text,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table if not exists traffic_table (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    dhcp_table_id   INTEGER,
    ip              text not null,
    name            text not null,
    rx_Mbytes       INTEGER,
    tx_Mbytes       INTEGER,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dhcp_table_id) REFERENCES dhcp_table(id) ON DELETE SET NULL
);

