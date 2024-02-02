

# excelapp/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import user_login  # Correct import path
from excelimport.views import get_report, get_report_page
urlpatterns = [
    path("admin/", admin.site.urls),
    path("upload/", include("excelimport.urls")),
    path("", user_login, name="user_login"),
    path('get_report_page/', get_report_page, name='get_report_page'),
    path('get_report/', get_report, name='get_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
