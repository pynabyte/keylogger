from django.contrib import admin
from django.urls import path,include
from malware_detection.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/authentication/",include("user_management.urls")),
    path("api/malware/",include("malware_detection.urls")),
    path("",index,name='index')
]
