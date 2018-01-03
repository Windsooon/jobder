from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
# from django.conf.urls import url, include
from common.models import Settings
from popular.models import Popular
from rest_framework import routers, serializers, viewsets
from rest_framework import permissions as rf_permissions
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly


class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Settings
        fields = (
            'id', 'user_name', 'blog',
            'linkedin', 'location', 'visiable'
        )


class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = (rf_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class PopularSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Popular
        fields = (
            'globle_id', 'name', 'name_with_owner'
        )


class PopularViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = PopularSerializer
    queryset = Popular.objects.all()

    def get_queryset(self):
        queryset = Popular.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet)
router.register(r'popular', PopularViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r"^", include("common.urls")),
]
