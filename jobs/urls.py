from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .api import SettingsViewSet, PostViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'post', PostViewSet)

post_list = PostViewSet.as_view({
    'post': 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

settings_detail = SettingsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/post/$',
        post_list, name='post-list'),
    url(r'^api/post/(?P<pk>[0-9]+)/$',
        post_detail, name='post-detail'),
    url(r'^api/settings/(?P<pk>[0-9]+)/$',
        settings_detail, name='settings-detail'),
    url(r"^", include("common.urls")),
]
