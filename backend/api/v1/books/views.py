from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from api.v1.books.serializers import BookSerializer
from apps.library.models import Book, BookAuthor
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('genres', 'book_authors__author').all()
    # queryset = Book.objects.prefetch_related(
    #     'genres',
    #     Prefetch(
    #         'book_authors',
    #         queryset=BookAuthor.objects.select_related('author')
    #     )
    # ).all()

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'authors__last_name']
    ordering_fields = ['publication_date', 'authors__last_name', 'genres__name']
    ordering = ['-publication_date',]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


