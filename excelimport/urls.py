# excelimport/urls.py
from django.urls import path
from .views import delete_hosts, upload_excel

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
    path('delete_hosts/', delete_hosts, name='delete_hosts'), 
]
