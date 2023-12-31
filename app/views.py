# excelimport/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd
import json
from excelimport import excel_to_zabbix_service


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            # df = pd.read_excel(excel_file)
            
            return excel_to_zabbix_service.process_first_sheet_for_work_name_sheet_number(excel_file)
           
            # data_dict = df.to_dict(orient='records')
            # # Ensure valid JSON
            # json_data = json.dumps(data_dict)

            # # Create the ExcelData object
            # ExcelData.objects.create(data=json_data)

            # return JsonResponse(data_dict, safe=False)
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})
