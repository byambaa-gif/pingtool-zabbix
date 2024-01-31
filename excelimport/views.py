# excelimport/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd
import json
from excelimport import process_job
from django.http import HttpResponse
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def export_excel_file(request):
    if request.method == 'GET':
        df = pd.read_excel("excel_filename.xlsx")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename=excel_filename.xlsx'
        df.to_excel(response, index=False)
        
        return response
@csrf_exempt 
def delete_hosts(request):
    if request.method == 'DELETE':
        zabbix_api_url = 'http://127.0.0.1:8081/api_jsonrpc.php'
        username = 'Admin'
        password = 'zabbix'
        zapi = process_job.login(zabbix_api_url, username, password)

        if zapi:
            excel_file_path = os.path.join(os.getcwd(), 'media', 'result.xlsx')
            with pd.ExcelFile(excel_file_path) as excel_file:
                for sheet_name in excel_file.sheet_names:
                    df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name)
                    hostnames_to_delete = df_sheet['serilon'].tolist()
                    host_ids_to_delete = []
                    for hostname in hostnames_to_delete:
                        if hostname:
                            host_id = process_job.get_host_id(zapi, hostname)
                            if host_id is not None:
                                host = int(host_id)
                                # host_ids_to_delete.append(host)
                                process_job.delete_hosts(zapi, host)
            for sheet_name in excel_file.sheet_names:
                process_job.delete_host_group(zapi, sheet_name)   
            os.remove(excel_file_path)
            
            return JsonResponse({'success': True, 'message': 'Hosts and Host Groups deleted successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to authenticate with Zabbix API'})    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

    
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
 
            zabbix_api_url = 'http://127.0.0.1:8081/api_jsonrpc.php'
            username = 'Admin'
            password = 'zabbix'
            zapi = process_job.login(zabbix_api_url, username, password)
            print(zapi)

            if zapi:
                template_name = "ICMP Ping"
                template_id = process_job.get_template_id(zapi, template_name)
                df = pd.read_excel(excel_file)
                df_result = pd.DataFrame(columns=['groupid', 'serilon', 'wan', 'hostid', 'beforedate', 'Before', 'After'])

                for index, row in df.iterrows():
                    job_name = row["Ажлын нэр"]
                    sheet = row["Хяналт sheet"]
                    process_job.create_host_group(zapi, job_name)
                    host_group_id = process_job.get_host_group_id(zapi, job_name)
                    print(host_group_id)

                    if host_group_id:
                        df_sheet = pd.read_excel(excel_file, sheet_name=str(sheet))

                        for index_sheet, row_sheet in df_sheet.iterrows():
                            serilon_name = row_sheet["Серилон нэр"]
                            wan = row_sheet["wan"]

                            if template_id:
                                host_id = process_job.create_host(zapi, serilon_name, wan, template_id, host_group_id)
                                df_new_row = pd.DataFrame({
                                    'groupid': host_group_id,
                                    'serilon': serilon_name,
                                    'wan': wan,
                                    'hostid': host_id,
                                    'beforedate': datetime.now().strftime('%Y-%m-%d %H-%M'),
                                    'Before': None,
                                    'After': None
                                }, index=[0])

                                df_result = pd.concat([df_result, df_new_row], ignore_index=True)
                    else:
                        return JsonResponse({'success': False, 'error': 'Failed to get host group ID from Zabbix API'})
                file_path = os.path.join(os.getcwd(), 'media', 'result.xlsx')

                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    for groupid, data in df_result.groupby('groupid', dropna=False):
                        data.to_excel(writer, sheet_name=str(groupid), index=False)         
                    
            else:
                return JsonResponse({'success': False, 'error': 'Failed to authenticate with Zabbix API'})
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})
