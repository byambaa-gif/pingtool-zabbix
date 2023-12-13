import requests
import json

# Replace with your Zabbix API URL
zabbix_api_url = "http://your-zabbix-server/api_jsonrpc.php"

# Your login request data
login_request = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",  # Replace with your Zabbix username
        "password": "zabbix"  # Replace with your Zabbix password
    },
    "id": 1
}

# Convert the data to JSON format
login_request_json = json.dumps(login_request)

# Make the API request
response = requests.post(zabbix_api_url, data=login_request_json, headers={'Content-Type': 'application/json'})

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Parse the response JSON
    response_data = response.json()

    # Check if the response contains the authentication token
    if "result" in response_data:
        auth_token = response_data["result"]
        print(f"Successfully logged in. Auth token: {auth_token}")

        # Now you can use this auth token for subsequent API requests
        # For example, you can make another request to get host information:
        host_request = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend"
            },
            "auth": auth_token,
            "id": 2
        }

        host_request_json = json.dumps(host_request)
        host_response = requests.post(zabbix_api_url, data=host_request_json, headers={'Content-Type': 'application/json'})

        if host_response.status_code == 200:
            host_response_data = host_response.json()
            print("Host information:")
            print(json.dumps(host_response_data, indent=2))
        else:
            print(f"Failed to get host information. Status code: {host_response.status_code}")
    else:
        print(f"Login failed. Response: {response_data}")
else:
    print(f"Failed to connect to Zabbix API. Status code: {response.status_code}")
