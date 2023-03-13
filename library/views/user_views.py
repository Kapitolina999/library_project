from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAdminUser

from library.models import User
from library.permissions import AdminOrOwnerPermission
from library.serializers import user_serializers as _


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = _.UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone']

    def perform_destroy(self, instance: User):
        instance.is_active = False
        instance.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return _.UserCreateSerializer
        return _.UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AdminOrOwnerPermission]
        return [permission() for permission in permission_classes]