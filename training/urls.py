# djangotemplates/djangotemplates/urls.py

# from django.conf.urls import path, include # Add include to the imports here
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [

    path("", include("polls.urls")),
    path("-", include("Blogs.urls")),
    path("n", include("tasks.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)