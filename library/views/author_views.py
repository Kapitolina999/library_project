from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from library.models import Author
from library.serializers import author_serializers as _


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = _.AuthorSerializer
    filterset_fields = ['first_name', 'last_name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
