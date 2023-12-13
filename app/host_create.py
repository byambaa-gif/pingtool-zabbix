import requests
import json

# Replace with your Zabbix API URL and authentication token
zabbix_api_url = "http://your-zabbix-server/api_jsonrpc.php"
auth_token = "your-auth-token"

# Create a host group
host_group_create_request = {
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": "YourHostGroupName"  # Replace with your desired host group name
    },
    "auth": auth_token,
    "id": 1
}

host_group_create_request_json = json.dumps(host_group_create_request)
host_group_create_response = requests.post(zabbix_api_url, data=host_group_create_request_json, headers={'Content-Type': 'application/json'})

if host_group_create_response.status_code == 200:
    host_group_create_response_data = host_group_create_response.json()
    host_group_id = host_group_create_response_data["result"]["groupids"][0]
    print(f"Host group created. Group ID: {host_group_id}")

    # Now, create a host with the newly created host group and "ICMP Ping" template
    host_create_request = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "YourHostName",  # Replace with your desired host name
            "interfaces": [
                {
                    "type": 1,  # 1 for agent, 2 for SNMP, 3 for IPMI, 4 for JMX
                    "main": 1,
                    "useip": 1,
                    "ip": "127.0.0.1",  # Replace with the IP address of the host
                    "dns": "",
                    "port": "10050"  # Replace with the port for Zabbix agent
                }
            ],
            "groups": [
                {
                    "groupid": host_group_id
                }
            ],
            "templates": [
                {
                    "templateid": "1"  # Replace with the template ID of "Template ICMP Ping"
                }
            ]
        },
        "auth": auth_token,
        "id": 2
    }

    host_create_request_json = json.dumps(host_create_request)
    host_create_response = requests.post(zabbix_api_url, data=host_create_request_json, headers={'Content-Type': 'application/json'})

    if host_create_response.status_code == 200:
        host_create_response_data = host_create_response.json()
        host_id = host_create_response_data["result"]["hostids"][0]
        print(f"Host created. Host ID: {host_id}")
    else:
        print(f"Failed to create host. Status code: {host_create_response.status_code}")
else:
    print(f"Failed to create host group. Status code: {host_group_create_response.status_code}")
