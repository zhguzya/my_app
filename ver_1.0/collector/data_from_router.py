import requests
from config import MIKROTIK_USER, MIKROTIK_PASSWORD, URL_DHCP_TABLE, URL_TRAFFIC_TABLE


def get_dhcp_table_from_mikrotik():
    result_dhcp_table = []
    data = requests.get(URL_DHCP_TABLE, auth=(MIKROTIK_USER, MIKROTIK_PASSWORD), verify=False).json()
    for device in data:
        result_dhcp_table.append({
            'ip': device['address'], 
            'mac_address': device['mac-address'], 
            'host_name': device.get('host-name'), 
            'age': device.get('age',), 
            'dynamic': device.get('dynamic') == 'true',
            'last_seen': device.get('last-seen')})
    return result_dhcp_table 

def get_traffic_from_mikrotik():
    result_traffic = []
    data = requests.get(URL_TRAFFIC_TABLE, auth=(MIKROTIK_USER, MIKROTIK_PASSWORD), verify=False).json()
    for device in data:
        result_traffic.append({
            'name': device['name'], 
            'ip': device['target'].split('/')[0], 
            'rx_Mbytes': round(int(device['bytes'].split('/')[0])/1024/1024, 3), 
            'tx_Mbytes': round(int(device['bytes'].split('/')[1])/1024/1024, 3)})     
    return result_traffic
    
if __name__ == "__main__":
    get_dhcp_table_from_mikrotik()
    get_traffic_from_mikrotik()