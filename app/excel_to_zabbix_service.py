import pandas as pd


def create_zabbix_host_group(job_name):
    json_request = {
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": {"name": {job_name}},
        "id": 1,
    }
    print(f"{json_request}")

def process_first_sheet_for_work_name_sheet_number(file_path):
    df = pd.read_excel(file_path)
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        job_name = row["Ажлын нэр"]
        sheet =row["Хяналт sheet"]
        json = create_zabbix_host_group(job_name)
        response_json = {
            "jsonrpc": "2.0",
            "result": {
            "groupids": [
            "107819"
            ]
            },
            "id": 1
            }
        if response_json["result"]["groupids"]:
            process_every_sheet_for_host_create(file_path, sheet)
        


def process_every_sheet_for_host_create(file_path, sheet):
    df = pd.read_excel(file_path, sheet_name=str(sheet))
    for index, row in df.iterrows():
        serilon_name = row["Серилон нэр"]
        wan = row["wan"]
        print(f"ner----{serilon_name}")

