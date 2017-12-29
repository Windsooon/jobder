from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
# from django.conf.urls import url, include
from common.models import Settings
from rest_framework import routers, serializers, viewsets
from rest_framework import permissions as rf_permissions
from .permissions import IsOwnerOrReadOnly


class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Settings
        fields = ('id', 'user_name', 'blog', 'linkedin')


class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = (rf_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r"^", include("common.urls")),
]
