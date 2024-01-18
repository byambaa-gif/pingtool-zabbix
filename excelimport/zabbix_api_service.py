import requests
import json

def login(zabbix_api_url, username, password):
    login_request = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 1
    }

    login_request_json = json.dumps(login_request)
    response = requests.post(zabbix_api_url, data=login_request_json, headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        response_data = response.json()
        if "result" in response_data:
            auth_token = response_data["result"]
            print(f"Successfully logged in. Auth token: {auth_token}")
            return auth_token
        else:
            print(f"Failed to log in. Status code: {response.status_code}")
    else:
        print(f"Login failed. Response: {response.text}")

def create_host_group(zabbix_api_url, auth_token, group_name):
    host_group_create_request = {
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": {
            "name": group_name
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
        return host_group_id
    else:
        print(f"Failed to create host group. Status code: {host_group_create_response.status_code}")
        return None

def get_template_id(zabbix_api_url, auth_token, template_name):
    template_get_request = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": ["templateid"],
            "filter": {
                "host": [template_name]
            }
        },
        "auth": auth_token,
        "id": 1
    }

    template_get_request_json = json.dumps(template_get_request)
    template_get_response = requests.post(zabbix_api_url, data=template_get_request_json, headers={'Content-Type': 'application/json'})

    if template_get_response.status_code == 200:
        template_get_response_data = template_get_response.json()
        if template_get_response_data.get("result"):
            return template_get_response_data["result"][0]["templateid"]
        else:
            print(f"Template '{template_name}' not found.")
            return None
    else:
        print(f"Failed to get template. Status code: {template_get_response.status_code}")
        return None

def create_host(zabbix_api_url, auth_token, host_name, ip, template_id, host_group_id):
    host_create_request = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": host_name,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": host_group_id
                }
            ],
            "templates": [
                {
                    "templateid": template_id
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
