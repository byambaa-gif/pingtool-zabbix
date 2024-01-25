# excelimport/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd
import json
from excelimport import process_job
from django.http import HttpResponse

def export_excel_file(request):
    df = pd.read_excel("excel_filename.xlsx")

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=excel_filename.xlsx'
    df.to_excel(response, index=False)
    
    return response
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            print(excel_file)
            zabbix_api_url = 'http://192.168.242.32/api_jsonrpc.php'
            username = 'Admin'
            password = 'zabbix'
            zapi = process_job.login(zabbix_api_url, username, password)
            print(zapi)
            if zapi:
                template_name = "ICMP Ping"
                template_id = process_job.get_template_id(zapi, template_name)
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    job_name = row["Ажлын нэр"]
                    sheet = row["Хяналт sheet"]
                    process_job.create_host_group(zapi, job_name)
                    host_group_id = process_job.get_host_group_id(zapi, job_name)
                    print(host_group_id)
                    if host_group_id:
                        df_sheet = pd.read_excel(excel_file, sheet_name=str(sheet))
                        df_result = pd.DataFrame(columns=['serilon_name', 'wan', 'host_id', 'Before', 'After']) 
                        for index, row in df_sheet.iterrows():
                            serilon_name = row["Серилон нэр"]
                            wan = row["wan"]
                            if template_id:
                                process_job.create_host(zapi, serilon_name, wan, template_id,host_group_id)
                        
                        for index, row in df_sheet.iterrows():
                            serilon_name = row["Серилон нэр"]
                            wan=row["wan"]
                            host_id = process_job.get_host_id(zapi, serilon_name)
                            last_value = process_job.get_last_value(zapi, 'icmpping', host_id)  
                            df_result = df_result.append({'serilon_name': serilon_name, 'wan': wan, 'host_id':host_id,'Before':last_value}, ignore_index=True)
                        
                        # output_file_path = '/media/folder/result_output.xlsx'  
                        # df_result.to_excel(output_file_path, index=False)          
                    else:
                        return JsonResponse({'success': False, 'error': 'Failed to get host group ID from Zabbix API'})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to authenticate with Zabbix API'})
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})
