from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r"^popular/", include("popular.urls")),
    url(r"^", include("common.urls")),
]
