# excelimport/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_excel, name='home'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('delete_hosts/', views.delete_hosts, name='delete_hosts'), 
    path('get_report/', views.get_report, name='get_report'),


   
]
