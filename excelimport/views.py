# excelimport/views.py
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd
from excelimport import zabbix_service
from django.http import HttpResponse, FileResponse, Http404, HttpResponseNotFound
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import xlsxwriter
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
from django.contrib.auth.decorators import login_required

def get_report_page(request):
    excel_url= "http://localhost:8000/media/report.xlsx"
    return render(request, 'get_report.html', {'excel_url':excel_url})

def get_report(request):
    if request.method == 'GET':
        excel_file_path = os.path.join(os.getcwd(), 'media', 'result.xlsx')   
        zabbix_api_url = 'http://127.0.0.1:8081/api_jsonrpc.php'
        username = 'Admin'
        password = 'zabbix'
        item_key = 'icmpping'
        zapi = zabbix_service.login(zabbix_api_url, username, password)
        if zapi:
            with pd.ExcelFile(excel_file_path) as excel_file:
                file_path = os.path.join(os.getcwd(), 'media', 'report.xlsx')   
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    for sheet_name in excel_file.sheet_names:
                        df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name)
                        for index, row in df_sheet.iterrows():
                            host_name = row["serilon"]
                            beforedate = row["beforedate"]
                            target_date = datetime.strptime(beforedate, '%Y-%m-%d %H:%M')
                            time_seconds = int(target_date.timestamp())

                            latest_value = zabbix_service.get_zabbix_latest_value(zapi, host_name, item_key)
                            if latest_value is not None:
                                df_sheet.at[index, 'After'] = float(latest_value)
    
                                print(f"Latest value for {host_name} - {item_key}: {latest_value}")
                            else:
                                print(f"No latest value found for {host_name} - {item_key}.")
                            
                            historical_value = zabbix_service.get_zabbix_historical_value(zapi, host_name, item_key, time_seconds)
                            if historical_value is not None:
                                df_sheet.at[index, 'Before'] = float(historical_value)
                                print(f"Historical value for {target_date} : {historical_value}")
                            else:
                                print(f"No historical data found for {target_date} .")
                            
                            df_sheet.at[index, 'ReportingTime'] =  datetime.now().strftime('%Y-%m-%d %H:%M'),
                        # STYLE
                            s = df_sheet.style.format('{:.0f}').hide([('groupid'), ('hostid')], axis="columns")

                            def map_background_color(row):
                                historical_value = row['Before']
                                latest_value = row['After']
                                return ['background-color: #a3f5a3' if historical_value == latest_value else 'background-color: #ffb3b3'] * len(row)

                            s.apply(lambda row: map_background_color(row), axis=1)

                            s.set_table_styles([
                                {'selector': '.background-color #a3f5a3', 'props': 'background-color: #a3f5a3;'},  # Bright green background
                                {'selector': '.background-color #ffb3b3', 'props': 'background-color: #ffb3b3;'},  # Bright red background
                            ], overwrite=False)
                        s.to_excel(writer, sheet_name=sheet_name)  
                        
            return JsonResponse({'success': True, 'message': 'successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to authenticate with Zabbix API'})


                        
@csrf_exempt
def delete_hosts(request):
    if request.method == 'DELETE':
        zabbix_api_url = 'http://127.0.0.1:8081/api_jsonrpc.php'
        username = 'Admin'
        password = 'zabbix'
        zapi = zabbix_service.login(zabbix_api_url, username, password)

        if zapi:
            excel_file_path = os.path.join(os.getcwd(), 'media', 'result.xlsx')
            with pd.ExcelFile(excel_file_path) as excel_file:
                for sheet_name in excel_file.sheet_names:
                    df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name)
                    hostnames_to_delete = df_sheet['serilon'].tolist()
                    for hostname in hostnames_to_delete:
                        if hostname:
                            host_id = zabbix_service.get_host_id(zapi, hostname)
                            if host_id is not None:
                                host = int(host_id)
                                zabbix_service.delete_hosts(zapi, host)
            for sheet_name in excel_file.sheet_names:
                zabbix_service.delete_host_group(zapi, sheet_name)   
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
            zapi = zabbix_service.login(zabbix_api_url, username, password)
            # excel_file_path="http://localhost:8000/media/result.xlsx"
            # print(zapi)

            if zapi:
                try:
                    template_name = "ICMP Ping"
                    template_id = zabbix_service.get_template_id(zapi, template_name)
                    df = pd.read_excel(excel_file)
                    df_result = pd.DataFrame(columns=['groupid','RFCnumber', 'serilon', 'wan', 'hostid', 'beforedate', 'Before', 'After'])

                    for index,row in df.iterrows():
                        job_name = row["Ажлын нэр"]
                        sheet = row["Хяналт sheet"]
                        tets= zabbix_service.create_host_group(zapi, job_name)
                        host_group_id = zabbix_service.get_host_group_id(zapi, job_name)
                        print(tets,"host_group_id")
                    
                        if host_group_id:
                            df_sheet = pd.read_excel(excel_file, sheet_name=str(sheet))

                            for index_sheet, row_sheet in df_sheet.iterrows():
                                serilon_name = row_sheet["Серилон нэр"]
                                wan = row_sheet["wan"]
                                wan = wan.strip()
                                if template_id:
                                    host_id = zabbix_service.create_host(zapi, serilon_name, wan, template_id, host_group_id)
                                    df_new_row = pd.DataFrame({
                                        'groupid': host_group_id,
                                        'RFCnumber': (str(sheet)),
                                        'serilon':serilon_name,
                                        'wan': wan,
                                        'hostid': host_id,
                                        'beforedate': datetime.now().strftime('%Y-%m-%d 23:30'),
                                        'Before': None,
                                        'After': None
                                    }, index=[0])

                                    df_result = pd.concat([df_result, df_new_row], ignore_index=True)
                        else:
                            return JsonResponse({'success': False, 'error': 'Failed to get host group ID from Zabbix API'})
                    file_path = os.path.join(os.getcwd(), 'media', 'result.xlsx')

                    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                        for groupid, data in df_result.groupby('groupid', dropna=False):
                            data.to_excel(writer, sheet_name=groupid, index=False)          

                except Exception as e:             
                    error_message = f"Hosts already exist"            
                    return render(request, 'upload.html', {'form': form, "error_message": error_message})
                     
    else:
        form = ExcelUploadForm()
    if form:
        excel_url= "http://localhost:8000/media/report.xlsx"       
        
        return render(request, 'upload.html', {'form': form,'excel_url':excel_url})
    else:
        return render(request, 'upload.html', {'form': form})
    
