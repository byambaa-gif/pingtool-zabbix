

# excelapp/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import user_login  # Correct import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("upload/", include("excelimport.urls")),
    path("", user_login, name="user_login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
