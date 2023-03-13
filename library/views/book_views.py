from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from library.models import Book
from library.serializers import book_serializers as _


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = _.BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
