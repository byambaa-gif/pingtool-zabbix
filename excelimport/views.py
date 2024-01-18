# excelimport/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd
import json
from excelimport import process_job


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            # df = pd.read_excel(excel_file)
            
            return process_job.zabbix_configuration(excel_file,"http://127.0.0.1:8081/api_jsonrpc.php","Admin","zabbix")
           
            # data_dict = df.to_dict(orient='records')
            # # Ensure valid JSON
            # json_data = json.dumps(data_dict)

            # # Create the ExcelData object
            # ExcelData.objects.create(data=json_data)

            # return JsonResponse(data_dict, safe=False)
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})
