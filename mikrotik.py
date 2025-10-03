#!/usr/bin/env python3
import requests
from db import fill_dhcp_table, fill_traffic_table
from config import MIKROTIK_USER, MIKROTIK_PASSWORD, URL_DHCP_TABLE, URL_TRAFFIC_TABLE
# import json


def get_dhcp_table_from_mikrotik():
    result_dhcp_table = []
    data = requests.get(URL_DHCP_TABLE, auth=(MIKROTIK_USER, MIKROTIK_PASSWORD), verify=False).json()
    for device in data:
        host_name = device.get('host-name', 'unknown')
        result_dhcp_table.append({'ip': device['address'], 'mac_address': device['mac-address'], 'host_name': host_name})
    fill_dhcp_table(result_dhcp_table) 
    return result_dhcp_table 

def get_traffic_from_mikrotik():
    result_traffic = []
    data = requests.get(URL_TRAFFIC_TABLE, auth=(MIKROTIK_USER, MIKROTIK_PASSWORD), verify=False).json()
    for device in data:
        result_traffic.append({'name': device['name'], 'ip': device['target'].split('/')[0], 'rx_Mbytes': round(int(device['bytes'].split('/')[0])/1024/1024, 3), 'tx_Mbytes': round(int(device['bytes'].split('/')[1])/1024/1024, 3)})     
    fill_traffic_table(result_traffic)
    return result_traffic
    
if __name__ == "__main__":
    get_dhcp_table_from_mikrotik()
    get_traffic_from_mikrotik()





