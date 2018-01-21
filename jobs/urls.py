from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .api import SettingsViewSet, PopularViewSet, PostViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet)
router.register(r'popular', PopularViewSet)
router.register(r'post', PostViewSet)

settings_detail = SettingsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/settings/(?P<pk>[0-9]+)/$', settings_detail, name='settings-detail'),
    url(r"^", include("common.urls")),
]
