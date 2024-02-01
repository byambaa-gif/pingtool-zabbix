from pyzabbix import ZabbixAPI, ZabbixAPIException
from datetime import datetime


def login(zabbix_api_url, username, password):
    zapi = ZabbixAPI(zabbix_api_url)
    zapi.login(user=username, password=password)
    auth_token = zapi.auth
    # zapi.timeout = 5.1
    print(f"Successfully logged in. Auth token: {auth_token}")
    return zapi



def create_host_group(zapi, group_name):
    result = zapi.hostgroup.create(name=group_name)
    return result



def get_host_group_id(zapi, host_group_name):
    result = zapi.hostgroup.get(filter={"name": host_group_name})
    if result:
        return result[0]['groupid']
    else:
        print(f"Host group '{host_group_name}' not found.")
        return None



def get_template_id(zapi, template_name):
    result = zapi.template.get(filter={"host": template_name})
    if result:
        return result[0]['templateid']
    else:
        print(f"Template '{template_name}' not found.")
        return None



def create_host(zapi, host_name, ip, template_id, host_group_id):
    result = zapi.host.create(
        host=host_name,
        interfaces=[{
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": ip,
            "port": "10050",
            "dns": ""
        }],
        groups=[{
            "groupid": host_group_id
        }],
        templates=[{
            "templateid": template_id
        }]
    )
    print(result)
    print(result['hostids'])



def get_host_id(zapi, host_name):

    host_info = zapi.host.get(filter={'host': host_name}, output=['hostid', 'host'])
    
    if host_info:
        # Extract hostid
        hostid = host_info[0]['hostid']
        print(f"Host ID for {host_name}: {hostid}")
        return hostid
    else:
        print(f"No matching host found for {host_name}")




def get_zabbix_latest_value(zapi, host_name, item_key):
    try:
        host = zapi.host.get(filter={'host': host_name})
        if not host:
            raise ZabbixAPIException(f"Host '{host_name}' not found.")

        host_id = host[0]['hostid']

        item = zapi.item.get(hostids=host_id, search={'key_': item_key}, output='extend', limit=1)
        if not item:
            raise ZabbixAPIException(f"Item with key '{item_key}' not found for host '{host_name}'.")

        item_id = item[0]['itemid']

        latest_value = zapi.item.get(itemids=item_id, output='extend', limit=1)[0]['lastvalue']
        
        return latest_value

    except ZabbixAPIException as e:
        print(f"Zabbix API error: {e}")
        return None



def get_zabbix_historical_value(zapi, host_name, item_key, time_seconds):
    try:
        host = zapi.host.get(filter={'host': host_name})
        if not host:
            raise ZabbixAPIException(f"Host '{host_name}' not found.")

        host_id = host[0]['hostid']

        item = zapi.item.get(hostids=host_id, search={'key_': item_key}, output='extend', limit=1)
        if not item:
            raise ZabbixAPIException(f"Item with key '{item_key}' not found for host '{host_name}'.")

        item_id = item[0]['itemid']

        # target_timestamp = int(datetime.strptime(f'{target_date} {target_time}', '%Y-%m-%d %H:%M').timestamp())
    
        history = zapi.history.get(itemids=item_id, time_from=time_seconds, output='extend', limit=1)
        if not history:
            return None
        else:
            return history[0]['value']

    except ZabbixAPIException as e:
        print(f"Zabbix API error: {e}")
        return None
    

 
def delete_hosts(zapi, host_id):
    try:
        zapi.host.delete(params=host_id)
        print(f"Hosts with IDs {host_id} deleted successfully.")
    except ZabbixAPIException as e:
        print(f"Error deleting hosts with IDs {host_id}: {e}")



def delete_host_group(zapi, host_group_ids):
    try:
        zapi.hostgroup.delete(params = host_group_ids)
        print(f"Host groups with IDs {host_group_ids} deleted successfully.")
    except ZabbixAPIException as e:
        if 'No permissions to referred object or it does not exist!' in str(e):
            print(f"Host group {host_group_ids} not exist ")

def zabbix_logout(zabbix):
    try:
        zabbix.user.logout()
        print("Logged out from Zabbix API.")
    except ZabbixAPIException as e:
        print(f"Error during Zabbix API logout: {e}")
