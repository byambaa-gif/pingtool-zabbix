from pyzabbix import ZabbixAPI, ZabbixAPIException

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


def get_last_value(zapi, item_key, host_id,):

    item = zapi.item.get(filter={'key_': item_key, 'hostid': host_id}, output='extend', limit=1)

    if item:
        item_id = item[0]['itemid']

        # Get the last value of the item
        history = zapi.history.get(itemids=item_id, output='extend', limit=1, sortfield='clock', sortorder='DESC')

        if history:
            last_value = history[0]['value']
            print(f"Last value of item {item_key} for host {host_id}: {last_value}")
        else:
            print(f"No history found for item {item_key}")

    else:
        print(f"No item found with key {item_key} for host {host_id}")

 
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

# zapi = login("http://127.0.0.1:8081/api_jsonrpc.php", "Admin", "zabbix")
# print(zapi)
# # Create a host group
# group_name = "Test"
# # group_result = create_host_group(zapi, group_name)
# # print(group_result)
# # Get host group ID
# host_group_id = get_host_group_id(zapi, group_name)
# print(host_group_id)
# # Get template ID (replace "Template Name" with the actual template name)
# template_name = "ICMP Ping"
# template_id = get_template_id(zapi, template_name)
# print(template_id)
# # Create a host
# result = create_host(zapi, "Sodoo", "172.30.14.36", template_id, host_group_id)
# print(result)
