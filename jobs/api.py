from common.models import Settings
from post.models import Post, Repo, Popular
from rest_framework import serializers, viewsets
from rest_framework import permissions as rf_permissions
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly


class SettingsSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Settings
        fields = (
            'id', 'user_name', 'blog',
            'linkedin', 'onsite', 'visiable'
        )


class SettingsViewSet(viewsets.ModelViewSet):
    permission_classes = (rf_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class PopularSerializer(serializers.ModelSerializer):

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


class RepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repo
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    repos = serializers.ListField(
        child=serializers.JSONField(), write_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'title', 'job_des', 'repos', 'repo',
            'onsite', 'salary', 'company_name', 'location',
            'company_des', 'apply',
        )
        extra_kwargs = {
            'repo': {'read_only': True}
        }

    def bulk_update_or_create_repo(self, repos):
        return [Repo.objects.get_or_create(
            repo_id=r['id'], repo_name=r['name'],
            owner_name=r['owner_name'], html_url=r['html_url'],
            stargazers_count=r['stargazers_count'], language=r['language']
        )[0] for r in repos]

    def create(self, validated_data):
        repo_data = validated_data.pop('repos')
        repo_list = self.bulk_update_or_create_repo(repo_data)
        post = Post.objects.create(**validated_data)
        post.repo.add(*repo_list)
        return post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (rf_permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = Post.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset
