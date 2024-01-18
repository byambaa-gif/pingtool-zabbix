import pandas as pd
import zabbix_api_service

def zabbix_configuration(file_path, zabbix_api_url, username, password):
    auth_token = zabbix_api_service.login(zabbix_api_url, username, password)
    if auth_token:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            job_name = row["Ажлын нэр"]
            sheet = row["Хяналт sheet"]
            host_group_id = zabbix_api_service.create_host_group(zabbix_api_url, auth_token, job_name)
            
            if host_group_id:
                df = pd.read_excel(file_path, sheet_name=str(sheet))
                for index, row in df.iterrows():
                    serilon_name = row["Серилон нэр"]
                    wan = row["wan"]
                    template_name = "ICMP ping"
                    template_id = zabbix_api_service.get_template_id(zabbix_api_url, auth_token, template_name)
                    
                    if template_id:
                        zabbix_api_service.create_host(zabbix_api_url, auth_token, serilon_name, wan, template_id, host_group_id)
