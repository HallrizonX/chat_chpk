from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
